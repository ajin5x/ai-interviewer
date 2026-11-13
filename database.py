"""
Database management module using Python's standard sqlite3 library.
Stores interview session summaries and question-by-question evaluations.
Zero external database servers or cloud dependencies required.
"""

import sqlite3
import json
from typing import Dict, Any, List, Optional
from config import DB_PATH


def get_db_connection() -> sqlite3.Connection:
    """Creates and returns a connection to the local SQLite database."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Initializes the database tables if they do not exist."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Sessions Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interview_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT UNIQUE NOT NULL,
            role TEXT NOT NULL,
            experience_level TEXT NOT NULL,
            category TEXT NOT NULL,
            total_score REAL NOT NULL,
            max_possible_score REAL NOT NULL,
            percentage REAL NOT NULL,
            grade TEXT NOT NULL,
            tech_average REAL,
            behavioral_average REAL,
            duration_seconds INTEGER,
            created_at TEXT NOT NULL
        )
    """)

    # Question Answers & Evaluations Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interview_answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            question_index INTEGER NOT NULL,
            question_id TEXT NOT NULL,
            question_type TEXT NOT NULL,
            topic TEXT NOT NULL,
            question_text TEXT NOT NULL,
            candidate_answer TEXT,
            score REAL NOT NULL,
            relevance_level TEXT,
            relevance_pct INTEGER,
            keywords_found_json TEXT,
            missing_concepts_json TEXT,
            strengths_json TEXT,
            improvements_json TEXT,
            suggested_answer TEXT,
            breakdown_json TEXT,
            word_count INTEGER,
            FOREIGN KEY (session_id) REFERENCES interview_sessions (session_id) ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()


def save_interview(summary: Dict[str, Any], questions: List[Dict[str, Any]], evaluations: Dict[int, Dict[str, Any]], answers: Dict[int, str]) -> bool:
    """
    Saves an entire interview session and all its question evaluations in a single transaction.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Insert or replace Session summary
        cursor.execute("""
            INSERT OR REPLACE INTO interview_sessions (
                session_id, role, experience_level, category, total_score,
                max_possible_score, percentage, grade, tech_average,
                behavioral_average, duration_seconds, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            summary["session_id"],
            summary["role"],
            summary["experience_level"],
            summary["category"],
            summary["total_score"],
            summary["max_possible_score"],
            summary["percentage"],
            summary.get("grade", "N/A"),
            summary.get("tech_average", 0.0),
            summary.get("behavioral_average", 0.0),
            summary.get("duration_seconds", 0),
            summary["created_at"]
        ))

        # Delete any existing answers for this session (idempotent re-save)
        cursor.execute("DELETE FROM interview_answers WHERE session_id = ?", (summary["session_id"],))

        # Insert question evaluations
        for idx, q in enumerate(questions):
            ev = evaluations.get(idx, {})
            ans_text = answers.get(idx, "")

            cursor.execute("""
                INSERT INTO interview_answers (
                    session_id, question_index, question_id, question_type,
                    topic, question_text, candidate_answer, score,
                    relevance_level, relevance_pct, keywords_found_json,
                    missing_concepts_json, strengths_json, improvements_json,
                    suggested_answer, breakdown_json, word_count
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                summary["session_id"],
                idx,
                q.get("id", f"q_{idx}"),
                q.get("type", "technical"),
                q.get("topic", "General"),
                q.get("question", ""),
                ans_text,
                ev.get("score", 0.0),
                ev.get("relevance_level", "Unknown"),
                ev.get("relevance_pct", 0),
                json.dumps(ev.get("keywords_found", [])),
                json.dumps(ev.get("missing_concepts", [])),
                json.dumps(ev.get("strengths", [])),
                json.dumps(ev.get("areas_for_improvement", [])),
                ev.get("suggested_improved_answer", ""),
                json.dumps(ev.get("breakdown", {})),
                ev.get("word_count", 0)
            ))

        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"Error saving interview to SQLite: {e}")
        return False
    finally:
        conn.close()


def get_all_interviews() -> List[Dict[str, Any]]:
    """Retrieves all past interview sessions ordered by most recent first."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT session_id, role, experience_level, category, total_score,
               max_possible_score, percentage, grade, duration_seconds, created_at
        FROM interview_sessions
        ORDER BY id DESC
    """)
    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def get_interview_by_id(session_id: str) -> Optional[Dict[str, Any]]:
    """
    Retrieves a complete interview session including all questions and evaluations.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM interview_sessions WHERE session_id = ?", (session_id,))
    session_row = cursor.fetchone()

    if not session_row:
        conn.close()
        return None

    session_data = dict(session_row)

    cursor.execute("""
        SELECT * FROM interview_answers
        WHERE session_id = ?
        ORDER BY question_index ASC
    """, (session_id,))
    answer_rows = cursor.fetchall()
    conn.close()

    answers_list = []
    for r in answer_rows:
        item = dict(r)
        item["keywords_found"] = json.loads(item["keywords_found_json"]) if item.get("keywords_found_json") else []
        item["missing_concepts"] = json.loads(item["missing_concepts_json"]) if item.get("missing_concepts_json") else []
        item["strengths"] = json.loads(item["strengths_json"]) if item.get("strengths_json") else []
        item["areas_for_improvement"] = json.loads(item["improvements_json"]) if item.get("improvements_json") else []
        item["breakdown"] = json.loads(item["breakdown_json"]) if item.get("breakdown_json") else {}
        answers_list.append(item)

    session_data["questions_data"] = answers_list
    return session_data


def delete_interview(session_id: str) -> bool:
    """Deletes an interview session and its answers."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM interview_answers WHERE session_id = ?", (session_id,))
        cursor.execute("DELETE FROM interview_sessions WHERE session_id = ?", (session_id,))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"Error deleting interview: {e}")
        return False
    finally:
        conn.close()


def get_statistics() -> Dict[str, Any]:
    """Computes aggregate analytics over past interview performance."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) as total_count, AVG(percentage) as avg_score, MAX(percentage) as best_score FROM interview_sessions")
    stats = cursor.fetchone()

    total_count = stats["total_count"] if stats else 0
    avg_score = round(stats["avg_score"] or 0.0, 1) if stats else 0.0
    best_score = round(stats["best_score"] or 0.0, 1) if stats else 0.0

    # Top role practiced
    cursor.execute("SELECT role, COUNT(*) as count FROM interview_sessions GROUP BY role ORDER BY count DESC LIMIT 1")
    top_role_row = cursor.fetchone()
    top_role = top_role_row["role"] if top_role_row else "None yet"

    conn.close()

    return {
        "total_interviews": total_count,
        "average_score": avg_score,
        "best_score": best_score,
        "top_role": top_role
    }


# Auto-initialize database schema on module import
init_db()

