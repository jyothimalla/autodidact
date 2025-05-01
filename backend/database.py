import os
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON, TIMESTAMP
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, Session
from datetime import datetime
from dotenv import load_dotenv
import time
from sqlalchemy.exc import OperationalError

def init_db(retries=10, delay=3):
    for attempt in range(retries):
        try:
            Base.metadata.create_all(bind=engine)
            print("✅ Database initialized and tables created.")
            break
        except OperationalError as e:
            print(f"❌ Attempt {attempt + 1} failed: {e}")
            time.sleep(delay)
    else:
        print("🚨 Failed to connect to database after several attempts.")

# ======================
# Environment Variables
# ======================
load_dotenv()

# ✅ MySQL database URL
DATABASE_URL = "mysql+pymysql://autodidact_user:Root%401234@db/autodidact_db"

# Database connection setup
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

# ======================
# Models
# ======================

class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(String(1000), nullable=False)
    option_a = Column(String(255), nullable=False)
    option_b = Column(String(255), nullable=False)
    option_c = Column(String(255), nullable=False)
    option_d = Column(String(255), nullable=False)
    option_e = Column(String(255), nullable=False)
    correct_answer = Column(String(5), nullable=False)
    image_url = Column(String(500), nullable=True)

class UploadedFile(Base):
    __tablename__ = "uploaded_files"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)

class QuizSession(Base):
    __tablename__ = "quiz_sessions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    operation = Column(String(50), nullable=False)
    level = Column(Integer, nullable=False)
    session_id = Column(String(100), unique=True, nullable=False)
    question_data = Column(JSON, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="sessions")
    responses = relationship("QuizResponse", back_populates="session")

class QuizResponse(Base):
    __tablename__ = "quiz_responses"
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey("quiz_sessions.id"), nullable=False)
    question_index = Column(Integer, nullable=False)
    selected_answer = Column(String(10), nullable=False)
    correct_answer = Column(String(10), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    session = relationship("QuizSession", back_populates="responses")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    ninja_stars = Column(Integer, default=0)
    awarded_title = Column(String(255), default="Beginner")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    sessions = relationship("QuizSession", back_populates="user")
    user_scores = relationship("UserScore", back_populates="user")
    fmc_admin_records = relationship("FMCAdmin", back_populates="user")

class UserAnswer(Base):
    __tablename__ = "user_answers"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    question_id = Column(Integer, nullable=False)
    selected_answer = Column(String(10), nullable=False)
    correct_answer = Column(String(10), nullable=False)

class UserProgress(Base):
    __tablename__ = "user_progress"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    ninja_stars = Column(Integer, default=0)
    user_name = Column(String(255), nullable=False)
    operation = Column(String(50), nullable=False)
    level_completed = Column(Integer, nullable=False)
    dojo_points = Column(Integer, nullable=False)
    current_level = Column(Integer, default=0)
    total_attempts = Column(Integer, default=0)

class FMCQuestionBank(Base):
    __tablename__ = "fmc_question_bank"
    id = Column(Integer, primary_key=True, index=True)
    level = Column(Integer, nullable=False)
    question_type = Column(String(255), nullable=False)
    question = Column(String(1000), nullable=False)
    answer = Column(String(255), nullable=False)
    explanation = Column(String(1000), nullable=False)
    image = Column(String(500), nullable=True)
    is_exam_ready = Column(Boolean, default=False)

class UserScore(Base):
    __tablename__ = "user_scores"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    operation = Column(String(50), nullable=False)
    level = Column(Integer, nullable=False)
    set_number = Column(Integer, default=1)
    score = Column(Integer, nullable=False)
    total_questions = Column(Integer, nullable=False)
    is_completed = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    user = relationship("User", back_populates="user_scores")

class FMCAdmin(Base):
    __tablename__ = "fmc_admin"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    level = Column(Integer, nullable=False)
    question_type = Column(String(255), nullable=False)
    question = Column(String(1000), nullable=False)
    answer = Column(String(255), nullable=False)
    explanation = Column(String(1000), nullable=False)
    image = Column(String(500), nullable=True)
    is_exam_ready = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="fmc_admin_records")

class FMCQuestionAttempt(Base):
    __tablename__ = "fmc_question_attempts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    level = Column(Integer, nullable=False)
    score = Column(Integer, nullable=False)
    questions = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

class FMCQuestionSave(Base):
    __tablename__ = "fmc_question_save"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    level = Column(Integer)
    question_type = Column(String(255))
    question = Column(String(1000))
    answer = Column(String(255))
    explanation = Column(String(1000))
    image = Column(String(500))
    is_exam_ready = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

class LevelAttempt(Base):
    __tablename__ = "level_attempts"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user_name = Column(String(255), nullable=False)
    operation = Column(String(50), nullable=False)
    level = Column(Integer, nullable=False)
    attempt_number = Column(Integer, nullable=False)
    score = Column(Integer, nullable=False)
    total_questions = Column(Integer, nullable=False)
    is_passed = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

class GeneratedProblem(Base):
    __tablename__ = "generated_problems"
    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String(255), nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(String(255), nullable=False)
    operation = Column(String(50), nullable=False)
    level = Column(Integer, default=1)
    attempted = Column(Boolean, default=False)
    user_answer = Column(String(255), nullable=True)
    correct = Column(Boolean, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

# ======================
# Utility Functions
# ======================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized and tables created.")

if __name__ == "__main__":
    init_db()
