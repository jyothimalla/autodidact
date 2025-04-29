from fastapi import APIRouter, Query
from pydantic import BaseModel
from typing import List
import random

router = APIRouter()

class DivisionQuestion(BaseModel):
    question: str
    answer: str
    explanation: str

@router.get("/division/questions", response_model=List[DivisionQuestion])
def generate_division_questions(level: int = Query(0, ge=0, le=10)):
    """Generate 10 division questions based on level."""
    questions: List[DivisionQuestion] = []

    for _ in range(10):
        if level == 0:
            divisor = random.randint(2, 5)
            quotient = random.randint(1, 5)
        elif level == 1:
            divisor = random.randint(2, 5)
            quotient = random.randint(5, 10)
        elif level == 2:
            divisor = random.randint(2, 10)
            quotient = random.randint(5, 15)
        elif level == 3:
            divisor = random.randint(2, 12)
            quotient = random.randint(10, 20)
        elif level == 4:
            divisor = random.randint(5, 15)
            quotient = random.randint(10, 30)
        elif level == 5:
            divisor = random.randint(5, 20)
            quotient = random.randint(10, 50)
        elif level == 6:
            divisor = random.randint(5, 30)
            quotient = random.randint(10, 60)
        elif level == 7:
            divisor = random.randint(10, 50)
            quotient = random.randint(20, 80)
        elif level == 8:
            divisor = random.randint(10, 75)
            quotient = random.randint(30, 100)
        elif level == 9 or level == 10:
            divisor = random.randint(20, 100)
            quotient = random.randint(50, 200)
        else:
            divisor = random.randint(2, 10)
            quotient = random.randint(2, 10)

        dividend = divisor * quotient  # ✅ Make sure perfectly divisible

        questions.append(DivisionQuestion(
            question=f"{dividend} ÷ {divisor} = ",
            answer=str(quotient),
            explanation=f"Because {dividend} ÷ {divisor} = {quotient} exactly."
        ))

    return questions
