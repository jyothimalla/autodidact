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
            question = f"{a} × {b} = "
            answer = str(a * b)
            explanation = f"Single-digit multiplication of {a} and {b}."
        elif level == 1:
            a, b = random.randint(10, 99), random.randint(1, 9)
            question = f"{a} × {b} = "
            answer = str(a * b)
            explanation = f"Two-digit × one-digit multiplication."
        elif level == 2:
            a, b = random.randint(10, 99), random.randint(10, 99)
            question = f"{a} × {b} = "
            answer = str(a * b)
            explanation = f"Two-digit × two-digit multiplication."
        elif level == 3:
            a, b, c = random.randint(10, 99), random.randint(1, 9), random.randint(1, 9)
            question = f"{a} × {b} × {c} = "
            answer = str(a * b * c)
            explanation = f"Triple multiplication."
        else:
            a, b = random.randint(100, 999), random.randint(10, 99)
            question = f"{a} × {b} = "
            answer = str(a * b)
            explanation = f"Large number multiplication using any method."

        questions.append({
            "question": question,
            "answer": answer,
            "explanation": explanation
        })

    return questions
