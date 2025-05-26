from fastapi import APIRouter, Query
import random
from model import GeneratedProblem
from database import SessionLocal

router = APIRouter()

names = ["Ava", "Liam", "Zoe", "Noah", "Emma", "Ethan"]
items = ["apples", "books", "coins", "stickers", "pencils"]

def generate_problem(op, level):
    if op == "addition":
        a, b = random.randint(5, 10 + level), random.randint(1, 5 + level)
        name1, name2 = random.sample(names, 2)
        item = random.choice(items)
        q = f"{name1} had {a} {item}. {name2} gave {name1} {b} more. How many does {name1} have now?"
        ans = a + b
    elif op == "subtraction":
        total = random.randint(10 + level, 20 + level * 2)
        taken = random.randint(1, total - 1)
        name = random.choice(names)
        item = random.choice(items)
        q = f"{name} had {total} {item}. They gave away {taken}. How many are left?"
        ans = total - taken
    elif op == "multiplication":
        count = random.randint(2, 4 + level)
        times = random.randint(2, 3 + level)
        name = random.choice(names)
        item = random.choice(items)
        q = f"{name} has {count} boxes of {item}, each with {times} items. How many in total?"
        ans = count * times
    elif op == "division":
        result = random.randint(2 + level, 10 + level)
        divisor = random.randint(1 + level, 5 + level)
        dividend = result * divisor
        name = random.choice(names)
        item = random.choice(items)
        q = f"{name} has {dividend} {item}, shared equally among {divisor} friends. How many each?"
        ans = result
    return q, str(ans)

@router.get("/word-problem")
def get_word_problems(
    user_name: str = "guest",
    operation: str = "addition",
    difficulty: int = 1,
    count: int = 10
):
    session = SessionLocal()
    result = []
    for _ in range(count):
        op = random.choice(["addition", "subtraction", "multiplication", "division"]) if operation == "mixed" else operation
        question, answer = generate_problem(op, difficulty)
        db_problem = GeneratedProblem(
            user_name=user_name,
            question=question,
            answer=answer,
            operation=op,
            level=difficulty
        )
        session.add(db_problem)
        result.append({"question": question, "answer": answer})
    session.commit()
    session.close()
    return {"problems": result}
