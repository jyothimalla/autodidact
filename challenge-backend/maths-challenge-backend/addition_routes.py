from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import random

router = APIRouter()

class Question(BaseModel):
    question: str
    answer: str
    explanation: str

@router.get("/addition/questions", response_model=List[Question])
def get_addition_questions(level: int = 0):
    questions = []

    for _ in range(10):
        if level == 0:
            a, b = random.randint(1, 9), random.randint(1, 9)
        elif level == 1:
            a, b = random.randint(10, 99), random.randint(10, 99)
        elif level == 2:
            a, b, c = random.randint(10, 99), random.randint(10, 99), random.randint(1, 9)
        else:
            a, b = random.randint(50, 150), random.randint(50, 150)

        if level == 2:
            question = f"{a} + {b} + {c} = "
            answer = str(a + b + c)
            explanation = f"Add {a}, {b}, and {c}"
        else:
            question = f"{a} + {b} = "
            answer = str(a + b)
            explanation = f"Add {a} and {b}"

        questions.append(Question(
            question=question,
            answer=answer,
            explanation=explanation
        ))

    return questions
