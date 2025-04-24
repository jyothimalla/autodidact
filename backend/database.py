import os
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

# =======================
# Environment Variables
# =======================
# Load environment variables from .env file
load_dotenv()

DATABASE_URL = "postgresql://autodidact:password@localhost:5432/autodidact"

#DATABASE_URL = os.getenv("DATABASE_URL")

# Database connection setup
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "../postgresql/schema.sql")

engine = create_engine(DATABASE_URL)
conn = engine.connect()
print("✅ Connection successful")
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

# =======================
# Models
# =======================

class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(String(500), nullable=False)
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

class QuizResponse(Base):
    __tablename__ = "quiz_responses"
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey("quiz_sessions.id"), nullable=False)
    question_index = Column(Integer, nullable=False)
    selected_answer = Column(String(10), nullable=False)
    correct_answer = Column(String(10), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    session = relationship("QuizSession", back_populates="responses")


class QuizSession(Base):
    __tablename__ = "quiz_sessions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    operation = Column(String(50), nullable=False)  # e.g., addition, multiplication
    level = Column(Integer, nullable=False)
    session_id = Column(String(100), unique=True, nullable=False)
    question_data = Column(JSON, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="sessions")
    responses = relationship("QuizResponse", back_populates="session")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    ninja_stars = Column(Integer, default=0) 
    awarded_title = Column(String, default="Beginner")  
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    sessions = relationship("QuizSession", back_populates="user")
    
class UserAnswer(Base):
    __tablename__ = "user_answers"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    question_id = Column(Integer, nullable=False)
    selected_answer = Column(String(10), nullable=False)
    correct_answer = Column(String(10), nullable=False)

class GeneratedProblem(Base):
    __tablename__ = "generated_problems"
    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(String, nullable=False)
    operation = Column(String, nullable=False)
    level = Column(Integer, default=1)
    attempted = Column(Boolean, default=False)
    user_answer = Column(String, nullable=True)
    correct = Column(Boolean, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

class UserScore(Base):
    __tablename__ = "user_scores"
    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, nullable=False)
    operation = Column(String, nullable=False)
    level = Column(Integer, nullable=False)
    set_number = Column(Integer, default=1)
    score = Column(Integer, nullable=False)
    total_questions = Column(Integer, nullable=False)
    is_completed = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

class UserProgress(Base):
    __tablename__ = "user_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    ninja_stars = Column(Integer, default=0)
    user_name = Column(String, nullable=False)
    operation = Column(String, nullable=False)
    level_completed = Column(Integer, nullable=False)
    dojo_points = Column(Integer, nullable=False)
    current_level = Column(Integer, default=0)   
    total_attempts = Column(Integer, default=0)  
    
class FMCQuestionBank(Base):
    __tablename__ = "fmc_question_bank"

    id = Column(Integer, primary_key=True, index=True)
    level = Column(Integer, nullable=False)
    question_type = Column(String, nullable=False)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    explanation = Column(String, nullable=False)
    image = Column(String, nullable=True)  # ✅ Optional image
    is_exam_ready = Column(Boolean, default=False)  # ✅ Admin toggle

class LevelAttempt(Base):
    __tablename__ = "level_attempts"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user_name = Column(String, nullable=False)
    operation = Column(String, nullable=False)
    level = Column(Integer, nullable=False)
    attempt_number = Column(Integer, nullable=False)
    score = Column(Integer, nullable=False)
    total_questions = Column(Integer, nullable=False)
    is_passed = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# =======================
# Initialize DB
# =======================
def init_db():
    table_sql = """
    CREATE TABLE IF NOT EXISTS generated_problems (
        id SERIAL PRIMARY KEY,
        user_name TEXT NOT NULL,
        question TEXT NOT NULL,
        answer TEXT NOT NULL,
        operation TEXT NOT NULL,
        level INTEGER NOT NULL DEFAULT 1,
        attempted BOOLEAN DEFAULT FALSE,
        user_answer TEXT,
        correct BOOLEAN,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    with engine.connect() as connection:
        connection.execute(text(table_sql))
        connection.commit()