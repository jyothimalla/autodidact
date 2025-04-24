# routers/auth_routes.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from passlib.hash import bcrypt
from database import get_db, User
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends
from passlib.hash import bcrypt
from fastapi import FastAPI

router = APIRouter(prefix="/auth", tags=["Auth"])
app = FastAPI()

class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    confirm_password: str


class LoginRequest(BaseModel):
    username: str
    password: str

class ResetPasswordRequest(BaseModel):
    email: EmailStr
    new_password: str
    confirm_password: str

@router.post("/register")
def register_user(credentials: RegisterRequest, db: Session = Depends(get_db)):
    print("📝 Incoming registration data:", credentials.dict())

    if credentials.password != credentials.confirm_password:
        print("❌ Passwords do not match")
        raise HTTPException(status_code=400, detail="Passwords do not match")

    existing_user = db.query(User).filter(
        (User.username == credentials.username) | (User.email == credentials.email)
    ).first()

    if existing_user:
        print("❌ User already exists")
        raise HTTPException(status_code=400, detail="Username or email already taken")

    hashed_password = bcrypt.hash(credentials.password)
    new_user = User(
        username=credentials.username,
        email=credentials.email,
        password=hashed_password,
        is_active=True,
        is_admin=False,
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        print("✅ Registration complete for:", new_user.username)
        return {"message": "User registered successfully", "user_id": new_user.id}
    except Exception as e:
        print("🔥 Database error:", e)
        raise HTTPException(status_code=500, detail="Internal server error")



@router.post("/login")
def login_user(credentials: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username.ilike(credentials.username)).first()
    
    if not user or not bcrypt.verify(credentials.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return {"message": "Login successful", 
            "user_id": user.id,
            "username": user.username}


@router.post("/reset-password")
def reset_password(credentials: ResetPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if credentials.new_password != credentials.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    user.password = bcrypt.hash(credentials.new_password)
    db.commit()
    return {"message": "Password reset successfully"}


@router.post("/logout")
def logout_user():
    # Implement token/session handling here if needed
    return {"message": "Logout successful"}


@router.get("/profile")
def get_profile(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "username": user.username,
        "email": user.email
    }


@router.put("/profile")
def update_profile(user_id: int, updated_data: RegisterRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if updated_data.password != updated_data.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    existing_user = db.query(User).filter(
        (User.username == updated_data.username) | (User.email == updated_data.email)
    ).first()
    if existing_user and existing_user.id != user_id:
        raise HTTPException(status_code=400, detail="Username or email already taken")

    user.username = updated_data.username
    user.email = updated_data.email
    user.password = bcrypt.hash(updated_data.password)

    db.commit()
    return {"message": "Profile updated successfully"}


@router.delete("/delete")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}