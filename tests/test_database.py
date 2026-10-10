import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import unittest
import tempfile
import os
import database

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.temp_db.close()
        self.db_path = self.temp_db.name
        database.init_db(self.db_path)

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_session_lifecycle(self):
        session_uuid = database.create_session(
            title="Operating Systems Deadlocks",
            subject="Computer Science",
            source_type="paste",
            source_content="Deadlock conditions include mutual exclusion, hold and wait, no preemption, and circular wait.",
            language="en",
            target_questions=5,
            is_demo=0,
            db_path=self.db_path
        )
        self.assertIsNotNone(session_uuid)

        session = database.get_session_by_uuid(session_uuid, db_path=self.db_path)
        self.assertIsNotNone(session)
        self.assertEqual(session["title"], "Operating Systems Deadlocks")
        self.assertEqual(session["target_questions"], 5)

    def test_save_and_retrieve_questions(self):
        session_uuid = database.create_session(
            title="Test Quiz",
            subject="OS",
            source_type="demo",
            source_content="Content",
            db_path=self.db_path
        )
        session = database.get_session_by_uuid(session_uuid, db_path=self.db_path)

        questions = [
            {
                "question": "What is a race condition?",
                "question_type": "mcq",
                "options": ["Bug", "Timing conflict", "CPU speed", "Memory leak"],
                "correct_answer": "Timing conflict",
                "explanation": "Concurrent access timing issue.",
                "topic": "Concurrency",
                "difficulty": "Easy"
            },
            {
                "question": "Define mutual exclusion.",
                "question_type": "short_answer",
                "options": [],
                "correct_answer": "Only one process can execute the critical section at a time.",
                "explanation": "Prevents conflicting updates.",
                "topic": "Critical Section",
                "difficulty": "Medium",
                "evaluation_rubric": "Must state only 1 process allowed in critical section."
            }
        ]

        database.save_questions(session["id"], questions, db_path=self.db_path)
        saved = database.get_questions_by_session_id(session["id"], db_path=self.db_path)
        self.assertEqual(len(saved), 2)
        self.assertEqual(saved[0]["question_type"], "mcq")
        self.assertEqual(len(saved[0]["options"]), 4)
        self.assertEqual(saved[1]["question_type"], "short_answer")

    def test_attempt_and_student_answers(self):
        session_uuid = database.create_session("OS", "CS", "paste", "Notes", db_path=self.db_path)
        session = database.get_session_by_uuid(session_uuid, db_path=self.db_path)
        database.save_questions(session["id"], [{
            "question": "Q1", "question_type": "mcq", "options": ["A", "B"], "correct_answer": "A",
            "explanation": "Exp", "topic": "T1", "difficulty": "Easy"
        }], db_path=self.db_path)
        
        saved_q = database.get_questions_by_session_id(session["id"], db_path=self.db_path)[0]
        attempt_uuid = database.create_attempt(session["id"], 5, db_path=self.db_path)
        attempt = database.get_attempt_by_uuid(attempt_uuid, db_path=self.db_path)
        self.assertEqual(attempt["current_difficulty"], "Medium")

        # Save student answer
        database.save_student_answer(
            attempt_id=attempt["id"],
            question_id=saved_q["id"],
            student_answer="A",
            is_correct=1,
            score_awarded=1.0,
            evaluation_feedback="Correct!",
            answered_difficulty="Easy",
            topic="T1",
            db_path=self.db_path
        )

        answers = database.get_student_answers_for_attempt(attempt["id"], db_path=self.db_path)
        self.assertEqual(len(answers), 1)
        self.assertEqual(answers[0]["student_answer"], "A")
        self.assertEqual(answers[0]["is_correct"], 1)

if __name__ == "__main__":
    unittest.main()
