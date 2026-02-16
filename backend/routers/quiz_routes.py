from fastapi import APIRouter, FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
from pydantic import BaseModel
import random
from datetime import datetime
from database import get_db
from model import LevelAttempt, User, QuizSession, FMCPaperSet, FMCPaperSet
from sqlalchemy.orm import Session
import logging
from uuid import uuid4
from fastapi.responses import FileResponse
import os, json
from reportlab.pdfgen import canvas

from model import FMCQuestionSave
from routers.fmc_routes import generate_fmc_problem
from openpyxl import Workbook
from fastapi.responses import StreamingResponse
from io import BytesIO


logger = logging.getLogger(__name__)

router = APIRouter()



# ====== Models ======
class Question(BaseModel):
    question: str
    options: Dict[str, str]
    answer: str
    explanation: str = None  # Optional explanation field

class UserSession(BaseModel):
    name: str
    operation: str = "multiplication"
    level: int = 0

class QuizResult(BaseModel):
    name: str
    score: int
    total: int
    answers: List[str]

class SessionStartRequest(BaseModel):
    username: str
    operation: str
    level: int


# ====== In-Memory Storage ======
user_sessions = {}
question_bank = {}


attempts = []

quiz_results = []

# ====== API Routes ======
@router.get("/")
def root():
    return {"message": "FastAPI backend is running!"}

@router.post("/start-session")
def start_session(data: SessionStartRequest):
    print("✅ Session started:", data)
    return {
        "message": f"Session started for {data.username}",
        "operation": data.operation,
        "level": data.level,
        "timestamp": datetime.utcnow()
    }
@router.post("/submit-result")
def submit_result(result: QuizResult):
    quiz_results.append({
        "username": result.username,
        "score": result.score,
        "total": result.total,
        "answers": result.answers,
        "timestamp": datetime.now().isoformat()
    })
    return {"status": "ok"}


@router.get("/leaderboard")
def get_leaderboard():
    return sorted(quiz_results, key=lambda r: r["score"], reverse=True)


class AnswerSubmission(BaseModel):
    name: str
    question_index: int
    selected_answer: str

@router.post("/submit-answer")
def submit_answer(data: AnswerSubmission):
    # Save to DB or in-memory store
    print(f"User {data.name} selected {data.selected_answer} for Q{data.question_index}")
    return {"status": "ok"}

@router.post("/record-attempt")
def record_attempt(user_id: int, operation: str, level: int, score: int, total_questions: int, db: Session = Depends(get_db)):
    attempt_number = db.query(LevelAttempt).filter_by(user_id=user_id, level=level, operation=operation).count() + 1
    is_passed = score == total_questions

    level_attempt = LevelAttempt(
        user_id=user_id,
        user_name=db.query(User).filter(User.id == user_id).first().username,
        operation=operation,
        level=level,
        attempt_number=attempt_number,
        score=score,
        total_questions=total_questions,
        is_passed=is_passed
    )
    db.add(level_attempt)
    db.commit()

    return {"message": "Level attempt recorded", "attempt_number": attempt_number}

@router.post("/submit-challenge/")
def submit_challenge(user_id: int, operation: str, level: int, score: int, total_questions: int, db: Session = Depends(get_db)):
    # Fetch user info
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {"error": "User not found"}

    # Check if user already attempted this level
    previous_attempts = db.query(LevelAttempt).filter_by(user_id=user_id, operation=operation, level=level).count()
    attempt_number = previous_attempts + 1

    # Define passing condition (example: 80% needed to pass)
    passing_score = 0.8 * total_questions
    is_passed = score >= passing_score
    logger.info(f"User {user_id} submitting attempt for level {level}")
    logger.info(f"Attempt number: {attempt_number}, Score: {score}, Total Questions: {total_questions}, Is Passed: {is_passed}")


    # Create LevelAttempt record
    level_attempt = LevelAttempt(
        user_id=user_id,
        user_name=user.username,
        operation=operation,
        level=level,
        attempt_number=attempt_number,
        score=score,
        total_questions=total_questions,
        is_passed=is_passed
    )

    db.add(level_attempt)
    db.commit()
    db.refresh(level_attempt)

    return {
        "message": "Challenge submitted successfully!",
        "level_attempt_id": level_attempt.id,
        "attempt_number": attempt_number,
        "is_passed": is_passed
    }


@router.post("/level-attempt/")
def save_level_attempt(
    
    user_id: int,
    operation: str,
    level: int,
    score: int,
    total_questions: int,
    db: Session = Depends(get_db)
):
    logger.info("Saving attempt for user_id=1, level=2, etc...")

    print(f"🔍 Fetching user with ID = {user_id}")
    user = db.query(User).filter(User.id == user_id).first()
    print(f"✅ User found: {user.username if user else 'None'}")

    if not user:
        return {"error": "User not found"}

    previous_attempts = db.query(LevelAttempt).filter_by(user_id=user_id, operation=operation, level=level).count()
    attempt_number = previous_attempts + 1

    is_passed = score >= (0.8 * total_questions)

    level_attempt = LevelAttempt(
        user_id=user.id,
        user_name=user.username,
        operation=operation,
        level=level,
        attempt_number=attempt_number,
        score=score,
        total_questions=total_questions,
        is_passed=is_passed
    )
   
    db.add(level_attempt)
    db.commit()
    db.refresh(level_attempt)
    update_ninja_stars_and_title(user_id, db)

    return {
        "message": "Level attempt saved successfully!",
        "level_attempt_id": level_attempt.id,
        "attempt_number": attempt_number,
        "is_passed": is_passed
    }

# for updating the ninja stars and title
def update_ninja_stars_and_title(user_id: int, db: Session):
    attempts = db.query(LevelAttempt).filter(LevelAttempt.user_id == user_id).all()

    level_weights = {i: (i + 1) * 0.1 for i in range(10)}  # 0.1 to 1.0
    total_weight = 0
    weighted_score = 0

    for a in attempts:
        if a.is_passed:
            weight = level_weights.get(a.level, 0)
            total_weight += weight
            performance = a.score / a.total_questions
            weighted_score += performance * weight

    if total_weight == 0:
        average_score = 0
    else:
        average_score = weighted_score / total_weight

    # Convert average score to stars (out of 5)
    ninja_stars = round(average_score * 5)

    # Award title
    if ninja_stars >= 5:
        title = "Math Ninja 🥇"
    elif ninja_stars >= 3:
        title = "Confident Solver 🥈"
    elif ninja_stars >= 1:
        title = "Basic Learner 🥉"
    else:
        title = "Getting Started"

    # Update user table
    user = db.query(User).filter_by(id=user_id).first()
    if user:
        user.ninja_stars = ninja_stars
        user.awarded_title = title
        db.commit()


@router.post("/start-session")
def start_quiz_session(user_id: int, username: str, operation: str, level: int, db: Session = Depends(get_db)):
    # Create unique session ID
    session_id = str(uuid4())
    
    # Build session entry
    session_entry = QuizSession(
        user_id=user_id,
        session_id=session_id,
        operation=operation,
        level=level,
        question_data={},  # You can populate this with actual questions if needed
        start_time=datetime.utcnow(),
        score=0
    )

    db.add(session_entry)
    db.commit()
    db.refresh(session_entry)

    return {
        "message": "Session started",
        "session_id": session_id,
        "session_db_id": session_entry.id
    }

@router.get("/fmc/generate-paper-pdf")
def generate_paper_pdf(user_id: int, level: int, show_answers: bool = False, db: Session = Depends(get_db)):
    paper_id = f"paper_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{uuid4().hex[:4]}"
    filename = f"{paper_id}_{'teacher' if show_answers else 'student'}.pdf"
    pdf_path = os.path.join("generated_papers", filename)
    os.makedirs("generated_papers", exist_ok=True)

    c = canvas.Canvas(pdf_path)
    y = 800
    c.drawString(50, y, f"Maths Challenge Paper ID: {paper_id}")
    y -= 40
    questions = []
    for i in range(20):
        q = generate_fmc_problem(level)
        c.drawString(50, y, f"{i+1}. {q.question}")
        y -= 30
        if show_answers:
            c.drawString(70, y, f"Answer: {q.answer}")
            y -= 20
        answer = getattr(q, "answer", "N/A")
        question = getattr(q, "question", "No question")
        explanation = getattr(q, "explanation", "")

        question_entry = {
        "number": i + 1,
        "question": q.question,
        "answer": q.answer,
        "explanation": q.explanation,
        }
        questions.append(question_entry)
    
        paper_set = FMCPaperSet(
        paper_id=paper_id,
        user_id=user_id,
        level=level,
        show_answers=show_answers,
        questions_json=questions,
        )
        db.add(paper_set)

        if y < 100:
            c.showPage()
            y = 800
    
    print("✅ Saved question:", question)
    db.commit()
    print("✅ Paper saved and PDF created:", pdf_path)

    c.save()
    return FileResponse(path=pdf_path, filename=filename, media_type="application/pdf")


@router.get("/fmc/download-paper-pdf")
def download_pdf(user_id: int, level: int, sublevel: str = 'C', db: Session = Depends(get_db)):
    paper_id = f"{user_id}_{level}_{sublevel}"
    paper_record = db.query(PaperSet).filter_by(code=paper_id).first()

    if not paper_record or not paper_record.question_json:
        return {"error": "Paper not found or empty"}

    questions = json.loads(paper_record.question_json)
    filename = f"{paper_id}.pdf"
    filepath = os.path.join("generated_papers", filename)
    os.makedirs("generated_papers", exist_ok=True)

    c = canvas.Canvas(filepath)
    y = 800
    c.setFont("Helvetica", 12)
    c.drawString(50, y, f"Maths Challenge Paper: {paper_id}")
    y -= 40

    for i, q in enumerate(questions):
        c.drawString(50, y, f"{i+1}. {q['question']}")
        y -= 25
        c.drawString(70, y, f"Answer: {q['answer']}")
        y -= 30
        if y < 100:
            c.showPage()
            y = 800

    c.save()
    return FileResponse(path=filepath, filename=filename, media_type="application/pdf")


@router.get("/fmc/download-paper-excel")
def download_excel(user_id: int, level: int, sublevel: str = 'C', db: Session = Depends(get_db)):
    paper_id = f"{user_id}_{level}_{sublevel}"
    paper_record = db.query(PaperSet).filter_by(code=paper_id).first()

    if not paper_record or not paper_record.question_json:
        return {"error": "Paper not found or empty"}

    questions = json.loads(paper_record.question_json)
    filename = f"{paper_id}.xlsx"
    filepath = os.path.join("generated_papers", filename)
    os.makedirs("generated_papers", exist_ok=True)

    wb = Workbook()
    ws = wb.active
    ws.append(["Question", "Answer"])

    for q in questions:
        ws.append([q["question"], q["answer"]])

    wb.save(filepath)
    return FileResponse(path=filepath, filename=filename, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
