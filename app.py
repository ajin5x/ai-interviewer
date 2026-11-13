"""
AI Interviewer - Modern, Premium AI Interview Platform
100% Offline, Rule-Based Evaluation Engine, Space & AI Glassmorphism Theme.
Zero External Services, Zero Cloud APIs, Zero API Keys Required.
"""

import streamlit as st
import json
import os
from pathlib import Path

# Local module imports
from config import (
    APP_TITLE,
    APP_SUBTITLE,
    APP_VERSION,
    JOB_ROLES,
    EXPERIENCE_LEVELS,
    INTERVIEW_CATEGORIES,
    TOTAL_QUESTIONS_PER_INTERVIEW
)
from interview import InterviewSession
from database import (
    save_interview,
    get_all_interviews,
    get_interview_by_id,
    delete_interview,
    get_statistics
)
from report import (
    generate_markdown_report,
    generate_json_report,
    generate_pdf_report
)

# Clean, minimal AI logo combining: Robot AI antenna (🤖) + Speech bubble (💬) + Studio mic (🎤)
AI_LOGO_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="40" height="40" fill="none">
  <defs>
    <linearGradient id="aiLogoGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#3B82F6"/>
      <stop offset="50%" stop-color="#2563EB"/>
      <stop offset="100%" stop-color="#1D4ED8"/>
    </linearGradient>
    <linearGradient id="aiLogoGlow" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#60A5FA"/>
      <stop offset="100%" stop-color="#93C5FD"/>
    </linearGradient>
  </defs>
  <path d="M8 12C8 7.58172 11.5817 4 16 4H32C36.4183 4 40 7.58172 40 12V28C40 32.4183 36.4183 36 32 36H18L10 42V35.6C8.8 34.2 8 32.2 8 28V12Z" fill="url(#aiLogoGrad)"/>
  <path d="M24 4V1" stroke="url(#aiLogoGlow)" stroke-width="2.5" stroke-linecap="round"/>
  <circle cx="24" cy="1" r="1.5" fill="#93C5FD"/>
  <rect x="20" y="11" width="8" height="13" rx="4" fill="#FFFFFF"/>
  <line x1="21" y1="15" x2="27" y2="15" stroke="#2563EB" stroke-width="1.2" stroke-linecap="round"/>
  <line x1="21" y1="18" x2="27" y2="18" stroke="#2563EB" stroke-width="1.2" stroke-linecap="round"/>
  <path d="M16 19C16 23.4183 19.5817 27 24 27C28.4183 27 32 23.4183 32 19" stroke="#FFFFFF" stroke-width="2.2" stroke-linecap="round" fill="none"/>
  <line x1="24" y1="27" x2="24" y2="31" stroke="#FFFFFF" stroke-width="2.2" stroke-linecap="round"/>
  <line x1="20" y1="31" x2="28" y2="31" stroke="#FFFFFF" stroke-width="2.2" stroke-linecap="round"/>
  <path d="M12 18C11 20 11 22 12 24" stroke="#93C5FD" stroke-width="1.8" stroke-linecap="round" fill="none"/>
  <path d="M36 18C37 20 37 22 36 24" stroke="#93C5FD" stroke-width="1.8" stroke-linecap="round" fill="none"/>
</svg>"""

# Page Configuration - Branded Favicon & AI Interviewer Title
favicon_path = Path(__file__).parent / "favicon.png"
icon_arg = str(favicon_path) if favicon_path.exists() else "🤖"

st.set_page_config(
    page_title="AI Interviewer",
    page_icon=icon_arg,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

if "current_page" not in st.session_state:
    st.session_state.current_page = "Overview"

if "interview_session" not in st.session_state:
    st.session_state.interview_session = None

if "viewing_history_id" not in st.session_state:
    st.session_state.viewing_history_id = None

# Inject Global Stylesheet
css_file = Path(__file__).parent / "styles.css"
if css_file.exists():
    with open(css_file, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Inject Active Theme Variables & Cosmic Animation Behind Content
theme_val = st.session_state.theme
if theme_val == "light":
    st.markdown("""
    <style>
    :root {
        --bg-app: #F8FAFC !important;
        --bg-sidebar: #FFFFFF !important;
        --bg-card: rgba(255, 255, 255, 0.92) !important;
        --bg-card-solid: #FFFFFF !important;
        --bg-subtle: #F1F5F9 !important;
        --border-glass: rgba(226, 232, 240, 0.9) !important;
        --border-light: #E2E8F0 !important;
        --border-medium: #CBD5E1 !important;
        --text-primary: #111827 !important;
        --text-secondary: #475569 !important;
        --text-muted: #64748B !important;
        --accent-primary: #2563EB !important;
        --accent-primary-hover: #1D4ED8 !important;
        --accent-primary-glow: rgba(37, 99, 235, 0.25) !important;
        --accent-red: #DC2626 !important;
        --accent-red-subtle: #FEF2F2 !important;
        --accent-green: #059669 !important;
        --accent-green-subtle: #ECFDF5 !important;
        --shadow-glass: 0 12px 28px -6px rgba(15, 23, 42, 0.08), 0 0 0 1px rgba(226, 232, 240, 0.85) !important;
        --shadow-hover: 0 20px 42px -10px rgba(15, 23, 42, 0.15), 0 0 0 1.5px rgba(37, 99, 235, 0.35) !important;
    }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
    :root {
        --bg-app: #0F172A !important;
        --bg-sidebar: #111827 !important;
        --bg-card: rgba(30, 41, 59, 0.78) !important;
        --bg-card-solid: #1E293B !important;
        --bg-subtle: rgba(51, 65, 85, 0.6) !important;
        --border-glass: rgba(255, 255, 255, 0.1) !important;
        --border-light: rgba(255, 255, 255, 0.14) !important;
        --border-medium: rgba(255, 255, 255, 0.22) !important;
        --text-primary: #F8FAFC !important;
        --text-secondary: #CBD5E1 !important;
        --text-muted: #94A3B8 !important;
        --accent-primary: #3B82F6 !important;
        --accent-primary-hover: #60A5FA !important;
        --accent-primary-glow: rgba(59, 130, 246, 0.35) !important;
        --accent-red: #F87171 !important;
        --accent-red-subtle: rgba(248, 113, 113, 0.16) !important;
        --accent-green: #34D399 !important;
        --accent-green-subtle: rgba(52, 211, 153, 0.16) !important;
        --shadow-glass: 0 16px 36px -4px rgba(0, 0, 0, 0.45), 0 0 0 1px rgba(255, 255, 255, 0.08) !important;
        --shadow-hover: 0 24px 50px -8px rgba(0, 0, 0, 0.6), 0 0 0 1.5px rgba(59, 130, 246, 0.5) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Render Hardware-Accelerated Space / AI Background Layer
st.markdown("""
<div class="space-background">
  <div class="nebula-orb nebula-1"></div>
  <div class="nebula-orb nebula-2"></div>
  <div class="nebula-orb nebula-3"></div>
  <div class="starfield starfield-1"></div>
  <div class="starfield starfield-2"></div>
</div>
""", unsafe_allow_html=True)


# ==============================================================================
# SIDEBAR: Branding, Theme Switcher, Navigation & Practice Stats
# ==============================================================================
with st.sidebar:
    # Top-Left Branding with SVG Logo
    st.markdown(f"""
        <div class="sidebar-brand-box">
            <div>{AI_LOGO_SVG}</div>
            <div>
                <h2 class="sidebar-brand-title">AI Interviewer</h2>
                <div class="sidebar-brand-sub">{APP_VERSION}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Day / Night Mode Toggle
    is_dark = (st.session_state.theme == "dark")
    col_t_label, col_t_switch = st.columns([3, 2])
    with col_t_label:
        st.markdown(
            "<span style='font-size:0.85rem; font-weight:600; color:var(--text-secondary);'>"
            + ("🌙 Dark Mode" if is_dark else "☀️ Light Mode")
            + "</span>",
            unsafe_allow_html=True
        )
    with col_t_switch:
        toggle_state = st.toggle("Theme", value=is_dark, label_visibility="collapsed", key="theme_toggle_switch")
        new_theme = "dark" if toggle_state else "light"
        if new_theme != st.session_state.theme:
            st.session_state.theme = new_theme
            st.rerun()

    st.markdown("---")

    # Navigation Options
    nav_options = [
        "Overview",
        "Take Interview",
        "Performance Report",
        "Interview History",
        "Evaluation Rubric"
    ]

    nav_index = 0
    if st.session_state.current_page in nav_options:
        nav_index = nav_options.index(st.session_state.current_page)

    selected_nav = st.radio(
        "Navigation",
        nav_options,
        index=nav_index,
        label_visibility="collapsed"
    )

    if selected_nav != st.session_state.current_page:
        st.session_state.current_page = selected_nav
        st.rerun()

    st.markdown("---")

    # System Architecture Glass Card
    st.markdown("#### System Architecture")
    st.markdown("""
        <div class="info-note">
            <strong>Engine:</strong> 100% Local Rule-Based<br>
            <strong>Storage:</strong> SQLite DB Persistent<br>
            <strong>Privacy:</strong> Zero Cloud Telemetry<br>
            <strong>Latency:</strong> Instant Offline Feedback
        </div>
    """, unsafe_allow_html=True)

    # Database Statistics Glass Card
    stats = get_statistics()
    st.markdown("---")
    st.markdown("#### Practice Analytics")
    st.metric("Total Completed", stats.get("total_interviews", 0))
    st.metric("Average Score", f"{stats.get('average_score', 0.0)}%")
    st.caption(f"Top Discipline: {stats.get('top_role', 'None')}")


# ==============================================================================
# PAGE 1: OVERVIEW / HOMEPAGE
# ==============================================================================
if st.session_state.current_page == "Overview":
    # Main Page Header with Logo & AI Interviewer Branding
    st.markdown(f"""
        <div class="hero-section">
            <div class="hero-tag-badge">
                {AI_LOGO_SVG}
                <span>Next-Gen AI Interview Platform</span>
            </div>
            <h1 class="hero-heading">Practice Interviews. Master Your Answers.</h1>
            <p class="hero-description">
                Prepare for top engineering and product roles with structured technical and behavioral questions.
                Submit answers and receive instant, transparent feedback on concept coverage, keyword depth,
                and architectural trade-offs.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # 3 Step Workflow Cards
    st.markdown("### How AI Interviewer Works")
    st.markdown("<p style='color:var(--text-muted); font-size:0.9rem; margin-bottom:1.5rem;'>A repeatable, high-signal preparation system for measurable growth.</p>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
            <div class="step-card">
                <div class="step-num">Step 1</div>
                <div class="step-title">Target Role &amp; Seniority</div>
                <p class="step-desc">
                    Choose your target engineering discipline and seniority level to generate targeted questions from our curated question bank.
                </p>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div class="step-card">
                <div class="step-num">Step 2</div>
                <div class="step-title">5 Structured Questions</div>
                <p class="step-desc">
                    Answer 3 in-depth technical problems and 2 behavioral scenarios evaluated against the rigorous STAR storytelling methodology.
                </p>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
            <div class="step-card">
                <div class="step-num">Step 3</div>
                <div class="step-title">Actionable Analytics</div>
                <p class="step-desc">
                    Review your score out of 10.0, matched keywords, missed concepts, strengths, and reference answers. Export to PDF, Markdown, or JSON.
                </p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Configuration & Practice Session Launch Card
    st.markdown("### Start Practice Session")
    st.markdown("<p style='color:var(--text-muted); font-size:0.9rem; margin-bottom:1.25rem;'>Select your interview configuration below to start immediately.</p>", unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            chosen_role = st.selectbox("Target Role", JOB_ROLES, index=0)
        with c2:
            chosen_level = st.selectbox("Experience Level", EXPERIENCE_LEVELS, index=0)
        with c3:
            chosen_category = st.selectbox("Interview Category", INTERVIEW_CATEGORIES, index=0)

        st.markdown("<br>", unsafe_allow_html=True)
        start_btn = st.button("🚀 Start Interview", type="primary", use_container_width=True)
        if start_btn:
            session = InterviewSession(chosen_role, chosen_level, chosen_category)
            st.session_state.interview_session = session
            st.session_state.current_page = "Take Interview"
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)


# ==============================================================================
# PAGE 2: TAKE INTERVIEW
# ==============================================================================
elif st.session_state.current_page == "Take Interview":
    session = st.session_state.interview_session

    if session is None:
        st.info("No active interview session. Configure your parameters below to start.")
        c1, c2, c3 = st.columns(3)
        with c1:
            role_sel = st.selectbox("Target Role", JOB_ROLES, key="init_role")
        with c2:
            level_sel = st.selectbox("Experience Level", EXPERIENCE_LEVELS, key="init_level")
        with c3:
            cat_sel = st.selectbox("Interview Category", INTERVIEW_CATEGORIES, key="init_cat")

        if st.button("🚀 Start Interview", type="primary"):
            st.session_state.interview_session = InterviewSession(role_sel, level_sel, cat_sel)
            st.rerun()

    else:
        total_q = len(session.questions)
        curr_q = session.current_index
        q_data = session.questions[curr_q]
        q_type = q_data.get("type", "technical").capitalize()
        topic = q_data.get("topic", "General")
        progress_pct = int(((curr_q + 1) / total_q) * 100)

        # Session Header
        col_meta, col_actions = st.columns([4, 1])
        with col_meta:
            st.markdown(f"### {session.role}")
            st.caption(f"Seniority: {session.experience_level} • Category: {session.category}")
        with col_actions:
            if st.button("Exit Session", type="secondary", help="Return to overview"):
                st.session_state.interview_session = None
                st.session_state.current_page = "Overview"
                st.rerun()

        # Animated Progress Bar Card
        st.markdown(f"""
            <div class="progress-container">
                <div class="progress-header-row">
                    <span class="progress-title">Question {curr_q + 1} of {total_q}</span>
                    <span class="progress-percentage">{progress_pct}% Completed</span>
                </div>
                <div class="progress-track">
                    <div class="progress-fill" style="width: {progress_pct}%;"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Question Step Status Pills
        step_cols = st.columns(total_q)
        for i in range(total_q):
            is_active = (i == curr_q)
            is_answered = bool(session.answers.get(i, "").strip())
            q_kind = session.questions[i].get("type", "tech")[:4].upper()

            with step_cols[i]:
                status_class = "active" if is_active else ("completed" if is_answered else "")
                st.markdown(f"""
                    <div class="progress-pill {status_class}">
                        Q{i+1}: {q_kind}
                    </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Question Presentation Card
        label_class = "technical" if q_type.lower() == "technical" else "behavioral"
        st.markdown(f"""
            <div class="question-panel">
                <div class="question-meta-row">
                    <span class="question-label">Question {curr_q + 1} of {total_q}</span>
                    <span class="question-label {label_class}">{q_type}</span>
                    <span class="question-label">{topic}</span>
                </div>
                <p class="question-prompt">{q_data.get('question', '')}</p>
            </div>
        """, unsafe_allow_html=True)

        if q_data.get("guidance"):
            st.markdown(f"""
                <div class="guidance-callout">
                    <strong>💡 Interviewer Focus:</strong> {q_data.get('guidance')}
                </div>
            """, unsafe_allow_html=True)

        # Answer Input Area
        existing_ans = session.answers.get(curr_q, "")
        user_answer = st.text_area(
            "Your Response",
            value=existing_ans,
            height=220,
            placeholder="Structure your answer clearly. Detail your architectural choices, trade-offs, edge cases, or STAR situations...",
            key=f"ans_input_{curr_q}"
        )

        word_count = len(user_answer.split()) if user_answer else 0
        st.caption(f"Length: {word_count} words • Recommended depth: 60 to 150 words.")

        # Save answer on typing
        session.record_answer(curr_q, user_answer)

        # Action Buttons Navigation
        st.markdown("<br>", unsafe_allow_html=True)
        col_eval, col_nav = st.columns([2, 3])

        with col_eval:
            check_live = st.button("🔍 Check Answer", type="secondary", help="Preview real-time feedback without advancing")

        with col_nav:
            btn_prev, btn_next = st.columns(2)
            with btn_prev:
                if curr_q > 0:
                    if st.button("← Previous", use_container_width=True):
                        session.current_index -= 1
                        st.rerun()

            with btn_next:
                if curr_q < total_q - 1:
                    if st.button("Next Question →", type="primary", use_container_width=True):
                        session.current_index += 1
                        st.rerun()
                else:
                    if st.button("Submit & Finish Interview", type="primary", use_container_width=True):
                        summary = session.finish_interview()
                        save_interview(
                            summary=summary,
                            questions=session.questions,
                            evaluations=session.evaluations,
                            answers=session.answers
                        )
                        st.session_state.current_page = "Performance Report"
                        st.rerun()

        # Instant Live Feedback Preview if requested
        if check_live:
            ev = session.evaluate_current_question(curr_q)
            st.markdown("---")
            st.markdown(f"#### Real-Time Evaluation: Question {curr_q + 1}")

            c_sc1, c_sc2, c_sc3 = st.columns(3)
            with c_sc1:
                st.metric("Estimated Score", f"{ev.get('score', 0.0)} / 10.0")
            with c_sc2:
                st.metric("Relevance Match", f"{ev.get('relevance_level')} ({ev.get('relevance_pct')}%)")
            with c_sc3:
                st.metric("Word Count", f"{ev.get('word_count', 0)} words")

            c_f1, c_f2 = st.columns(2)
            with c_f1:
                st.markdown("**Matched Keywords:**")
                if ev.get("keywords_found"):
                    for kw in ev["keywords_found"]:
                        st.markdown(f"<span class='badge-tag match'>✓ {kw}</span>", unsafe_allow_html=True)
                else:
                    st.caption("No domain keywords matched yet.")

                st.markdown("**Key Strengths:**")
                for s in ev.get("strengths", []):
                    st.markdown(f"- {s}")

            with c_f2:
                st.markdown("**Missing Key Concepts:**")
                if ev.get("missing_concepts"):
                    for mc in ev["missing_concepts"]:
                        st.markdown(f"<span class='badge-tag missing'>⚠ {mc}</span>", unsafe_allow_html=True)
                else:
                    st.caption("All rubric concepts addressed.")

                st.markdown("**Areas for Improvement:**")
                for imp in ev.get("areas_for_improvement", []):
                    st.markdown(f"- {imp}")

            with st.expander("Reference Model Answer"):
                st.markdown(f"<div class='reference-box'>{ev.get('suggested_improved_answer')}</div>", unsafe_allow_html=True)


# ==============================================================================
# PAGE 3: PERFORMANCE REPORT (RESULTS DASHBOARD)
# ==============================================================================
elif st.session_state.current_page == "Performance Report":
    session = st.session_state.interview_session

    if session is None or not session.is_completed:
        st.info("No completed interview report in the active session.")
        if st.button("Start New Interview", type="primary"):
            st.session_state.current_page = "Take Interview"
            st.rerun()
    else:
        summary = session.get_summary()

        st.markdown("## Interview Performance Dashboard")
        st.caption(f"Role: {summary['role']} • Seniority: {summary['experience_level']} • Date: {summary['created_at']}")

        # Circular Score Indicator + Metric Cards Grid
        pct_val = summary.get("percentage", 0.0)
        circumference = 339.29
        dash_offset = circumference - (circumference * (pct_val / 100.0))

        dash_col1, dash_col2 = st.columns([1, 2])

        with dash_col1:
            st.markdown(f"""
                <div class="glass-card circular-score-box">
                    <svg class="score-circle-svg" width="160" height="160" viewBox="0 0 140 140">
                        <defs>
                            <linearGradient id="scoreGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                                <stop offset="0%" stop-color="#3B82F6"/>
                                <stop offset="50%" stop-color="#60A5FA"/>
                                <stop offset="100%" stop-color="#818CF8"/>
                            </linearGradient>
                        </defs>
                        <circle class="score-circle-bg" cx="70" cy="70" r="54"/>
                        <circle class="score-circle-progress" cx="70" cy="70" r="54"
                                stroke-dasharray="{circumference}"
                                stroke-dashoffset="{dash_offset}"/>
                        <g transform="rotate(90 70 70)">
                            <text class="score-circle-text" x="70" y="72" text-anchor="middle" dominant-baseline="central">
                                {pct_val}%
                            </text>
                            <text class="score-circle-subtext" x="70" y="96" text-anchor="middle">
                                ACCURACY
                            </text>
                        </g>
                    </svg>
                    <div style="margin-top:1rem; font-weight:700; font-size:1.05rem; color:var(--text-primary);">
                        {summary.get('grade', 'Completed')}
                    </div>
                    <div style="font-size:0.85rem; color:var(--text-muted); margin-top:2px;">
                        Composite Accuracy Tier
                    </div>
                </div>
            """, unsafe_allow_html=True)

        with dash_col2:
            m_r1_c1, m_r1_c2 = st.columns(2)
            with m_r1_c1:
                st.markdown(f"""
                    <div class="metric-tile">
                        <div class="metric-caption">🎯 Overall Score</div>
                        <div class="metric-number">{summary['total_score']} <span style="font-size:1rem; color:var(--text-muted);">/ {summary['max_possible_score']}</span></div>
                        <div class="metric-sub">{summary['percentage']}% composite score</div>
                    </div>
                """, unsafe_allow_html=True)
            with m_r1_c2:
                st.markdown(f"""
                    <div class="metric-tile">
                        <div class="metric-caption">💻 Technical Average</div>
                        <div class="metric-number">{summary['tech_average']} <span style="font-size:1rem; color:var(--text-muted);">/ 10.0</span></div>
                        <div class="metric-sub">Across 3 domain questions</div>
                    </div>
                """, unsafe_allow_html=True)

            m_r2_c1, m_r2_c2 = st.columns(2)
            with m_r2_c1:
                st.markdown(f"""
                    <div class="metric-tile">
                        <div class="metric-caption">🤝 Behavioral Average</div>
                        <div class="metric-number">{summary['behavioral_average']} <span style="font-size:1rem; color:var(--text-muted);">/ 10.0</span></div>
                        <div class="metric-sub">Across 2 STAR scenarios</div>
                    </div>
                """, unsafe_allow_html=True)
            with m_r2_c2:
                mins, secs = divmod(summary['duration_seconds'], 60)
                duration_str = f"{mins}m {secs}s" if mins > 0 else f"{secs}s"
                st.markdown(f"""
                    <div class="metric-tile">
                        <div class="metric-caption">⏱️ Response Time</div>
                        <div class="metric-number">{duration_str}</div>
                        <div class="metric-sub">Total session duration</div>
                    </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Working Export Buttons in Glass Card
        st.markdown("### Export Performance Report")
        st.markdown("<p style='color:var(--text-muted); font-size:0.9rem; margin-bottom:1.25rem;'>Download an offline copy of your performance evaluation.</p>", unsafe_allow_html=True)

        prepared_questions = []
        for idx, q in enumerate(session.questions):
            ev = session.evaluations.get(idx, {})
            item = dict(q)
            item.update(ev)
            item["candidate_answer"] = session.answers.get(idx, "")
            prepared_questions.append(item)

        d1, d2, d3 = st.columns(3)
        with d1:
            pdf_bytes = generate_pdf_report(summary, prepared_questions)
            st.download_button(
                label="📄 Download PDF Report",
                data=pdf_bytes,
                file_name=f"ai_interview_report_{summary['session_id'][:8]}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        with d2:
            md_text = generate_markdown_report(summary, prepared_questions)
            st.download_button(
                label="📝 Download Markdown (.md)",
                data=md_text,
                file_name=f"ai_interview_report_{summary['session_id'][:8]}.md",
                mime="text/markdown",
                use_container_width=True
            )
        with d3:
            json_text = generate_json_report(summary, prepared_questions)
            st.download_button(
                label="📊 Download JSON (.json)",
                data=json_text,
                file_name=f"ai_interview_report_{summary['session_id'][:8]}.json",
                mime="application/json",
                use_container_width=True
            )

        st.markdown("---")
        st.markdown("### Question Breakdown & Detailed Evaluation")

        for idx, q in enumerate(session.questions):
            ev = session.evaluations.get(idx, {})
            ans_text = session.answers.get(idx, "")
            score = ev.get("score", 0.0)
            q_topic = q.get("topic", "General")
            q_type = q.get("type", "tech").capitalize()

            with st.expander(f"Question {idx+1}: {q_topic} ({q_type}) • Score: {score} / 10.0", expanded=(idx == 0)):
                st.markdown(f"**Prompt:** *{q.get('question')}*")
                st.markdown("**Candidate Response:**")
                st.markdown(f"> {ans_text if ans_text else '(No response submitted)'}")

                m1, m2, m3 = st.columns(3)
                m1.metric("Score", f"{score} / 10.0")
                m2.metric("Relevance", f"{ev.get('relevance_level', 'Unknown')}")
                m3.metric("Word Count", f"{ev.get('word_count', 0)} words")

                f1, f2 = st.columns(2)
                with f1:
                    st.markdown("**Identified Strengths:**")
                    for s in ev.get("strengths", []):
                        st.markdown(f"- {s}")

                    st.markdown("**Keywords Detected:**")
                    if ev.get("keywords_found"):
                        for kw in ev["keywords_found"]:
                            st.markdown(f"<span class='badge-tag match'>✓ {kw}</span>", unsafe_allow_html=True)
                    else:
                        st.caption("No domain keywords matched.")

                with f2:
                    st.markdown("**Areas for Improvement:**")
                    for imp in ev.get("areas_for_improvement", []):
                        st.markdown(f"- {imp}")

                    st.markdown("**Missing Key Concepts:**")
                    if ev.get("missing_concepts"):
                        for mc in ev["missing_concepts"]:
                            st.markdown(f"<span class='badge-tag missing'>⚠ {mc}</span>", unsafe_allow_html=True)
                    else:
                        st.caption("All rubric concepts addressed.")

                st.markdown("**Reference Model Answer:**")
                st.markdown(f"<div class='reference-box'>{ev.get('suggested_improved_answer', '')}</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Start Another Interview", type="primary"):
            st.session_state.interview_session = None
            st.session_state.current_page = "Overview"
            st.rerun()


# ==============================================================================
# PAGE 4: INTERVIEW HISTORY
# ==============================================================================
elif st.session_state.current_page == "Interview History":
    st.markdown("## Interview History")
    st.caption("Past sessions preserved in your local SQLite database.")

    all_sessions = get_all_interviews()

    if not all_sessions:
        st.info("No recorded interview sessions found. Complete an interview to view performance history.")
        if st.button("Start an Interview", type="primary"):
            st.session_state.current_page = "Overview"
            st.rerun()

    else:
        if st.session_state.viewing_history_id:
            detailed = get_interview_by_id(st.session_state.viewing_history_id)
            if detailed:
                if st.button("← Back to All Sessions"):
                    st.session_state.viewing_history_id = None
                    st.rerun()

                st.markdown(f"### Session Details: {detailed['role']}")
                st.caption(f"Session ID: {detailed['session_id']} • Date: {detailed['created_at']}")

                c1, c2, c3 = st.columns(3)
                c1.metric("Overall Score", f"{detailed['total_score']} / {detailed['max_possible_score']} ({detailed['percentage']}%)")
                c2.metric("Tech Average", f"{detailed.get('tech_average', 0.0)} / 10.0")
                c3.metric("Behavioral Average", f"{detailed.get('behavioral_average', 0.0)} / 10.0")

                st.markdown("---")
                st.markdown("#### Export This Session")
                p1, p2, p3 = st.columns(3)
                q_data = detailed.get("questions_data", [])

                with p1:
                    pdf_bytes = generate_pdf_report(detailed, q_data)
                    st.download_button("📄 Download PDF", pdf_bytes, file_name=f"history_{detailed['session_id'][:8]}.pdf", mime="application/pdf")
                with p2:
                    md_text = generate_markdown_report(detailed, q_data)
                    st.download_button("📝 Download Markdown", md_text, file_name=f"history_{detailed['session_id'][:8]}.md", mime="text/markdown")
                with p3:
                    json_text = generate_json_report(detailed, q_data)
                    st.download_button("📊 Download JSON", json_text, file_name=f"history_{detailed['session_id'][:8]}.json", mime="application/json")

                st.markdown("---")
                for q in q_data:
                    idx = q["question_index"] + 1
                    with st.expander(f"Question {idx}: {q.get('topic', 'General')} • Score: {q.get('score', 0)} / 10.0"):
                        st.markdown(f"**Prompt:** *{q.get('question_text', '')}*")
                        st.markdown(f"**Candidate Response:** {q.get('candidate_answer', '(None)')}")
                        st.markdown(f"**Score:** {q.get('score', 0)} / 10.0 (Relevance: {q.get('relevance_level', '')})")
                        st.markdown(f"**Keywords Detected:** {', '.join(q.get('keywords_found', [])) or 'None'}")
                        st.markdown(f"**Strengths:** {'; '.join(q.get('strengths', [])) or 'None'}")
                        st.markdown(f"**Areas for Improvement:** {'; '.join(q.get('areas_for_improvement', [])) or 'None'}")
                        st.markdown(f"**Model Answer:**\n```\n{q.get('suggested_answer', '')}\n```")

            else:
                st.session_state.viewing_history_id = None
                st.rerun()

        else:
            for s in all_sessions:
                with st.container():
                    st.markdown('<div class="section-card">', unsafe_allow_html=True)
                    c_info, c_score, c_btn = st.columns([4, 2, 2])
                    with c_info:
                        st.markdown(f"**{s['role']}** ({s['experience_level']})")
                        st.caption(f"Category: {s['category']} • Recorded: {s['created_at']}")
                    with c_score:
                        st.markdown(f"### {s['total_score']} / {s['max_possible_score']}")
                        st.caption(f"Composite: {s['percentage']}%")
                    with c_btn:
                        if st.button("View Details", key=f"view_{s['session_id']}"):
                            st.session_state.viewing_history_id = s["session_id"]
                            st.rerun()
                        if st.button("Delete", key=f"del_{s['session_id']}"):
                            delete_interview(s["session_id"])
                            st.rerun()
                    st.markdown('</div><br>', unsafe_allow_html=True)


# ==============================================================================
# PAGE 5: EVALUATION RUBRIC & METHODOLOGY
# ==============================================================================
elif st.session_state.current_page == "Evaluation Rubric":
    st.markdown("## Evaluation Engine Rubric & Methodology")
    st.markdown("""
        **AI Interviewer** operates on an **offline, deterministic rule-based evaluation engine**.
        Scoring is completely transparent, objective, and repeatable without any cloud or API key dependencies.
    """)

    st.markdown("### The 10-Point Scoring Framework")
    r1, r2, r3, r4 = st.columns(4)
    with r1:
        st.markdown("""
            <div class="metric-tile">
                <div class="metric-caption">1. Concept Coverage</div>
                <div class="metric-number">3.5 <span style="font-size:1rem; color:var(--text-muted);">pts</span></div>
                <div class="metric-sub">Matches fundamental architectural mechanisms and domain principles.</div>
            </div>
        """, unsafe_allow_html=True)
    with r2:
        st.markdown("""
            <div class="metric-tile">
                <div class="metric-caption">2. Domain Terminology</div>
                <div class="metric-number">2.5 <span style="font-size:1rem; color:var(--text-muted);">pts</span></div>
                <div class="metric-sub">Scans for industry terminology, standard acronyms, and technical precision.</div>
            </div>
        """, unsafe_allow_html=True)
    with r3:
        st.markdown("""
            <div class="metric-tile">
                <div class="metric-caption">3. Structure &amp; Depth</div>
                <div class="metric-number">2.0 <span style="font-size:1rem; color:var(--text-muted);">pts</span></div>
                <div class="metric-sub">Evaluates trade-off articulation, elaboration, or STAR storytelling.</div>
            </div>
        """, unsafe_allow_html=True)
    with r4:
        st.markdown("""
            <div class="metric-tile">
                <div class="metric-caption">4. Relevance &amp; Focus</div>
                <div class="metric-number">2.0 <span style="font-size:1rem; color:var(--text-muted);">pts</span></div>
                <div class="metric-sub">Penalizes filler or off-topic responses; rewards concise, focused answers.</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Behavioral Evaluation: The STAR Framework")
    st.markdown("""
        Behavioral and situational responses are evaluated using the four pillars of the **STAR** method:
        - **Situation (S):** Contextual background of the business or technical scenario.
        - **Task (T):** Your specific responsibility, challenge, or objective.
        - **Action (A):** The concrete technical measures, communication decisions, and steps taken.
        - **Result (R):** Quantifiable outcome, business impact, or engineering lesson learned.
    """)
