from fastapi import APIRouter, Query
from typing import List, Dict
import random

router = APIRouter()

@router.get("/multiplication/questions", response_model=List[Dict])
def get_multiplication_questions(level: int = Query(0, ge=0, le=10)):
    questions = []
    for _ in range(10):
        if level == 0:
            a, b = random.randint(1, 9), random.randint(1, 9)
            question_text = f"{a} × {b} = "
            answer = str(a * b)
            explanation = f"Multiply {a} and {b}."

        elif level == 1:
            a, b = random.randint(10, 99), random.randint(10, 99)
            question_text = f"{a} × {b} = "
            answer = str(a * b)
            explanation = f"Multiply {a} and {b}."

        elif level == 2:
            a, b, c = random.randint(10, 99), random.randint(10, 99), random.randint(1, 9)
            question_text = f"{a} × {b} × {c} = "
            answer = str(a * b * c)
            explanation = f"Multiply {a}, {b}, and {c}."

        else:
            a, b = random.randint(50, 150), random.randint(50, 150)
            question_text = f"{a} × {b} = "
            answer = str(a * b)
            explanation = f"Multiply {a} and {b} carefully."

        questions.append({
            "question": question_text,
            "answer": answer,
            "explanation": explanation
        })

    return questions
