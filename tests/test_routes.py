import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import unittest
import tempfile
import os
import io
import json
from app import app
import database

class TestAppRoutes(unittest.TestCase):
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.temp_db.close()
        self.db_path = self.temp_db.name

        app.config["TESTING"] = True
        app.config["DATABASE_PATH"] = self.db_path
        self.client = app.test_client()
        database.init_db(self.db_path)

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_home_page_renders_successfully(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"AI LearnMate", response.data)
        self.assertIn(b"SDG 4 Quality Education", response.data)

    def test_create_session_page_renders(self):
        response = self.client.get("/create")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Create Learning Session", response.data)

    def test_create_session_empty_content_rejected(self):
        response = self.client.post("/create", data={
            "title": "Short Test",
            "subject": "CS",
            "source_type": "paste",
            "content": "Too small"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"too short", response.data.lower())

    def test_unsupported_file_upload_rejected(self):
        data = {
            "title": "File Test",
            "subject": "CS",
            "source_type": "file",
            "lecture_file": (io.BytesIO(b"binary data"), "test.exe")
        }
        response = self.client.post("/create", data=data, content_type="multipart/form-data", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"unsupported file format", response.data.lower())

    def test_demo_mode_workflow_and_quiz_submission(self):
        """End-to-end integration test: Demo mode launch -> quiz question -> answer submit -> report."""
        # 1. Launch Demo Mode
        create_res = self.client.post("/create", data={
            "is_demo": "1",
            "target_questions": "5"
        }, follow_redirects=False)
        self.assertEqual(create_res.status_code, 302)
        redirect_url = create_res.headers["Location"]
        self.assertIn("/quiz/", redirect_url)

        attempt_uuid = redirect_url.split("/quiz/")[-1]

        # 2. View Quiz Question
        quiz_res = self.client.get(f"/quiz/{attempt_uuid}")
        self.assertEqual(quiz_res.status_code, 200)
        self.assertIn(b"Question 1 of 5", quiz_res.data)

        # Retrieve the question ID from DB
        attempt = database.get_attempt_by_uuid(attempt_uuid, db_path=self.db_path)
        questions = database.get_questions_by_session_id(attempt["session_id"], db_path=self.db_path)
        first_q = questions[0]

        # 3. Submit an answer via API
        sub_res = self.client.post(
            f"/api/quiz/{attempt_uuid}/submit",
            data=json.dumps({
                "question_id": first_q["id"],
                "student_answer": first_q["correct_answer"]
            }),
            content_type="application/json"
        )
        self.assertEqual(sub_res.status_code, 200)
        res_data = sub_res.get_json()
        self.assertTrue(res_data["success"])
        self.assertTrue(res_data["is_correct"])

        # 4. View Progress History
        hist_res = self.client.get("/history")
        self.assertEqual(hist_res.status_code, 200)
        self.assertIn(b"Process Synchronization", hist_res.data)

    def test_create_session_paste_without_title_and_subject(self):
        """Verify that pasted notes create a valid session without user-provided title or subject."""
        sample_content = (
            "# Introduction to Computer Networks\n"
            "Computer networking refers to interconnected computing devices that can exchange data "
            "and share resources with each other. Network devices use communication protocols to transmit "
            "information over physical or wireless technologies. The OSI model defines seven layers."
        )
        sample_questions = [{
            "question": "What is the primary function of a network protocol?",
            "question_type": "mcq",
            "options": ["Exchange data", "Format hard drive", "Cool CPU", "Power on"],
            "correct_answer": "Exchange data",
            "explanation": "Protocols govern communication.",
            "topic": "Network Protocols",
            "difficulty": "Easy"
        }]

        from unittest.mock import patch
        with patch("app.generate_quiz_questions", return_value=sample_questions):
            res = self.client.post("/create", data={
                "source_type": "paste",
                "content": sample_content,
                "target_questions": "5"
            }, follow_redirects=False)

            self.assertEqual(res.status_code, 302)
            self.assertIn("/quiz/", res.headers["Location"])
            attempt_uuid = res.headers["Location"].split("/quiz/")[-1]

            attempt = database.get_attempt_by_uuid(attempt_uuid, db_path=self.db_path)
            session = database.get_session_by_uuid(attempt["session_id"], db_path=self.db_path)
            self.assertTrue(len(session["title"]) > 0)
            self.assertIn("Computer Networks", session["subject"])

    def test_create_session_youtube_without_title_and_subject(self):
        """Verify that YouTube URLs create a valid session without user-provided title or subject."""
        sample_questions = [{
            "question": "What is a packet?",
            "question_type": "mcq",
            "options": ["A unit of data", "A cable", "A screen", "A key"],
            "correct_answer": "A unit of data",
            "explanation": "Packets carry data.",
            "topic": "Packets",
            "difficulty": "Easy"
        }]
        yt_mock_res = {
            "success": True,
            "transcript": "In this video we will thoroughly discuss operating systems process scheduling, CPU bursts, round robin algorithms, priority scheduling, and context switching across threads.",
            "video_id": "test_video_123",
            "title": "Operating Systems: Process Scheduling Explained",
            "error": None
        }

        from unittest.mock import patch
        with patch("app.fetch_youtube_transcript", return_value=yt_mock_res), \
             patch("app.generate_quiz_questions", return_value=sample_questions):
            res = self.client.post("/create", data={
                "source_type": "youtube",
                "youtube_url": "https://www.youtube.com/watch?v=test_video_123",
                "target_questions": "5"
            }, follow_redirects=False)

            self.assertEqual(res.status_code, 302)
            self.assertIn("/quiz/", res.headers["Location"])
            attempt_uuid = res.headers["Location"].split("/quiz/")[-1]

            attempt = database.get_attempt_by_uuid(attempt_uuid, db_path=self.db_path)
            session = database.get_session_by_uuid(attempt["session_id"], db_path=self.db_path)
            self.assertEqual(session["title"], "Operating Systems: Process Scheduling Explained")
            self.assertEqual(session["subject"], "Operating Systems")

    def test_create_session_file_upload_without_title_and_subject(self):
        """Verify that file uploads create a valid session without user-provided title or subject."""
        sample_questions = [{
            "question": "What is SQL?",
            "question_type": "mcq",
            "options": ["Query language", "Hardware", "Router", "Cable"],
            "correct_answer": "Query language",
            "explanation": "Structured Query Language.",
            "topic": "SQL",
            "difficulty": "Easy"
        }]
        file_content = (
            "Database Systems Unit 2: Relational Databases and SQL Queries. "
            "A database management system stores tables with primary keys and foreign keys. "
            "Transactions follow ACID properties: Atomicity, Consistency, Isolation, Durability."
        )

        from unittest.mock import patch
        with patch("app.generate_quiz_questions", return_value=sample_questions):
            data = {
                "source_type": "file",
                "lecture_file": (io.BytesIO(file_content.encode("utf-8")), "database_management_notes.txt"),
                "target_questions": "5"
            }
            res = self.client.post("/create", data=data, content_type="multipart/form-data", follow_redirects=False)

            self.assertEqual(res.status_code, 302)
            self.assertIn("/quiz/", res.headers["Location"])
            attempt_uuid = res.headers["Location"].split("/quiz/")[-1]

            attempt = database.get_attempt_by_uuid(attempt_uuid, db_path=self.db_path)
            session = database.get_session_by_uuid(attempt["session_id"], db_path=self.db_path)
            self.assertIn("Database Management Notes", session["title"])
            self.assertEqual(session["subject"], "Database Systems")

if __name__ == "__main__":
    unittest.main()
