from fastapi import APIRouter, Body
from pydantic import BaseModel
from database import SessionLocal
from model import UserScore

router = APIRouter()

class ScoreSubmission(BaseModel):
    user_name: str
    operation: str
    level: int
    score: int
    total_questions: int

@router.post("/submit-score")
def submit_score(payload: ScoreSubmission):
    db = SessionLocal()

    # Get existing attempts to calculate next set number
    prev_attempts = db.query(UserScore).filter_by(
        user_name=payload.user_name,
        operation=payload.operation,
        level=payload.level
    ).count()

    new_score = UserScore(
        user_name=payload.user_name,
        operation=payload.operation,
        level=payload.level,
        set_number=prev_attempts + 1,
        score=payload.score,
        total_questions=payload.total_questions,
        is_completed=(payload.score == payload.total_questions)
    )
    db.add(new_score)
    db.commit()
    db.close()
    return {"message": "Score submitted", "set_number": prev_attempts + 1}
