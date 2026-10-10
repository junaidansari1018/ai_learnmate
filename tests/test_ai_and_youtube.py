import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import unittest
from ai_service import (
    extract_json_from_response,
    validate_question_structure,
    sanitize_lecture_content,
    evaluate_short_answer_rubric_fallback,
    AIValidationError,
    AIServiceError,
    generate_quiz_questions
)
from youtube_service import extract_video_id, fetch_youtube_transcript

class TestAIAndYouTubeServices(unittest.TestCase):
    def test_youtube_video_id_parsing(self):
        urls = [
            ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "dQw4w9WgXcQ"),
            ("https://youtu.be/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
            ("https://www.youtube.com/embed/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
            ("https://www.youtube.com/shorts/dQw4w9WgXcQ", "dQw4w9WgXcQ")
        ]
        for url, expected_id in urls:
            self.assertEqual(extract_video_id(url), expected_id)

    def test_youtube_invalid_url_fails_gracefully(self):
        res = fetch_youtube_transcript("https://invalid-domain.com/not-youtube")
        self.assertFalse(res["success"])
        self.assertIn("invalid", res["error"].lower())

    def test_short_content_raises_value_error(self):
        with self.assertRaises(ValueError):
            generate_quiz_questions("Too short", target_count=5)

    def test_extract_json_from_markdown_fences(self):
        raw_llm_output = """Here are the questions:
```json
[
  {
    "question": "What is a Mutex?",
    "question_type": "mcq",
    "options": ["A lock", "A file", "A port", "A socket"],
    "correct_answer": "A lock",
    "explanation": "Mutual exclusion lock.",
    "topic": "Synchronization",
    "difficulty": "Easy"
  }
]
```
Hope this helps!"""
        parsed = extract_json_from_response(raw_llm_output)
        self.assertIsInstance(parsed, list)
        self.assertEqual(len(parsed), 1)
        self.assertEqual(parsed[0]["question"], "What is a Mutex?")

    def test_validate_question_structure_normalizes_data(self):
        raw_q = {
            "question": "Explain Peterson's algorithm?",
            "question_type": "short_answer",
            "correct_answer": "Software-based critical section solution for two processes.",
            "topic": "Process Synchronization",
            "difficulty": "hard"
        }
        val = validate_question_structure(raw_q)
        self.assertEqual(val["difficulty"], "Hard")
        self.assertEqual(val["question_type"], "short_answer")

    def test_short_answer_evaluator_accepts_equivalent_wording(self):
        """Case 7: Evaluator accepts equivalent concept without requiring exact string match."""
        reference = "Bounded waiting sets a limit on other processes entering the critical section to prevent starvation."
        rubric = "Must mention bound/limit on entry and preventing starvation."

        # Student uses alternative phrasing and synonyms:
        student_ans = "It means there is a finite limit on how many times other processes can enter, ensuring no process starves."
        is_corr, score, feedback = evaluate_short_answer_rubric_fallback(
            student_answer=student_ans,
            reference_answer=reference,
            rubric=rubric
        )
        self.assertTrue(is_corr)
        self.assertGreaterEqual(score, 0.7)
        self.assertIn("conceptually correct", feedback.lower())

    def test_short_answer_evaluator_rejects_irrelevant_answer(self):
        reference = "Bounded waiting prevents starvation."
        student_ans = "A compiler optimizes loops in C++."
        is_corr, score, feedback = evaluate_short_answer_rubric_fallback(
            student_answer=student_ans,
            reference_answer=reference,
            rubric="Prevents starvation"
        )
        self.assertFalse(is_corr)
        self.assertEqual(score, 0.0)

if __name__ == "__main__":
    unittest.main()
