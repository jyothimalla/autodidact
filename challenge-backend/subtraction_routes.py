from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import random

router = APIRouter()

class Question(BaseModel):
    question: str
    answer: str
    explanation: str

@router.get("/subtraction/questions", response_model=List[Question])
def get_subtraction_questions(level: int = 0):
    questions = []

    for _ in range(10):
        if level == 0:
            a, b = sorted([random.randint(1, 9), random.randint(1, 9)], reverse=True)
        elif level == 1:
            a, b = sorted([random.randint(10, 99), random.randint(10, 99)], reverse=True)
        else:
            a, b = sorted([random.randint(50, 150), random.randint(50, 150)], reverse=True)

        question = f"{a} - {b} ="
        answer = str(a - b)
        explanation = f"Subtract {b} from {a}"
        
        questions.append(Question(question=question, answer=answer, explanation=explanation))

    return questions
