from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, JSON, TIMESTAMP
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON, TIMESTAMP, Float

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    year = Column(String(20), nullable=True)
    password = Column(String(255), nullable=False)
    ninja_stars = Column(Integer, default=0)
    awarded_title = Column(String(255), default="Beginner")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    sessions = relationship("QuizSession", back_populates="user")
    user_scores = relationship("UserScore", back_populates="user")
    logs = relationship("UserLog", back_populates="user")
    fmc_question_saves = relationship("FMCQuestionSave", back_populates="user")
    fmc_paper_sets = relationship("FMCPaperSet", back_populates="user")
    questions = relationship("Question", back_populates="user")

class UserLog(Base):
    __tablename__ = "user_logs"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String(50))  # 'deleted', 'deactivated', etc.
    timestamp = Column(TIMESTAMP, default=datetime.utcnow)

    user = relationship("User", back_populates="logs")

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


class FMCQuestionAttempt(Base):
    __tablename__ = "fmc_question_attempts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    level = Column(Integer, nullable=False)
    score = Column(Integer, nullable=False)
    questions_json = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

class FMCQuestionSave(Base):
    __tablename__ = "fmc_question_save"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    level = Column(Integer)
    paper_id = Column(String(255), unique=True, nullable=False)  # ✅ required
    questions = Column(JSON, nullable=False)  # ✅ save all 10 questions here
    is_exam_ready = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="fmc_question_saves")


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

class FMCPaperSet(Base):
    __tablename__ = "fmc_paper_sets"
    id = Column(Integer, primary_key=True)
    paper_id = Column(String(255), unique=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    level = Column(Integer)
    show_answers = Column(Boolean, default=False)
    questions_json = Column(JSON)  # 🔥 all 10 questions as one JSON blob
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    user = relationship("User", back_populates="fmc_paper_sets")

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

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="questions")


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
    score = Column(Integer, default=0)
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)

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

class MockTest(Base):
    __tablename__ = "mock_tests"
    id = Column(Integer, primary_key=True)
    test_id = Column(String(255), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    questions_json = Column(JSON, nullable=False)  # 50 MCQ questions with correct_option
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

class MockTestResult(Base):
    __tablename__ = "mock_test_results"
    id = Column(Integer, primary_key=True)
    test_id = Column(String(255), ForeignKey("mock_tests.test_id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    score = Column(Integer, nullable=False)
    total = Column(Integer, nullable=False)
    time_taken = Column(Integer, default=0)  # seconds
    answers_json = Column(JSON, nullable=False)
    submitted_at = Column(TIMESTAMP, default=datetime.utcnow)

class GrammarPaper(Base):
    __tablename__ = "grammar_papers"
    id = Column(Integer, primary_key=True)
    paper_number = Column(Integer, unique=True, nullable=False)
    title = Column(String(255), nullable=False)
    difficulty = Column(String(50), default='mixed')
    questions_json = Column(JSON, nullable=False)  # 50 MCQ questions
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

class CustomPaper(Base):
    __tablename__ = "custom_papers"
    id = Column(Integer, primary_key=True)
    paper_id = Column(String(255), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    module_id = Column(String(100), nullable=False)
    difficulty = Column(String(50), nullable=False)
    num_questions = Column(Integer, nullable=False)
    questions_json = Column(JSON, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

class PracticeAttempt(Base):
    __tablename__ = "practice_attempts"
    id = Column(Integer, primary_key=True)
    attempt_id = Column(String(255), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    subject_id = Column(String(100), nullable=False)  # e.g., 'maths', 'computers'
    module_id = Column(String(100), nullable=False)   # e.g., 'four-operations', 'python-programming'
    topic_id = Column(String(100), nullable=True)     # e.g., 'addition', 'python-basics'
    level = Column(Integer, nullable=False)           # Level number
    attempt_type = Column(String(20), nullable=False) # 'practice' or 'challenge'
    mode = Column(String(20), nullable=False)         # 'online' or 'download'
    num_questions = Column(Integer, nullable=False)   # 5 for practice, 10 for challenge
    questions_json = Column(JSON, nullable=False)     # Questions with correct answers
    answers_json = Column(JSON, nullable=True)        # Student's answers (null if downloaded but not submitted)
    score = Column(Integer, nullable=True)            # Number correct (null if not submitted)
    percentage = Column(Float, nullable=True)         # Score percentage
    time_taken = Column(Integer, default=0)           # Time in seconds
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    submitted_at = Column(TIMESTAMP, nullable=True)   # When answers were submitted
