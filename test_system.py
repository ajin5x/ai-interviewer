"""
Comprehensive test suite for the Local AI Mock Interview Assistant.
Validates question bank, interview session logic, evaluation engine,
SQLite persistence, and PDF/Markdown/JSON exports.
"""

import sys
import json
from pathlib import Path

# Import all modules
import config
import evaluation
import interview
import database
import report

def run_tests():
    print("=" * 60)
    print("RUNNING AI MOCK INTERVIEW SYSTEM TESTS")
    print("=" * 60)

    # TEST 1: Question Bank Integrity
    print("\n[TEST 1] Verifying Question Bank...")
    assert len(config.JOB_ROLES) >= 6, "Expected at least 6 job roles"
    assert len(config.EXPERIENCE_LEVELS) == 3, "Expected 3 experience levels"
    assert len(config.BEHAVIORAL_QUESTION_BANK) >= 4, "Expected behavioral questions"

    for role in config.JOB_ROLES:
        role_data = config.QUESTION_BANK.get(role, {})
        assert role_data, f"Role {role} missing from question bank"
        for level in config.EXPERIENCE_LEVELS:
            questions = role_data.get(level, [])
            assert len(questions) > 0, f"Role '{role}' level '{level}' has no questions"
            for q in questions:
                assert "id" in q and "question" in q and "key_concepts" in q and "keywords" in q
    print("PASS: Question Bank verified across all roles and levels.")

    # TEST 2: Interview Session & Question Generation
    print("\n[TEST 2] Verifying Interview Session Generation...")
    session = interview.InterviewSession(
        role="Python Developer / Software Engineer",
        experience_level="Mid Level (3 - 5 Years)",
        category="Comprehensive (3 Technical + 2 Behavioral)"
    )
    assert len(session.questions) == 5, f"Expected 5 questions, got {len(session.questions)}"

    tech_count = sum(1 for q in session.questions if q.get("type") == "technical")
    beh_count = sum(1 for q in session.questions if q.get("type") == "behavioral")
    assert tech_count == 3, f"Expected 3 technical questions, got {tech_count}"
    assert beh_count == 2, f"Expected 2 behavioral questions, got {beh_count}"
    print(f"PASS: Session generated exactly 5 questions (3 Technical + 2 Behavioral).")

    # TEST 3: Rule-Based Evaluation Engine
    print("\n[TEST 3] Testing Rule-Based Evaluation Engine...")
    q_tech = session.questions[0]

    # Sub-test 3A: Empty/Minimal Answer
    empty_eval = evaluation.RuleBasedEvaluationEngine.evaluate_answer(q_tech, "idk")
    assert empty_eval["score"] == 0.0, f"Expected 0.0 for 'idk', got {empty_eval['score']}"
    assert len(empty_eval["areas_for_improvement"]) > 0

    # Sub-test 3B: Solid Answer for technical question
    tech_ans = q_tech.get("sample_answer")
    strong_eval = evaluation.RuleBasedEvaluationEngine.evaluate_answer(q_tech, tech_ans)
    assert strong_eval["score"] >= 8.0, f"Expected score >= 8.0 for model answer, got {strong_eval['score']}"
    assert len(strong_eval["keywords_found"]) > 0
    assert len(strong_eval["strengths"]) > 0
    print(f"PASS: Evaluation engine correctly scored empty answer (0.0) and model tech answer ({strong_eval['score']}/10.0).")

    # Sub-test 3C: Behavioral STAR Scoring
    q_beh = config.BEHAVIORAL_QUESTION_BANK[0]
    beh_ans = (
        "Situation: At my previous company, my lead proposed building an in-memory custom cache, "
        "whereas I advocated for using an established Redis cluster due to horizontal scaling requirements.\n"
        "Task: My responsibility was to ensure our caching architecture would remain reliable under black-Friday traffic without creating maintenance overhead.\n"
        "Action: I scheduled a review, benchmarked Redis performance with objective load test data, and proposed a compromise with managed failover.\n"
        "Result: The lead agreed to adopt Redis based on the benchmark results, reducing API latency by 45% with zero outages."
    )
    beh_eval = evaluation.RuleBasedEvaluationEngine.evaluate_answer(q_beh, beh_ans)
    assert beh_eval["score"] >= 7.0, f"Expected high STAR score, got {beh_eval['score']}"
    assert len(beh_eval["keywords_found"]) >= 4, f"Expected keywords, got {beh_eval['keywords_found']}"
    print(f"PASS: Behavioral STAR evaluation succeeded with score {beh_eval['score']}/10.0.")

    # Sub-test 3D: Mismatched/Off-Topic Answer
    off_topic_eval = evaluation.RuleBasedEvaluationEngine.evaluate_answer(q_tech, "I love eating chocolate ice cream on sunny days in summer.")
    assert off_topic_eval["score"] <= 2.0, f"Expected low score for off-topic answer, got {off_topic_eval['score']}"
    print(f"PASS: Off-topic detection successfully assigned low score ({off_topic_eval['score']}/10.0).")

    # TEST 4: SQLite Database Operations
    print("\n[TEST 4] Testing SQLite Database Persistence...")
    for i, q in enumerate(session.questions):
        session.record_answer(i, q.get("sample_answer", "Answer text"))

    summary = session.finish_interview()
    assert session.is_completed is True
    assert summary["total_score"] > 0

    save_ok = database.save_interview(
        summary=summary,
        questions=session.questions,
        evaluations=session.evaluations,
        answers=session.answers
    )
    assert save_ok is True, "Database save failed"

    # Query back
    all_interviews = database.get_all_interviews()
    assert len(all_interviews) >= 1, "Expected at least 1 interview record in database"

    fetched = database.get_interview_by_id(summary["session_id"])
    assert fetched is not None, "Failed to retrieve interview by session_id"
    assert len(fetched["questions_data"]) == 5, f"Expected 5 questions in DB, got {len(fetched['questions_data'])}"

    stats = database.get_statistics()
    assert stats["total_interviews"] >= 1
    print(f"PASS: SQLite database saved and retrieved session {summary['session_id'][:8]} with 5 evaluated questions.")

    # TEST 5: Reports Export (PDF, Markdown, JSON)
    print("\n[TEST 5] Testing Report Generation (PDF, Markdown, JSON)...")
    q_data_list = fetched["questions_data"]

    # Markdown Test
    md_output = report.generate_markdown_report(summary, q_data_list)
    assert "# AI Mock Interview Performance Report" in md_output
    assert "Overall Score" in md_output

    # JSON Test
    json_output = report.generate_json_report(summary, q_data_list)
    parsed = json.loads(json_output)
    assert parsed["session_summary"]["total_score"] == summary["total_score"]

    # PDF Test (ReportLab is installed!)
    pdf_bytes = report.generate_pdf_report(summary, q_data_list)
    assert pdf_bytes.startswith(b"%PDF"), f"Expected %PDF header, got {pdf_bytes[:10]}"

    # Save all reports test
    saved_paths = report.save_all_reports(summary, q_data_list)
    for fmt, p in saved_paths.items():
        assert Path(p).exists(), f"Saved {fmt} report file not found at {p}"
        assert Path(p).stat().st_size > 0, f"Saved {fmt} report file is empty"
    print(f"PASS: Generated valid Markdown, JSON, and PDF ({len(pdf_bytes)} bytes).")

    # Clean up test session from DB
    database.delete_interview(summary["session_id"])
    print("PASS: Session successfully cleaned up from SQLite test database.")

    print("\n" + "=" * 60)
    print("ALL TESTS PASSED SUCCESSFULLY! (100% OFFLINE VERIFIED)")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()
