# AI Mock Interview Assistant (100% Local & Offline)

An intelligent, privacy-first Mock Interview Assistant built with **Python**, **Streamlit**, and **SQLite**.

> **IMPORTANT**: This application runs **completely locally without any external AI APIs** (No Google Gemini, No OpenAI, No API keys, No paid services). All evaluations are computed deterministically using an explainable, transparent rule-based scoring engine.

---

## Key Features

1. **Modern SaaS Interface:** Polished, responsive layout with dashboard analytics, progress steppers, and interactive performance cards.
2. **Role & Seniority Customization:**
   - **Roles:** Python Developer / Software Engineer, Frontend Developer (React / JS), Backend Developer (API & Microservices), Data Scientist / AI Engineer, DevOps & Cloud Engineer, Product Manager.
   - **Experience Levels:** Entry Level (0-2 Yrs), Mid Level (3-5 Yrs), Senior / Staff (5+ Yrs).
3. **Curated 5-Question Session:**
   - **3 Technical Questions:** Deep-dive architectural, algorithmic, and domain questions with sample reference answers.
   - **2 Behavioral / HR Questions:** Structured situational challenges evaluated against the **STAR** (Situation, Task, Action, Result) methodology.
4. **Transparent Rule-Based Scoring Engine:**
   - Evaluates answers out of **10.0 points** across 4 objective criteria:
     - **Concept Coverage (3.5 pts):** Checks for foundational principles and thematic depth.
     - **Keyword Presence (2.5 pts):** Scans for domain terminology, acronyms, and technical precision.
     - **Structure & Completeness (2.0 pts):** Analyzes response elaboration, analytical markers, and STAR storytelling.
     - **Relevance & Focus (2.0 pts):** Measures topical density and penalizes one-line or filler responses.
   - Explicitly displays:
     - Answer relevance percentage.
     - Domain keywords detected vs. missed.
     - Missing core concepts.
     - Concrete strengths & actionable improvement areas.
     - Model reference response.
5. **Local SQLite Persistence:**
   - Automatically tracks historical sessions, question-by-question evaluations, and performance trends over time.
   - Zero database configuration required (uses Python's built-in `sqlite3`).
6. **Multi-Format Export Engine:**
   - Export full interview performance reports in **PDF**, **Markdown**, and **JSON** with a single click.

---

## Project Structure

```text
Gen Ai project/
├── app.py                # Main Streamlit web application & UI navigation
├── config.py             # Roles, levels, rubric weights & curated local question bank
├── evaluation.py         # 100% offline rule-based scoring & feedback engine
├── interview.py          # Session state orchestration & question sampling (3 Tech + 2 HR)
├── report.py             # Multi-format report exporter (PDF, Markdown, JSON)
├── database.py           # SQLite local storage & historical analytics
├── styles.css            # Custom SaaS typography, cards, badges & dark/light styling
├── requirements.txt      # Project dependencies (Streamlit & ReportLab)
├── .gitignore            # Git exclusion rules
└── README.md             # Project documentation & operational guide
```

---

## How the Local Evaluation System Works

Rather than delegating evaluations to an opaque third-party cloud LLM:
1. **Curated Rubrics:** Every question in `config.py` defines explicit `key_concepts` and `keywords`.
2. **Concept Token Analysis:** The engine evaluates semantic concept coverage by checking lemma and phrase clustering.
3. **Vocabulary Matching:** Word-boundary regular expressions verify the exact use of industry-standard technical terminology.
4. **Behavioral STAR Verification:** Behavioral answers are parsed for narrative markers (`Situation`, `Task`, `Action`, `Result`) and rewarded for thoroughness.
5. **No Hallucinations:** Scores are deterministic, repeatable, and accompanied by a clear transparency disclaimer.

---

## Installation & Running

### 1. Prerequisites
Ensure you have **Python 3.10+** installed on your system.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

*(Note: `sqlite3`, `json`, `re`, and `math` are part of the Python standard library).*

### 3. Launch the Application
Run the Streamlit application from the project root:
```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`.

---

## Zero-Gemini Architecture Verification

- **No Google Gemini packages** (`google-generativeai` is NOT required).
- **No API keys** (`GEMINI_API_KEY` or environment variables are NOT used).
- **No cloud telemetry** or remote processing of interview answers.
- **100% private and offline.**

