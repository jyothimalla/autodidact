from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List
import random
from database import GeneratedProblem
from fastapi import Depends
from database import get_db
from sqlalchemy.orm import Session


router = APIRouter()

class FMCQuestion(BaseModel):
    question: str
    answer: str
    explanation: str

names = ["Ava", "Lima", "Zoe", "Noah", "Emma", "Ethan"]
items = ["apples", "books", "coins", "stickers", "pencils"]

def generate_fmc_problem(level: int):
    op = random.choice(["addition", "subtraction", "multiplication", "division"])
    name1, name2 = random.sample(names, 2)
    item = random.choice(items)

    if op == "addition":
        a, b = random.randint(5, 10 + level), random.randint(1, 5 + level)
        question = f"{name1} had {a} {item}. {name2} gave {name1} {b} more. How many does {name1} have now?"
        answer = str(a + b)
        explanation = f"{a} + {b} = {a + b}"

    elif op == "subtraction":
        total = random.randint(10 + level, 20 + level * 2)
        taken = random.randint(1, total - 1)
        question = f"{name1} had {total} {item}. {name1} gave away {taken}. How many are left?"
        answer = str(total - taken)
        explanation = f"{total} - {taken} = {total - taken}"

    elif op == "multiplication":
        count = random.randint(2, 4 + level)
        times = random.randint(2, 3 + level)
        question = f"{name1} has {count} boxes of {item}, each with {times} items. How many in total?"
        answer = str(count * times)
        explanation = f"{count} × {times} = {count * times}"

    else:  # division
        result = random.randint(2 + level, 10 + level)
        divisor = random.randint(1 + level, 5 + level)
        dividend = result * divisor
        question = f"{name1} has {dividend} {item}, shared equally among {divisor} friends. How many each?"
        answer = str(result)
        explanation = f"{dividend} ÷ {divisor} = {result}"

    return FMCQuestion(question=question, answer=answer, explanation=explanation)


@router.get("/fmc/questions", response_model=List[FMCQuestion])
def get_fmc_questions(level: int = 0):
    return [generate_fmc_problem(level) for _ in range(10)]

@router.get("/fmc/all")
def get_all_generated(db: Session = Depends(get_db)):
    return db.query(GeneratedProblem).order_by(GeneratedProblem.id.desc()).limit(10).all()

@router.get("/fmc/history")
def get_user_history(user_name: str, db: Session = Depends(get_db)):
    return db.query(GeneratedProblem).filter_by(user_name=user_name).order_by(GeneratedProblem.created_at.desc()).all()
