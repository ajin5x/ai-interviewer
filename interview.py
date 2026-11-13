"""
Interview session and question management module.
Responsible for selecting exactly 5 questions (3 Technical + 2 Behavioral)
from the local question bank, tracking interview progress, and orchestrating evaluations.
100% offline, zero external API.
"""

import random
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from config import (
    QUESTION_BANK,
    BEHAVIORAL_QUESTION_BANK,
    TECHNICAL_QUESTIONS_COUNT,
    BEHAVIORAL_QUESTIONS_COUNT,
    TOTAL_QUESTIONS_PER_INTERVIEW
)
from evaluation import RuleBasedEvaluationEngine


class InterviewSession:
    """
    Encapsulates a single interview session, including selected questions,
    candidate answers, and rule-based evaluation results.
    """

    def __init__(self, role: str, experience_level: str, category: str):
        self.session_id: str = str(uuid.uuid4())
        self.role: str = role
        self.experience_level: str = experience_level
        self.category: str = category
        self.created_at: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.start_timestamp: float = datetime.now().timestamp()
        self.completed_at: Optional[str] = None
        self.duration_seconds: int = 0

        # Generate exactly 5 questions
        self.questions: List[Dict[str, Any]] = self._generate_questions()
        self.current_index: int = 0
        self.answers: Dict[int, str] = {i: "" for i in range(len(self.questions))}
        self.evaluations: Dict[int, Dict[str, Any]] = {}
        self.is_completed: bool = False

    def _generate_questions(self) -> List[Dict[str, Any]]:
        """
        Extracts 3 technical questions for the chosen role and level,
        plus 2 behavioral/HR questions from the behavioral bank.
        Total = exactly 5 questions.
        """
        # 1. Fetch technical questions for the role & level
        role_data = QUESTION_BANK.get(self.role, {})
        level_data = role_data.get(self.experience_level, [])

        # Fallback to another level if current level has fewer than 3
        if len(level_data) < TECHNICAL_QUESTIONS_COUNT:
            combined = []
            for lvl_questions in role_data.values():
                combined.extend(lvl_questions)
            tech_candidates = combined
        else:
            tech_candidates = list(level_data)

        # Shuffle and pick 3 technical
        random.seed()
        if len(tech_candidates) >= TECHNICAL_QUESTIONS_COUNT:
            chosen_tech = random.sample(tech_candidates, TECHNICAL_QUESTIONS_COUNT)
        else:
            chosen_tech = tech_candidates[:TECHNICAL_QUESTIONS_COUNT]

        # 2. Pick 2 behavioral questions
        behavioral_candidates = list(BEHAVIORAL_QUESTION_BANK)
        if len(behavioral_candidates) >= BEHAVIORAL_QUESTIONS_COUNT:
            chosen_behavioral = random.sample(behavioral_candidates, BEHAVIORAL_QUESTIONS_COUNT)
        else:
            chosen_behavioral = behavioral_candidates[:BEHAVIORAL_QUESTIONS_COUNT]

        # Combine into exactly 5 questions (3 tech + 2 behavioral)
        questions = chosen_tech + chosen_behavioral

        # Ensure we return exactly TOTAL_QUESTIONS_PER_INTERVIEW
        if len(questions) < TOTAL_QUESTIONS_PER_INTERVIEW:
            # Pad from behavioral if necessary
            for b in BEHAVIORAL_QUESTION_BANK:
                if b not in questions:
                    questions.append(b)
                if len(questions) == TOTAL_QUESTIONS_PER_INTERVIEW:
                    break

        return questions[:TOTAL_QUESTIONS_PER_INTERVIEW]

    def record_answer(self, index: int, answer_text: str) -> None:
        """Stores the candidate's answer for a given question index."""
        if 0 <= index < len(self.questions):
            self.answers[index] = answer_text

    def evaluate_current_question(self, index: int) -> Dict[str, Any]:
        """Runs the rule-based evaluator for a single question."""
        if 0 <= index < len(self.questions):
            q_data = self.questions[index]
            ans_text = self.answers.get(index, "")
            eval_result = RuleBasedEvaluationEngine.evaluate_answer(q_data, ans_text)
            self.evaluations[index] = eval_result
            return eval_result
        return {}

    def finish_interview(self) -> Dict[str, Any]:
        """
        Evaluates all questions, marks interview completed,
        and computes cumulative summary statistics.
        """
        for i, q in enumerate(self.questions):
            if i not in self.evaluations:
                ans_text = self.answers.get(i, "")
                self.evaluations[i] = RuleBasedEvaluationEngine.evaluate_answer(q, ans_text)

        self.is_completed = True
        self.completed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.duration_seconds = int(datetime.now().timestamp() - self.start_timestamp)

        return self.get_summary()

    def get_summary(self) -> Dict[str, Any]:
        """Calculates total score, percentage, and category breakdown."""
        total_score = sum(ev.get("score", 0.0) for ev in self.evaluations.values())
        max_possible = len(self.questions) * 10.0
        pct = round((total_score / max_possible) * 100, 1) if max_possible > 0 else 0.0

        tech_scores = [
            self.evaluations[i]["score"]
            for i, q in enumerate(self.questions)
            if q.get("type") == "technical" and i in self.evaluations
        ]
        behavioral_scores = [
            self.evaluations[i]["score"]
            for i, q in enumerate(self.questions)
            if q.get("type") == "behavioral" and i in self.evaluations
        ]

        avg_tech = round(sum(tech_scores) / len(tech_scores), 1) if tech_scores else 0.0
        avg_behavioral = round(sum(behavioral_scores) / len(behavioral_scores), 1) if behavioral_scores else 0.0

        # Performance assessment band
        if pct >= 85:
            grade = "Excellent (Ready for Senior/Lead Offers)"
            color = "#10B981"
        elif pct >= 70:
            grade = "Strong (Competitive Candidate)"
            color = "#3B82F6"
        elif pct >= 50:
            grade = "Developing (Good Foundation, Needs Refinement)"
            color = "#F59E0B"
        else:
            grade = "Needs Practice (Review Recommended Concepts)"
            color = "#EF4444"

        return {
            "session_id": self.session_id,
            "role": self.role,
            "experience_level": self.experience_level,
            "category": self.category,
            "created_at": self.created_at,
            "duration_seconds": self.duration_seconds,
            "total_score": round(total_score, 1),
            "max_possible_score": max_possible,
            "percentage": pct,
            "grade": grade,
            "grade_color": color,
            "tech_average": avg_tech,
            "behavioral_average": avg_behavioral,
            "question_count": len(self.questions)
        }

