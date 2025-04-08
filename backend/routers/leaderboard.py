from fastapi import APIRouter
from sqlalchemy import desc
from database import SessionLocal, UserScore

router = APIRouter()

@router.get("/leaderboard")
def get_leaderboard(operation: str = "addition"):
    db = SessionLocal()
    results = db.query(UserScore).filter_by(operation=operation, is_completed=True).order_by(desc(UserScore.created_at)).limit(10).all()
    db.close()
    return [
        {
            "name": row.user_name,
            "level": row.level,
            "score": row.score,
            "set": row.set_number,
            "date": row.created_at
        }
        for row in results
    ]
