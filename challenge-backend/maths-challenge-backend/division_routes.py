from fastapi import APIRouter, Query
from typing import List
from pydantic import BaseModel
import random

router = APIRouter()

class Question(BaseModel):
    question: str
    answer: str
    explanation: str

@router.get("/division/questions", response_model=List[Question])
def get_division_questions(level: int = Query(0, ge=0, le=10)):
    questions = []
    for _ in range(10):
        if level == 0:
            dividend = random.randint(1, 9)
            divisor = random.randint(1, 9)
        elif level in [1, 2, 3]:
            dividend = random.randint(10, 99)
            divisor = random.randint(1, 9)
        else:
            dividend = random.randint(50, 150)
            divisor = random.randint(1, 9)

        quotient = dividend // divisor
        question = f"{dividend} ÷ {divisor} = "
        answer = str(quotient)
        explanation = f"Divide {dividend} by {divisor} to get {quotient}"

        questions.append(Question(
            question=question,
            answer=answer,
            explanation=explanation
        ))

    return questions
