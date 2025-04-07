from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
from pydantic import BaseModel
import random
from datetime import datetime


router = APIRouter()



# ====== Models ======
class Question(BaseModel):
    question: str
    options: Dict[str, str]
    answer: str
    explanation: str = None  # Optional explanation field

class UserSession(BaseModel):
    name: str
    operation: str = "multiplication"
    level: int = 0

class QuizResult(BaseModel):
    name: str
    score: int
    total: int
    answers: List[str]

# ====== In-Memory Storage ======
user_sessions = {}
question_bank = {}

# ====== Question Generator ======
def generate_questions(operation: str, level: int) -> List[Question]:
    questions = []
    for _ in range(10):
        if operation == "addition":
            if level == 0:
                a, b = random.randint(1, 9), random.randint(1, 9)
            elif level == 1:
                a, b = random.randint(10, 20), random.randint(1, 10)
            elif level == 2:
                a, b = random.randint(10, 20), random.randint(10, 20)
            elif level == 3:
                a, b = random.randint(10, 99), random.randint(10, 99)
            elif level == 4:
                a, b = random.randint(10, 50), random.randint(20, 50)
                c,d = random.randint(1, 10), random.randint(1, 10)
                text = f"{a} + {b} + {c} + {d}= "
            elif level == 5:
                a, b = random.randint(20, 50), random.randint(20, 50)
            elif level == 6:
                a, b = random.randint(20, 50), random.randint(50, 80)
            elif level == 7:
                a, b = random.randint(50, 100), random.randint(50, 80)
            elif level == 8:
                a, b = random.randint(50, 100), random.randint(80, 100)
            else:
                a, b = random.randint(80, 100), random.randint(80, 100)
        

            correct = a + b 
            text = f"{a} + {b} = "
            explanation = f"When you add {a} and {b}, you get {correct}."


        elif operation == "subtraction":
            if level == 1:
                a, b = random.randint(1, 9), random.randint(1, 9)
            else:
                a, b = random.randint(10, 20), random.randint(1, 10)
            if b > a:
                a, b = b, a
            
            correct = a - b
            text = f"{a} - {b} ="
            explanation = f"When you subtract {b} from {a}, you get {correct}."

        elif operation == "multiplication":
            if level == 0:
                a, b = random.randint(1, 5), random.randint(1, 5)
            else:
                a, b = random.randint(1, 10), random.randint(1, 10)
            correct = a * b
            text = f"{a} × {b}?"
            explanation = f"When you multiply {a} and {b}, you get {correct}."

        elif operation == "division":
            if level == 0:
                b = random.randint(1, 5)
                correct = random.randint(1, 5)
            else:
                b = random.randint(1, 10)
                correct = random.randint(1, 10)
            a = b * correct
            text = f"{a} ÷ {b} = "
            explanation = f"When you divide {a} by {b}, you get {correct}."

        else:
            correct = 0
            text = "Invalid operation"
            explanation = "No Explanation available"

        # Shuffle options
        options = [correct,
                   correct + random.randint(1, 3),
                   correct - random.randint(1, 2),
                   correct + random.randint(4, 6)]
        options = list(set(options))[:4]
        while len(options) < 4:
            options.append(correct + random.randint(7, 10))
        random.shuffle(options)
        labels = ['A', 'B', 'C', 'D']
        option_dict = {label: str(opt) for label, opt in zip(labels, options)}
        correct_label = next(label for label, val in option_dict.items() if int(val) == correct)

        questions.append(Question(
            question=text,
            options=option_dict,
            answer=correct_label,
            explanation=explanation
        ))

    return questions

attempts = []

quiz_results = []

# ====== API Routes ======
@router.get("/")
def root():
    return {"message": "FastAPI backend is running!"}

@router.post("/start-session")
def start_session(data: UserSession):
    print(f"Starting session for: {data.name}, operation: {data.operation}, level: {data.level}")

    user_sessions[data.name] = {
        "score": 0,
        "current_q": 0,
        "answers": {}
    }
    # Generate and save questions for the user
    question_bank[data.name] = generate_questions(data.operation, data.level)
    return {"message": "Session started", "name": data.name}

@router.get("/quiz/questions", response_model=List[Question])
def get_user_questions(name: str):
    return question_bank.get(name, [])


@router.post("/quiz/submit-result")
def submit_result(result: QuizResult):
    quiz_results.append({
        "name": result.name,
        "score": result.score,
        "total": result.total,
        "answers": result.answers,
        "timestamp": datetime.now().isoformat()
    })
    return {"status": "ok"}


@router.get("/quiz/leaderboard")
def get_leaderboard():
    return sorted(quiz_results, key=lambda r: r["score"], reverse=True)


@router.post("/start-session")
def start_session(data: UserSession):
    print(f"🔁 Starting session for: {data.name} | Operation: {data.operation}, Level: {data.level}")

    user_sessions[data.name] = {
        "score": 0,
        "current_q": 0,
        "answers": {},
        "operation": data.operation,
        "level": data.level,
    }

    # ✅ Correctly generate questions for the selected operation and level
    question_bank[data.name] = generate_questions(data.operation, data.level)

    return {"message": "Session started", "name": data.name}


class AnswerSubmission(BaseModel):
    name: str
    question_index: int
    selected_answer: str

@router.post("/quiz/submit-answer")
def submit_answer(data: AnswerSubmission):
    # Save to DB or in-memory store
    print(f"User {data.name} selected {data.selected_answer} for Q{data.question_index}")
    return {"status": "ok"}