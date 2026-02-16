# routes/results.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from model import QuizSession, LevelAttempt, LevelAttempt, User
from database import get_db
from datetime import datetime
from uuid import uuid4

router = APIRouter()

@router.get("/results/{user_id}/{operation}")
def get_user_results(user_id: int, operation: str, db: Session = Depends(get_db)):
    attempts = (
        db.query(QuizSession)
        .filter(QuizSession.user_id == user_id, QuizSession.operation == operation)
        .order_by(QuizSession.start_time)
        .all()
    )

    return [
        {
            "attempt": idx + 1,
            "score": attempt.score,
            "total": attempt.total_questions,
            "timestamp": attempt.start_time,
            "level": attempt.level
        }
        for idx, attempt in enumerate(attempts)
    ]

@router.get("/progress/{user_id}")
def get_user_progress(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {"message": "User not found", "attempts": []}
    
    attempts = db.query(LevelAttempt).filter(LevelAttempt.user_id == user_id).all()

    attempt_data = [
        {
            "operation": a.operation,
            "level": a.level,
            "attempt_number": a.attempt_number,
            "score": a.score,
            "total_questions": a.total_questions,
            "date": a.timestamp.strftime("%Y-%m-%d %H:%M")
        }
        for a in attempts
    ]

    return {
        "ninja_stars": user.ninja_stars,
        "awarded_title": user.awarded_title,
        "attempts": attempt_data
    }

@router.post("/start-session")
def start_session(payload: dict, db: Session = Depends(get_db)):
    ...
    new_session = QuizSession(
        user_id=payload["user_id"],
        operation=payload["operation"],
        level=payload["level"],
        session_id=str(uuid4()),
        question_data=payload["questions"],
        start_time=datetime.utcnow()
    )
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return {"session_id": new_session.session_id}