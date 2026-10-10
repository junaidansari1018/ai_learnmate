import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import unittest
from quiz_engine import AdaptiveQuizEngine, MLStudentRiskPredictor

class TestQuizEngine(unittest.TestCase):
    def setUp(self):
        self.engine = AdaptiveQuizEngine()
        self.sample_questions = [
            {"id": 1, "topic": "Race Conditions", "difficulty": "Easy", "question_text": "Q1"},
            {"id": 2, "topic": "Race Conditions", "difficulty": "Medium", "question_text": "Q2"},
            {"id": 3, "topic": "Race Conditions", "difficulty": "Hard", "question_text": "Q3"},
            {"id": 4, "topic": "Semaphores", "difficulty": "Easy", "question_text": "Q4"},
            {"id": 5, "topic": "Semaphores", "difficulty": "Medium", "question_text": "Q5"},
            {"id": 6, "topic": "Semaphores", "difficulty": "Hard", "question_text": "Q6"},
            {"id": 7, "topic": "Deadlocks", "difficulty": "Easy", "question_text": "Q7"},
            {"id": 8, "topic": "Deadlocks", "difficulty": "Medium", "question_text": "Q8"},
            {"id": 9, "topic": "Deadlocks", "difficulty": "Hard", "question_text": "Q9"},
        ]

    def test_initial_state_defaults_to_medium(self):
        next_diff, rationale = self.engine.calculate_next_difficulty("Medium", [])
        self.assertEqual(next_diff, "Medium")
        self.assertIn("baseline", rationale.lower())

    def test_difficulty_increases_on_high_performance(self):
        # 3 out of 3 correct answers
        recent_answers = [
            {"is_correct": 1, "topic": "Race Conditions"},
            {"is_correct": 1, "topic": "Semaphores"},
            {"is_correct": 1, "topic": "Deadlocks"}
        ]
        next_diff, rationale = self.engine.calculate_next_difficulty("Medium", recent_answers)
        self.assertEqual(next_diff, "Hard")
        self.assertIn("increased", rationale.lower())

    def test_difficulty_decreases_on_struggling_window(self):
        # 0 out of 3 correct
        recent_answers = [
            {"is_correct": 0, "topic": "Race Conditions"},
            {"is_correct": 0, "topic": "Semaphores"},
            {"is_correct": 0, "topic": "Deadlocks"}
        ]
        next_diff, rationale = self.engine.calculate_next_difficulty("Medium", recent_answers)
        self.assertEqual(next_diff, "Easy")
        self.assertIn("reduced", rationale.lower())

    def test_remediation_on_specific_topic_failure(self):
        # If student fails question on Deadlocks, select remedial Deadlocks question
        recent_answers = [
            {"is_correct": 1, "topic": "Race Conditions"},
            {"is_correct": 0, "topic": "Deadlocks"}
        ]
        next_q, diff, rationale = self.engine.select_next_question(
            all_questions=self.sample_questions,
            answered_question_ids=[2, 8],
            recent_answers=recent_answers,
            current_difficulty="Medium"
        )
        self.assertIsNotNone(next_q)
        self.assertEqual(next_q["topic"], "Deadlocks")
        self.assertEqual(next_q["difficulty"], "Easy")
        self.assertIn("reinforcing", rationale.lower())

    def test_no_repeat_questions(self):
        answered_ids = [1, 2, 3, 4, 5, 6, 7, 8]
        next_q, diff, rationale = self.engine.select_next_question(
            all_questions=self.sample_questions,
            answered_question_ids=answered_ids,
            recent_answers=[],
            current_difficulty="Medium"
        )
        self.assertIsNotNone(next_q)
        self.assertEqual(next_q["id"], 9)
        self.assertNotIn(next_q["id"], answered_ids)

    def test_ml_remediation_predictor_output(self):
        pred = MLStudentRiskPredictor.predict_remediation_risk(
            recent_accuracy=0.0,
            topic_accuracy=0.2,
            topic_attempts=3,
            difficulty="Medium"
        )
        self.assertTrue(pred["needs_remediation"])
        self.assertIn("model_type", pred)

if __name__ == "__main__":
    unittest.main()
