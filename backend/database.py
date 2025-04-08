import os
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import text
# =======================
# Environment Variables
# =======================
# Load environment variables from .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Database connection setup
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "../postgresql/schema.sql")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
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
    id = Column(Integer, primary_key=True, index=True)
    student_name = Column(String(100), nullable=False)
    session_id = Column(String(100), nullable=False)
    question_id = Column(Integer, nullable=False)
    selected_answer = Column(String(5), nullable=False)
    correct_answer = Column(String(5), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

class QuizSession(Base):
    __tablename__ = "quiz_session"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False)
    session_id = Column(String(255), nullable=False, unique=True)
    question_data = Column(JSON, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    answers = relationship("UserAnswer", back_populates="user")

class UserAnswer(Base):
    __tablename__ = "user_answers"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    question_id = Column(Integer, nullable=False)
    selected_answer = Column(String(10), nullable=False)
    correct_answer = Column(String(10), nullable=False)
    user = relationship("User", back_populates="answers")

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

# =======================
# Initialize DB
# =======================
def init_db():
    with engine.connect() as connection:
        with open(SCHEMA_PATH, "r") as file:
            sql_commands = file.read().split(';')
            for command in sql_commands:
                cleaned = command.strip()
                if cleaned:
                    connection.execute(text(cleaned))