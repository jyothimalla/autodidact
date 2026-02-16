from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from database import get_db
from models import QuizSession, LevelAttempt
from pydantic import BaseModel

router = APIRouter()

class TimeQuizSubmission(BaseModel):
    user_id: int
    user_name: str
    score: int
    total_questions: int

@router.post("/time-quiz/submit/")
def submit_time_quiz(data: TimeQuizSubmission, db: Session = Depends(get_db)):
    # Create a QuizSession
    session = QuizSession(
        user_id=data.user_id,
        operation="time",
        level=0,
        session_id=f"time_{data.user_id}_{int(datetime.utcnow().timestamp())}",
        question_data={},  # You can store question snapshots if needed
        score=data.score,
        start_time=datetime.utcnow(),
        end_time=datetime.utcnow()
    )
    db.add(session)
    db.commit()
    db.refresh(session)

    # Count previous attempts
    existing_attempts = db.query(LevelAttempt).filter_by(
        user_id=data.user_id,
        operation="time",
        level=0
    ).count()

    # Create a LevelAttempt
    level_attempt = LevelAttempt(
        user_id=data.user_id,
        user_name=data.user_name,
        operation="time",
        level=0,
        attempt_number=existing_attempts + 1,
        score=data.score,
        total_questions=data.total_questions,
        is_passed=data.score >= data.total_questions  # only 100% passes
    )
    db.add(level_attempt)
    db.commit()

    return {"message": "✅ Time Quiz saved!", "quiz_session_id": session.id}
