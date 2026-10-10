import sqlite3
import json
import uuid
from typing import List, Dict, Any, Optional
from config import Config

def get_db_connection(db_path: Optional[str] = None) -> sqlite3.Connection:
    """Creates a database connection with row factory and foreign keys enabled."""
    path = db_path or Config.DATABASE_PATH
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db(db_path: Optional[str] = None):
    """Initializes the database schema with parameterized setup."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()

    # 1. Learning Sessions table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS learning_sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_uuid TEXT UNIQUE NOT NULL,
        title TEXT NOT NULL,
        subject TEXT NOT NULL,
        source_type TEXT NOT NULL,
        source_content TEXT NOT NULL,
        language TEXT NOT NULL DEFAULT 'en',
        target_questions INTEGER NOT NULL DEFAULT 10,
        is_demo INTEGER NOT NULL DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status TEXT NOT NULL DEFAULT 'created'
    );
    """)

    # 2. Quiz Questions table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS quiz_questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id INTEGER NOT NULL,
        question_text TEXT NOT NULL,
        question_type TEXT NOT NULL, -- 'mcq' or 'short_answer'
        options_json TEXT,          -- JSON serialized list for MCQ
        correct_answer TEXT NOT NULL,
        explanation TEXT NOT NULL,
        topic TEXT NOT NULL,
        difficulty TEXT NOT NULL,    -- 'Easy', 'Medium', 'Hard'
        evaluation_rubric TEXT,
        order_index INTEGER DEFAULT 0,
        FOREIGN KEY (session_id) REFERENCES learning_sessions(id) ON DELETE CASCADE
    );
    """)

    # 3. Quiz Attempts table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS quiz_attempts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        attempt_uuid TEXT UNIQUE NOT NULL,
        session_id INTEGER NOT NULL,
        current_question_index INTEGER DEFAULT 0,
        total_questions_planned INTEGER NOT NULL,
        score REAL DEFAULT 0.0,
        total_answered INTEGER DEFAULT 0,
        total_correct INTEGER DEFAULT 0,
        current_difficulty TEXT DEFAULT 'Medium',
        is_completed INTEGER DEFAULT 0,
        started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        completed_at TIMESTAMP,
        FOREIGN KEY (session_id) REFERENCES learning_sessions(id) ON DELETE CASCADE
    );
    """)

    # 4. Student Answers table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS student_answers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        attempt_id INTEGER NOT NULL,
        question_id INTEGER NOT NULL,
        student_answer TEXT NOT NULL,
        is_correct INTEGER NOT NULL, -- 1 for correct, 0 for incorrect
        score_awarded REAL DEFAULT 0.0,
        evaluation_feedback TEXT NOT NULL,
        answered_difficulty TEXT NOT NULL,
        topic TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (attempt_id) REFERENCES quiz_attempts(id) ON DELETE CASCADE,
        FOREIGN KEY (question_id) REFERENCES quiz_questions(id) ON DELETE CASCADE
    );
    """)

    # 5. Topic Performance table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS topic_performance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        attempt_id INTEGER NOT NULL,
        topic TEXT NOT NULL,
        questions_attempted INTEGER DEFAULT 0,
        questions_correct INTEGER DEFAULT 0,
        accuracy_percentage REAL DEFAULT 0.0,
        mastery_level TEXT NOT NULL, -- 'Strong understanding', 'Developing understanding', 'Needs revision', 'Limited Evidence'
        needs_revision INTEGER DEFAULT 0,
        misconceptions_identified TEXT,
        FOREIGN KEY (attempt_id) REFERENCES quiz_attempts(id) ON DELETE CASCADE
    );
    """)

    # Indexes for fast lookup
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_sessions_uuid ON learning_sessions(session_uuid);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_questions_session ON quiz_questions(session_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_attempts_uuid ON quiz_attempts(attempt_uuid);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_answers_attempt ON student_answers(attempt_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_topic_perf_attempt ON topic_performance(attempt_id);")

    conn.commit()
    conn.close()

# ----------------- CRUD Operations -----------------

def create_session(
    title: str = "Lecture Assessment",
    subject: str = "General",
    source_type: str = "paste",
    source_content: str = "",
    language: str = "en",
    target_questions: int = 10,
    is_demo: int = 0,
    db_path: Optional[str] = None
) -> str:
    """Inserts a new learning session and returns its unique UUID."""
    session_uuid = str(uuid.uuid4())
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    safe_title = (title or "Lecture Assessment").strip()
    safe_subject = (subject or "General").strip()
    cursor.execute(
        """
        INSERT INTO learning_sessions 
        (session_uuid, title, subject, source_type, source_content, language, target_questions, is_demo)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (session_uuid, safe_title, safe_subject, source_type, source_content, language, target_questions, is_demo)
    )
    conn.commit()
    conn.close()
    return session_uuid

def get_session_by_uuid(session_uuid: Any, db_path: Optional[str] = None) -> Optional[sqlite3.Row]:
    """Retrieves session record by session_uuid (or integer id)."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    if isinstance(session_uuid, int) or (isinstance(session_uuid, str) and session_uuid.isdigit()):
        cursor.execute("SELECT * FROM learning_sessions WHERE id = ?", (int(session_uuid),))
    else:
        cursor.execute("SELECT * FROM learning_sessions WHERE session_uuid = ?", (str(session_uuid),))
    row = cursor.fetchone()
    conn.close()
    return row

def get_session_by_id(session_id: int, db_path: Optional[str] = None) -> Optional[sqlite3.Row]:
    """Retrieves session record by integer primary key id."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM learning_sessions WHERE id = ?", (int(session_id),))
    row = cursor.fetchone()
    conn.close()
    return row

def save_questions(session_id: int, questions: List[Dict[str, Any]], db_path: Optional[str] = None):
    """Saves generated questions associated with a session."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    for idx, q in enumerate(questions):
        options = json.dumps(q.get("options", [])) if q.get("options") else None
        cursor.execute(
            """
            INSERT INTO quiz_questions
            (session_id, question_text, question_type, options_json, correct_answer, 
             explanation, topic, difficulty, evaluation_rubric, order_index)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                session_id,
                q.get("question", "").strip(),
                q.get("question_type", "mcq"),
                options,
                q.get("correct_answer", "").strip(),
                q.get("explanation", "").strip(),
                q.get("topic", "General").strip(),
                q.get("difficulty", "Medium").strip().capitalize(),
                q.get("evaluation_rubric", ""),
                idx
            )
        )
    conn.commit()
    conn.close()

def get_questions_by_session_id(session_id: int, db_path: Optional[str] = None) -> List[Dict[str, Any]]:
    """Fetches all questions for a given session."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM quiz_questions WHERE session_id = ? ORDER BY order_index ASC", (session_id,))
    rows = cursor.fetchall()
    conn.close()
    
    questions = []
    for r in rows:
        q_dict = dict(r)
        if q_dict.get("options_json"):
            try:
                q_dict["options"] = json.loads(q_dict["options_json"])
            except Exception:
                q_dict["options"] = []
        else:
            q_dict["options"] = []
        questions.append(q_dict)
    return questions

def create_attempt(session_id: int, total_questions: int, db_path: Optional[str] = None) -> str:
    """Initializes a new quiz attempt for a session and returns its attempt_uuid."""
    attempt_uuid = str(uuid.uuid4())
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO quiz_attempts
        (attempt_uuid, session_id, total_questions_planned, current_difficulty)
        VALUES (?, ?, ?, 'Medium')
        """,
        (attempt_uuid, session_id, total_questions)
    )
    conn.commit()
    conn.close()
    return attempt_uuid

def get_attempt_by_uuid(attempt_uuid: str, db_path: Optional[str] = None) -> Optional[sqlite3.Row]:
    """Retrieves attempt record by attempt_uuid."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM quiz_attempts WHERE attempt_uuid = ?", (attempt_uuid,))
    row = cursor.fetchone()
    conn.close()
    return row

def save_student_answer(
    attempt_id: int,
    question_id: int,
    student_answer: str,
    is_correct: int,
    score_awarded: float,
    evaluation_feedback: str,
    answered_difficulty: str,
    topic: str,
    db_path: Optional[str] = None
):
    """Records an individual question answer from the student."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO student_answers
        (attempt_id, question_id, student_answer, is_correct, score_awarded, 
         evaluation_feedback, answered_difficulty, topic)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            attempt_id,
            question_id,
            student_answer.strip(),
            is_correct,
            score_awarded,
            evaluation_feedback.strip(),
            answered_difficulty,
            topic
        )
    )
    conn.commit()
    conn.close()

def get_student_answers_for_attempt(attempt_id: int, db_path: Optional[str] = None) -> List[Dict[str, Any]]:
    """Gets all submitted answers for an attempt joined with question details."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT sa.*, qq.question_text, qq.question_type, qq.options_json, 
               qq.correct_answer, qq.explanation, qq.evaluation_rubric
        FROM student_answers sa
        JOIN quiz_questions qq ON sa.question_id = qq.id
        WHERE sa.attempt_id = ?
        ORDER BY sa.id ASC
        """,
        (attempt_id,)
    )
    rows = cursor.fetchall()
    conn.close()
    
    results = []
    for r in rows:
        d = dict(r)
        if d.get("options_json"):
            try:
                d["options"] = json.loads(d["options_json"])
            except Exception:
                d["options"] = []
        results.append(d)
    return results

def update_attempt_progress(
    attempt_id: int,
    score: float,
    total_answered: int,
    total_correct: int,
    next_difficulty: str,
    is_completed: int = 0,
    db_path: Optional[str] = None
):
    """Updates attempt running score and completion state."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    if is_completed:
        cursor.execute(
            """
            UPDATE quiz_attempts
            SET score = ?, total_answered = ?, total_correct = ?, 
                current_difficulty = ?, is_completed = 1, completed_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (score, total_answered, total_correct, next_difficulty, attempt_id)
        )
    else:
        cursor.execute(
            """
            UPDATE quiz_attempts
            SET score = ?, total_answered = ?, total_correct = ?, 
                current_difficulty = ?, current_question_index = current_question_index + 1
            WHERE id = ?
            """,
            (score, total_answered, total_correct, next_difficulty, attempt_id)
        )
    conn.commit()
    conn.close()

def save_topic_performances(attempt_id: int, topic_stats: List[Dict[str, Any]], db_path: Optional[str] = None):
    """Saves computed topic mastery records for the attempt."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    # Remove any existing stats for this attempt to avoid duplicates
    cursor.execute("DELETE FROM topic_performance WHERE attempt_id = ?", (attempt_id,))
    for stat in topic_stats:
        cursor.execute(
            """
            INSERT INTO topic_performance
            (attempt_id, topic, questions_attempted, questions_correct, accuracy_percentage, 
             mastery_level, needs_revision, misconceptions_identified)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                attempt_id,
                stat["topic"],
                stat["questions_attempted"],
                stat["questions_correct"],
                stat["accuracy_percentage"],
                stat["mastery_level"],
                stat.get("needs_revision", 0),
                json.dumps(stat.get("misconceptions", []))
            )
        )
    conn.commit()
    conn.close()

def get_topic_performances_for_attempt(attempt_id: int, db_path: Optional[str] = None) -> List[Dict[str, Any]]:
    """Retrieves saved topic performance analytics for an attempt."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM topic_performance WHERE attempt_id = ? ORDER BY accuracy_percentage ASC", (attempt_id,))
    rows = cursor.fetchall()
    conn.close()
    
    results = []
    for r in rows:
        d = dict(r)
        if d.get("misconceptions_identified"):
            try:
                d["misconceptions"] = json.loads(d["misconceptions_identified"])
            except Exception:
                d["misconceptions"] = []
        else:
            d["misconceptions"] = []
        results.append(d)
    return results

def get_all_attempts_history(db_path: Optional[str] = None) -> List[Dict[str, Any]]:
    """Fetches all quiz attempts with session details for progress history."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT qa.*, ls.title, ls.subject, ls.language, ls.is_demo, ls.session_uuid
        FROM quiz_attempts qa
        JOIN learning_sessions ls ON qa.session_id = ls.id
        ORDER BY qa.started_at DESC
        """
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]
