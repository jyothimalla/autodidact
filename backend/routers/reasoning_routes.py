# reasoning_routes.py

from fastapi import APIRouter
from typing import List
from pydantic import BaseModel
import random
from routers import reasoning_routes


router = APIRouter()

class Question(BaseModel):
    question: str
    answer: str
    explanation: str

@router.get("/reasoning/flow-logic", response_model=List[Question])
def get_flow_chain_questions():
    questions = []
    for _ in range(10):
        start = random.randint(1, 9)
        multiplier = 0
        subtractor = random.randint(1, 5)
        final = random.randint(1, 10)
        temp = start * multiplier
        missing = final + subtractor - temp
        question = f"{start} → × {multiplier} → + ? → - {subtractor} = {final}"
        answer = str(missing)
        explanation = f"{start} × {multiplier} = {temp}, then ? = {final} + {subtractor} - {temp}"
        questions.append(Question(question=question, answer=answer, explanation=explanation))
    return questions

@router.get("/reasoning/shapes", response_model=List[Question])
def get_symbolic_shapes_questions():
    questions = []
    for _ in range(10):
        triangle = random.randint(1, 9)
        pentagon = random.randint(1, triangle)
        hexagon = random.randint(1, 9)
        trapezium = 4
        q_text = (
            f"🟥 - 🟩 = {triangle - pentagon}\n"
            f"🟨 ÷ 2 = {trapezium // 2}\n"
            f"🟩 + 🟦 = {pentagon + hexagon}\n"
            f"What is the value of 🟥?"
        )
        answer = str(triangle)
        explanation = (
            f"🟩 = {pentagon}, 🟦 = {hexagon}, 🟥 = 🟩 + ({triangle - pentagon}) = {triangle}"
        )
        questions.append(Question(question=q_text, answer=answer, explanation=explanation))
    return questions

@router.get("/reasoning/max-option", response_model=List[Question])
def get_max_option_questions():
    questions = []
    for _ in range(10):
        a, b, c = random.sample(range(1, 5), 3)
        options = {
            "A": a + b - c,
            "B": b - a + c,
            "C": a + c - b,
            "D": c - b + a,
            "E": c - b - a
        }
        correct_option = max(options, key=options.get)
        q_text = (
            f"Which gives the highest value?\n"
            f"A. {a} + {b} - {c}\n"
            f"B. {b} - {a} + {c}\n"
            f"C. {a} + {c} - {b}\n"
            f"D. {c} - {b} + {a}\n"
            f"E. {c} - {b} - {a}"
        )
        explanation = f"Option {correct_option} = {options[correct_option]} is the highest."
        questions.append(Question(question=q_text, answer=correct_option, explanation=explanation))
    return questions

@router.get("/reasoning")
def test():
    return {"message": "Reasoning route is working!"}