from typing import Optional
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class FMCQuestionCreate(BaseModel):
    level: int
    question_type: str
    question: str
    answer: str
    explanation: str
    image: Optional[str] = None
    is_exam_ready: Optional[bool] = False

class FMCQuestionRead(FMCQuestionCreate):
    id: int

    class Config:
        orm_mode = True

class LevelAttempt(BaseModel):
    user_name: str
    operation: str
    level: int
    attempt_number: int
    score: int
    total_questions: int
    is_passed: bool
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)

    
