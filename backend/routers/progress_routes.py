from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import UserProgress, get_db
from typing import Optional


router = APIRouter(prefix="/progress", tags=["Progress"])

@router.post("/update")
def update_progress(user_name: str, operation: str, level: int, passed: bool, db: Session = Depends(get_db)):
    progress = db.query(UserProgress).filter_by(user_name=user_name, operation=operation).first()

    if not progress:
        progress = UserProgress(
            user_name=user_name,
            operation=operation,
            level_completed=level if passed else 0,
            dojo_points=10 if passed else 0,
            current_level=level,
            total_attempts=1
        )
        db.add(progress)
    else:
        progress.total_attempts += 1
        if passed:
            progress.level_completed = max(progress.level_completed, level)
            progress.dojo_points += 10
            progress.current_level = level + 1

    db.commit()
    return {"message": "Progress updated", "current_level": progress.current_level, "dojo_points": progress.dojo_points}


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db, UserProgress, LevelAttempt

router = APIRouter()

@router.get("/progress/{user_id}")
def get_progress(user_id: int, operation: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(LevelAttempt).filter(LevelAttempt.user_id == user_id)
    if operation:
        query = query.filter(LevelAttempt.operation == operation)

    attempts = query.all()

    progress_summary = []
    levels = {}

    for attempt in attempts:
        level = attempt.level
        if level not in levels:
            levels[level] = {
                "attempts": 0,
                "best_score": 0
            }
        levels[level]["attempts"] += 1
        levels[level]["best_score"] = max(levels[level]["best_score"], attempt.score)

    for level, data in levels.items():
        progress_summary.append({
            "level": level,
            "attempts": data["attempts"],
            "best_score": data["best_score"]
        })

    return {
        "progress": progress_summary
    }
