from pydantic import BaseModel
from typing import Optional

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
