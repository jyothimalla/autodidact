from fastapi import FastAPI,requests, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
from pydantic import BaseModel
import random
from fastapi import FastAPI
from routers import word_problem_routes
from routers import quiz_routes
from routers import sudoku_routes
from routers import addition_routes
from routers import subtraction_routes
from routers import multiplication_routes
from routers import division_routes
from database import init_db
from routers import submit_score 
from sqlalchemy import text
from database import init_db
init_db()


from sqladmin import Admin, ModelView
from database import engine, Question, QuizSession, User, UserScore  # Import your models
from database import Base, engine
Base.metadata.create_all(bind=engine)


app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from Autodidact!"}

admin = Admin(app, engine)

@app.on_event("startup")
def configure_schema():
    with engine.connect() as conn:
        conn.execute(text("SET search_path TO jyothi, public"))

# Define views
class QuestionAdmin(ModelView, model=Question):
    column_list = [Question.id, Question.question_text, Question.correct_answer]

class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.name]

# Register views
admin.add_view(QuestionAdmin)
admin.add_view(UserAdmin)


# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with your frontend origin in prod

    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all quiz-related routes
app.include_router(quiz_routes.router)
app.include_router(addition_routes.router)
app.include_router(subtraction_routes.router)
app.include_router(division_routes.router)
app.include_router(multiplication_routes.router)
app.include_router(sudoku_routes.router)
app.include_router(word_problem_routes.router)
app.include_router(submit_score.router)

