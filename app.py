import os
import re
import uuid
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, abort
from config import Config
import database
from demo_data import DEMO_LECTURE, get_demo_questions
from ai_service import generate_quiz_questions, evaluate_short_answer, AIServiceError, AIValidationError
from youtube_service import fetch_youtube_transcript
from quiz_engine import AdaptiveQuizEngine, MLStudentRiskPredictor
from learning_analyzer import LearningAnalyzer

app = Flask(__name__)
app.config.from_object(Config)

# Ensure database is initialized on startup
with app.app_context():
    database.init_db()

@app.errorhandler(413)
def request_entity_too_large(error):
    return render_template(
        "error.html",
        title="File Too Large",
        message="The uploaded file exceeds the 2MB size limit. Please upload a smaller text file or paste the text directly."
    ), 413

@app.errorhandler(404)
def not_found_error(error):
    return render_template(
        "error.html",
        title="Page Not Found",
        message="The requested resource or session was not found."
    ), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template(
        "error.html",
        title="Unexpected Error",
        message="An unexpected system error occurred. Please try again or switch to Demo Mode."
    ), 500

# ----------------- Navigation Routes -----------------

@app.route("/")
def index():
    """Landing page introducing AI LearnMate, SDG 4 alignment, and 4-step workflow."""
    return render_template("index.html")

def derive_title_and_subject(content: str, source_type: str, custom_title: str = "", custom_subject: str = "") -> tuple:
    """
    Derives an informative title and subject from content and source metadata
    without requiring user input on the frontend.
    """
    derived_title = custom_title.strip() if custom_title else ""
    derived_subject = custom_subject.strip() if custom_subject else ""

    clean_content = (content or "").strip()

    # If title not provided, derive from content snippet
    if not derived_title and clean_content:
        first_line = clean_content.splitlines()[0].strip()
        first_line = re.sub(r'^[#*_\-\s]+', '', first_line).strip()
        if 5 <= len(first_line) <= 70 and not first_line.endswith(('.', '?', '!')):
            derived_title = first_line
        else:
            words = clean_content.split()[:7]
            snippet = " ".join(words)
            if len(snippet) > 40:
                snippet = snippet[:40].rsplit(' ', 1)[0]
            derived_title = f"Lecture: {snippet}" if snippet else "Lecture Assessment"

    if not derived_title:
        derived_title = "Lecture Assessment"

    # If subject not provided, infer domain from content keywords
    if not derived_subject:
        lower_content = clean_content.lower()[:3000]
        if any(k in lower_content for k in ["process", "thread", "cpu", "memory", "deadlock", "semaphore", "kernel", "operating system"]):
            derived_subject = "Operating Systems"
        elif any(k in lower_content for k in ["packet", "ip address", "tcp", "udp", "routing", "network", "osi layer"]):
            derived_subject = "Computer Networks"
        elif any(k in lower_content for k in ["sql", "database", "rdbms", "query", "schema", "table", "transaction"]):
            derived_subject = "Database Systems"
        elif any(k in lower_content for k in ["algorithm", "complexity", "graph", "binary search", "sorting", "data structure"]):
            derived_subject = "Data Structures & Algorithms"
        elif any(k in lower_content for k in ["class", "object", "inheritance", "polymorphism", "encapsulation", "java", "python"]):
            derived_subject = "Software Engineering"
        else:
            derived_subject = "Engineering & Science"

    return derived_title, derived_subject

@app.route("/create", methods=["GET", "POST"])
def create_session():
    """Form to create a learning session via YouTube, paste, file upload, or Demo Mode."""
    if request.method == "GET":
        return render_template("create_session.html", min_chars=Config.MIN_CONTENT_CHARS)

    # Process submission
    source_type = request.form.get("source_type", "paste").strip()
    language = request.form.get("language", "en").strip()
    is_demo_req = request.form.get("is_demo") == "1"
    
    try:
        target_questions = int(request.form.get("target_questions", 10))
        if target_questions not in [5, 10, 15]:
            target_questions = 10
    except ValueError:
        target_questions = 10

    # 1. Handle Demo Mode Immediately
    if is_demo_req or source_type == "demo":
        title = DEMO_LECTURE["title"]
        subject = DEMO_LECTURE["subject"]
        content = DEMO_LECTURE["content"]
        session_uuid = database.create_session(
            title=title,
            subject=subject,
            source_type="demo",
            source_content=content,
            language=language,
            target_questions=target_questions,
            is_demo=1,
            db_path=app.config.get("DATABASE_PATH")
        )
        session = database.get_session_by_uuid(session_uuid, db_path=app.config.get("DATABASE_PATH"))
        demo_qs = get_demo_questions(language=language, limit=target_questions)
        database.save_questions(session["id"], demo_qs, db_path=app.config.get("DATABASE_PATH"))
        attempt_uuid = database.create_attempt(session["id"], len(demo_qs), db_path=app.config.get("DATABASE_PATH"))
        return redirect(url_for("take_quiz", attempt_uuid=attempt_uuid))

    content = ""
    suggested_title = ""

    # 2. Handle YouTube URL
    if source_type == "youtube":
        youtube_url = request.form.get("youtube_url", "").strip()
        if not youtube_url:
            flash("Please provide a valid YouTube video URL.", "error")
            return render_template("create_session.html", min_chars=Config.MIN_CONTENT_CHARS, source_type="youtube")

        yt_result = fetch_youtube_transcript(youtube_url)
        if not yt_result["success"]:
            flash(yt_result["error"], "error")
            return render_template(
                "create_session.html",
                min_chars=Config.MIN_CONTENT_CHARS,
                youtube_url=youtube_url,
                suggest_paste=True
            )
        content = yt_result["transcript"]
        suggested_title = yt_result.get("title") or "YouTube Video Lecture"

    # 3. Handle File Upload
    elif source_type == "file":
        uploaded_file = request.files.get("lecture_file")
        if not uploaded_file or uploaded_file.filename == "":
            flash("Please select a text file (.txt, .md, .vtt, .srt) to upload.", "error")
            return render_template("create_session.html", min_chars=Config.MIN_CONTENT_CHARS, source_type="file")

        ext = uploaded_file.filename.rsplit(".", 1)[-1].lower() if "." in uploaded_file.filename else ""
        if ext not in Config.ALLOWED_EXTENSIONS:
            flash(f"Unsupported file format '.{ext}'. Supported formats: {', '.join(Config.ALLOWED_EXTENSIONS)}", "error")
            return render_template("create_session.html", min_chars=Config.MIN_CONTENT_CHARS, source_type="file")

        try:
            raw_bytes = uploaded_file.read()
            content = raw_bytes.decode("utf-8", errors="replace").strip()
            name_base = uploaded_file.filename.rsplit(".", 1)[0]
            suggested_title = re.sub(r'[-_]+', ' ', name_base).strip().title()
        except Exception as e:
            flash(f"Failed to read file: {str(e)}", "error")
            return render_template("create_session.html", min_chars=Config.MIN_CONTENT_CHARS, source_type="file")

    # 4. Handle Direct Paste
    else:
        content = request.form.get("content", "").strip()

    # Validate content length
    if len(content) < Config.MIN_CONTENT_CHARS:
        flash(
            f"The lecture material is too short ({len(content)} characters). "
            f"Please provide at least {Config.MIN_CONTENT_CHARS} characters of notes or transcript.",
            "error"
        )
        return render_template(
            "create_session.html",
            min_chars=Config.MIN_CONTENT_CHARS,
            content=content,
            source_type=source_type
        )

    # Derive safe title & subject internally
    title, subject = derive_title_and_subject(content, source_type, custom_title=suggested_title)

    # Attempt AI Quiz Generation
    try:
        session_uuid = database.create_session(
            title=title,
            subject=subject,
            source_type=source_type,
            source_content=content,
            language=language,
            target_questions=target_questions,
            is_demo=0,
            db_path=app.config.get("DATABASE_PATH")
        )
        session = database.get_session_by_uuid(session_uuid, db_path=app.config.get("DATABASE_PATH"))

        # Generate questions via AI service
        generated_questions = generate_quiz_questions(
            lecture_content=content,
            subject=subject,
            language=language,
            target_count=target_questions
        )

        database.save_questions(session["id"], generated_questions, db_path=app.config.get("DATABASE_PATH"))
        attempt_uuid = database.create_attempt(session["id"], len(generated_questions), db_path=app.config.get("DATABASE_PATH"))
        return redirect(url_for("take_quiz", attempt_uuid=attempt_uuid))

    except (AIServiceError, AIValidationError, ValueError) as err:
        flash(f"AI Generation Notice: {str(err)}", "error")
        return render_template(
            "create_session.html",
            min_chars=Config.MIN_CONTENT_CHARS,
            content=content,
            source_type=source_type,
            show_demo_fallback=True
        )

# ----------------- Quiz Interaction Routes -----------------

@app.route("/quiz/<attempt_uuid>")
def take_quiz(attempt_uuid: str):
    """Renders the single-question assessment screen with adaptive difficulty."""
    db_path = app.config.get("DATABASE_PATH")
    attempt = database.get_attempt_by_uuid(attempt_uuid, db_path=db_path)
    if not attempt:
        abort(404)

    if attempt["is_completed"]:
        return redirect(url_for("view_report", attempt_uuid=attempt_uuid))

    session = database.get_session_by_uuid(attempt["session_id"], db_path=db_path)
    all_questions = database.get_questions_by_session_id(attempt["session_id"], db_path=db_path)
    answered_records = database.get_student_answers_for_attempt(attempt["id"], db_path=db_path)
    answered_ids = [r["question_id"] for r in answered_records]

    # Check if target question count reached or no more questions
    if len(answered_records) >= attempt["total_questions_planned"] or len(answered_ids) >= len(all_questions):
        # Finalize attempt
        total_corr = sum(1 for a in answered_records if a["is_correct"] == 1)
        score = sum(float(a["score_awarded"]) for a in answered_records)
        database.update_attempt_progress(
            attempt_id=attempt["id"],
            score=score,
            total_answered=len(answered_records),
            total_correct=total_corr,
            next_difficulty=attempt["current_difficulty"],
            is_completed=1,
            db_path=db_path
        )
        # Compute and persist topic performance
        analysis = LearningAnalyzer.analyze_attempt(answered_records, attempt["total_questions_planned"])
        database.save_topic_performances(attempt["id"], analysis["topic_breakdown"], db_path=db_path)
        return redirect(url_for("view_report", attempt_uuid=attempt_uuid))

    # Adaptively pick next question
    next_q, target_diff, rationale = AdaptiveQuizEngine.select_next_question(
        all_questions=all_questions,
        answered_question_ids=answered_ids,
        recent_answers=answered_records,
        current_difficulty=attempt["current_difficulty"]
    )

    if not next_q:
        # No more available questions
        return redirect(url_for("view_report", attempt_uuid=attempt_uuid))

    current_question_num = len(answered_records) + 1
    total_planned = attempt["total_questions_planned"]
    progress_percentage = int(((current_question_num - 1) / total_planned) * 100)

    return render_template(
        "quiz.html",
        attempt=attempt,
        session=session,
        question=next_q,
        question_num=current_question_num,
        total_questions=total_planned,
        progress_percentage=progress_percentage,
        target_diff=target_diff,
        rationale=rationale
    )

@app.route("/api/quiz/<attempt_uuid>/submit", methods=["POST"])
def submit_answer(attempt_uuid: str):
    """Evaluates an submitted answer, records score, and returns adaptive next state."""
    db_path = app.config.get("DATABASE_PATH")
    attempt = database.get_attempt_by_uuid(attempt_uuid, db_path=db_path)
    if not attempt or attempt["is_completed"]:
        return jsonify({"success": False, "error": "Attempt is not active."}), 400

    data = request.get_json(silent=True) or {}
    question_id = data.get("question_id")
    student_ans = str(data.get("student_answer", "")).strip()

    if not question_id:
        return jsonify({"success": False, "error": "Missing question ID."}), 400

    # Retrieve the question
    all_qs = database.get_questions_by_session_id(attempt["session_id"], db_path=db_path)
    target_q = next((q for q in all_qs if q["id"] == int(question_id)), None)
    if not target_q:
        return jsonify({"success": False, "error": "Question not found."}), 404

    is_correct = False
    score_awarded = 0.0
    feedback = ""

    if target_q["question_type"] == "mcq":
        # MCQ Evaluation
        ref = target_q["correct_answer"].strip().lower()
        sub = student_ans.strip().lower()
        if ref == sub:
            is_correct = True
            score_awarded = 1.0
            feedback = "Correct! " + target_q["explanation"]
        else:
            is_correct = False
            score_awarded = 0.0
            feedback = f"Incorrect. The correct option is '{target_q['correct_answer']}'. {target_q['explanation']}"
    else:
        # Short Answer Evaluation
        is_correct, score_awarded, feedback = evaluate_short_answer(
            question_text=target_q["question_text"],
            student_answer=student_ans,
            reference_answer=target_q["correct_answer"],
            rubric=target_q.get("evaluation_rubric", "")
        )

    # Save student response
    database.save_student_answer(
        attempt_id=attempt["id"],
        question_id=target_q["id"],
        student_answer=student_ans,
        is_correct=1 if is_correct else 0,
        score_awarded=score_awarded,
        evaluation_feedback=feedback,
        answered_difficulty=target_q["difficulty"],
        topic=target_q["topic"],
        db_path=db_path
    )

    # Fetch updated history of answers to calculate next adaptive difficulty
    answered_records = database.get_student_answers_for_attempt(attempt["id"], db_path=db_path)
    next_diff, diff_rationale = AdaptiveQuizEngine.calculate_next_difficulty(
        current_difficulty=attempt["current_difficulty"],
        recent_answers=answered_records
    )

    # Update attempt record
    current_answered = len(answered_records)
    current_correct = sum(1 for a in answered_records if a["is_correct"] == 1)
    current_score = sum(float(a["score_awarded"]) for a in answered_records)
    is_completed = current_answered >= attempt["total_questions_planned"]

    database.update_attempt_progress(
        attempt_id=attempt["id"],
        score=current_score,
        total_answered=current_answered,
        total_correct=current_correct,
        next_difficulty=next_diff,
        is_completed=1 if is_completed else 0,
        db_path=db_path
    )

    if is_completed:
        # Generate learning analysis on completion
        analysis = LearningAnalyzer.analyze_attempt(answered_records, attempt["total_questions_planned"])
        database.save_topic_performances(attempt["id"], analysis["topic_breakdown"], db_path=db_path)

    return jsonify({
        "success": True,
        "is_correct": is_correct,
        "score_awarded": score_awarded,
        "correct_answer": target_q["correct_answer"],
        "explanation": target_q["explanation"],
        "feedback": feedback,
        "next_difficulty": next_diff,
        "diff_rationale": diff_rationale,
        "is_completed": is_completed,
        "report_url": url_for("view_report", attempt_uuid=attempt_uuid)
    })

# ----------------- Learning Report & History Routes -----------------

@app.route("/report/<attempt_uuid>")
def view_report(attempt_uuid: str):
    """Detailed Learning Gap and Topic Mastery Report."""
    db_path = app.config.get("DATABASE_PATH")
    attempt = database.get_attempt_by_uuid(attempt_uuid, db_path=db_path)
    if not attempt:
        abort(404)

    session = database.get_session_by_uuid(attempt["session_id"], db_path=db_path)
    student_answers = database.get_student_answers_for_attempt(attempt["id"], db_path=db_path)

    # Compute comprehensive analytics
    analysis = LearningAnalyzer.analyze_attempt(student_answers, attempt["total_questions_planned"])
    
    # Check ML risk model for weakest topic
    ml_remediation_info = None
    if analysis["topic_breakdown"]:
        weakest = analysis["topic_breakdown"][0]
        recent_3 = student_answers[-3:]
        recent_acc = sum(1 for a in recent_3 if a["is_correct"] == 1) / max(1, len(recent_3))
        topic_acc = weakest["accuracy_percentage"] / 100.0
        ml_remediation_info = MLStudentRiskPredictor.predict_remediation_risk(
            recent_accuracy=recent_acc,
            topic_accuracy=topic_acc,
            topic_attempts=weakest["questions_attempted"],
            difficulty=attempt["current_difficulty"]
        )

    return render_template(
        "report.html",
        attempt=attempt,
        session=session,
        analysis=analysis,
        ml_info=ml_remediation_info
    )

@app.route("/review/<attempt_uuid>")
def review_answers(attempt_uuid: str):
    """Question-by-question review of student's answers against reference solutions."""
    db_path = app.config.get("DATABASE_PATH")
    attempt = database.get_attempt_by_uuid(attempt_uuid, db_path=db_path)
    if not attempt:
        abort(404)

    session = database.get_session_by_uuid(attempt["session_id"], db_path=db_path)
    student_answers = database.get_student_answers_for_attempt(attempt["id"], db_path=db_path)

    return render_template(
        "review.html",
        attempt=attempt,
        session=session,
        answers=student_answers
    )

@app.route("/history")
def progress_history():
    """Displays previous assessment attempts, improvement trends, and mastery summary."""
    db_path = app.config.get("DATABASE_PATH")
    attempts = database.get_all_attempts_history(db_path=db_path)
    
    # Calculate global analytics for dashboard header
    total_attempts = len(attempts)
    completed_attempts = [a for a in attempts if a["is_completed"]]
    avg_score = round(sum(a["score"] for a in completed_attempts) / max(1, len(completed_attempts)), 1) if completed_attempts else 0.0

    return render_template(
        "history.html",
        attempts=attempts,
        total_attempts=total_attempts,
        completed_count=len(completed_attempts),
        avg_score=avg_score
    )

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
