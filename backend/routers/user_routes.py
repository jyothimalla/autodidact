from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from passlib.hash import bcrypt
from database import get_db
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends
from passlib.hash import bcrypt
from fastapi import FastAPI
from model import User, UserProgress, UserLog


router = APIRouter()

@router.get("/user/profile/{user_id}")
def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    progress = db.query(UserProgress).filter(UserProgress.user_id == user_id).all()
    return {
        "userid": user.id,
        "username": user.username,
        "email": user.email,
        "ninja_stars": user.ninja_stars,
        "awarded_title": "Math Explorer",
        "progress": [
            {
                "operation": p.operation,
                "level": p.level,
                "attempts": p.attempts,
                "best_score": p.best_score
            }
            for p in progress
        ]
    }


@router.get("/myaccount/{user_id}")
def get_user_account(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "userid": user.id,
        "username": user.username,
        "email": user.email,
        "ninja_stars": user.ninja_stars,
        "awarded_title": user.awarded_title,
    }

@router.put("/user/update/{user_id}")
def update_user(user_id: int, payload: dict, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.username = payload.get("username", user.username)
    user.email = payload.get("email", user.email)
    if payload.get("password"):
        user.password = bcrypt.hash(payload["password"])  # hash if password provided

    db.commit()
    return {"message": "User updated successfully"}

def log_user_action(db: Session, user_id: int, action: str):
    log = UserLog(user_id=user_id, action=action)
    db.add(log)
    db.commit()

@router.delete("/user/delete/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_active = False
    db.commit()
    log_user_action(db, user_id, "deactivated")

    return {"message": "User deactivated successfully"}

@router.post("/admin/reactivate-user/{user_id}")
def reactivate_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_active = True
    db.commit()
    log_user_action(db, user_id, "reactivated")

    return {"message": f"✅ User {user.id} reactivated"}


@router.get("/admin/inactive-users")
def get_inactive_users(db: Session = Depends(get_db)):
    users = db.query(User).filter(User.is_active == False).all()
    return users


@router.get("/admin/user-logs")
def get_user_logs(db: Session = Depends(get_db)):
    logs = db.query(UserLog).order_by(UserLog.timestamp.desc()).all()
    return logs
