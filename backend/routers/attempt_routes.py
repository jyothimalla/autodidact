from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from model import LevelAttempt
from database import get_db
from pydantic import BaseModel
from datetime import datetime
from typing import List
import models, schemas
from schemas import LevelAttempt as LevelAttemptSchema 


router = APIRouter(prefix="/attempts", tags=["Level Attempts"])

class AttemptInput(BaseModel):
    user_name: str
    operation: str
    level: int
    score: int
    total_questions: int
    is_passed: bool

@router.post("/record")
def record_attempt(data: AttemptInput, db: Session = Depends(get_db)):
    # Count current number of attempts for this level
    existing_attempts = db.query(LevelAttempt).filter_by(
        user_name=data.user_name,
        operation=data.operation,
        level=data.level
    ).count()

    new_attempt = LevelAttempt(
        user_name=data.user_name,
        operation=data.operation,
        level=data.level,
        attempt_number=existing_attempts + 1,
        score=data.score,
        total_questions=data.total_questions,
        is_passed=data.is_passed,
        timestamp=datetime.utcnow()
    )
    db.add(new_attempt)
    db.commit()
    return {
        "message": "Attempt recorded",
        "attempt_number": new_attempt.attempt_number
    }

@router.get("/attempts/stats", response_model=List[schemas.LevelAttempt])
def get_all_attempts(db: Session = Depends(get_db)):
    return db.query(models.LevelAttempt).all()