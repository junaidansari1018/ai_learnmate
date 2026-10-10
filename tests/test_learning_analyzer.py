import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import unittest
from learning_analyzer import LearningAnalyzer

class TestLearningAnalyzer(unittest.TestCase):
    def test_single_question_marked_as_limited_evidence(self):
        """Case 10: One-question topics are NOT labeled as definitively mastered."""
        answers = [
            {
                "topic": "Process Scheduling",
                "is_correct": 1,
                "score_awarded": 1.0,
                "question_text": "What is Round Robin?",
                "student_answer": "Time sliced scheduling",
                "correct_answer": "Time sliced scheduling",
                "explanation": "RR uses time slices."
            }
        ]
        report = LearningAnalyzer.analyze_attempt(answers, total_questions=5)
        self.assertEqual(len(report["topic_breakdown"]), 1)
        tb = report["topic_breakdown"][0]
        self.assertEqual(tb["mastery_level"], "Limited Evidence")
        self.assertIn("limited evidence", tb["evidence_note"].lower())
        self.assertEqual(len(report["strong_topics"]), 0) # Must not be labeled strong on 1 question!

    def test_multi_question_mastery_classification(self):
        """Case 9: Topic performance calculations and thresholds."""
        answers = [
            # Topic A: 3 attempts, 3 correct (100%) -> Strong
            {"topic": "Semaphores", "is_correct": 1, "score_awarded": 1.0, "question_text": "Q1", "student_answer": "A", "correct_answer": "A", "explanation": "E"},
            {"topic": "Semaphores", "is_correct": 1, "score_awarded": 1.0, "question_text": "Q2", "student_answer": "B", "correct_answer": "B", "explanation": "E"},
            {"topic": "Semaphores", "is_correct": 1, "score_awarded": 1.0, "question_text": "Q3", "student_answer": "C", "correct_answer": "C", "explanation": "E"},
            # Topic B: 3 attempts, 0 correct (0%) -> Needs revision
            {"topic": "Deadlocks", "is_correct": 0, "score_awarded": 0.0, "question_text": "Q4", "student_answer": "Wrong", "correct_answer": "Right", "explanation": "Deadlock rule"},
            {"topic": "Deadlocks", "is_correct": 0, "score_awarded": 0.0, "question_text": "Q5", "student_answer": "Wrong2", "correct_answer": "Right2", "explanation": "Banker algo"},
            {"topic": "Deadlocks", "is_correct": 0, "score_awarded": 0.0, "question_text": "Q6", "student_answer": "Wrong3", "correct_answer": "Right3", "explanation": "Resource graph"},
        ]
        report = LearningAnalyzer.analyze_attempt(answers, total_questions=6)
        
        self.assertEqual(report["overall_percentage"], 50.0)
        self.assertEqual(report["total_correct"], 3)
        self.assertEqual(report["total_incorrect"], 3)

        # Semaphores should be Strong
        sem_item = next(t for t in report["topic_breakdown"] if t["topic"] == "Semaphores")
        self.assertEqual(sem_item["mastery_level"], "Strong understanding")

        # Deadlocks should be Needs revision
        dead_item = next(t for t in report["topic_breakdown"] if t["topic"] == "Deadlocks")
        self.assertEqual(dead_item["mastery_level"], "Needs revision")

        # Recommendations should focus on Deadlocks
        self.assertTrue(any("Deadlocks" in r["topic"] for r in report["actionable_recommendations"]))
        self.assertTrue(len(report["misconception_patterns"]) == 3)

if __name__ == "__main__":
    unittest.main()
