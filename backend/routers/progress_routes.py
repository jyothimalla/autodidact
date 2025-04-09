from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from database import SessionLocal, get_db, UserProgress

router = APIRouter()

@router.post("/save-progress")
def save_progress(
    data: dict = Body(...),
    db: Session = Depends(get_db)
):
    new_progress = UserProgress(
        user_name=data["userName"],
        operation=data["operation"],
        level_completed=data["level"],
        dojo_points=data["dojoPoints"]
    )
    db.add(new_progress)
    db.commit()
    db.refresh(new_progress)
    return {"message": "✅ Progress saved", "data": data}
