import os
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
from dotenv import load_dotenv
from model import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

# ======================
# Environment Variables
# ======================
load_dotenv()


# ✅ MySQL database URL
DATABASE_URL = os.getenv("DATABASE_URL")
print("Connecting to DB:", DATABASE_URL)

# Database connection setup
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()