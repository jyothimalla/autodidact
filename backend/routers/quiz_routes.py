from fastapi import APIRouter, FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
from pydantic import BaseModel
import random
from datetime import datetime
from database import get_db, LevelAttempt, User
from sqlalchemy.orm import Session
import logging

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

# ====== In-Memory Storage ======
user_sessions = {}
question_bank = {}


attempts = []

quiz_results = []

# ====== API Routes ======
@router.get("/")
def root():
    return {"message": "FastAPI backend is running!"}


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