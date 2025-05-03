import os
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sqladmin import Admin, ModelView
from database import engine, Base, init_db, Question, QuizSession, User, UserScore, LevelAttempt
from fastapi.responses import JSONResponse


# Initialize DB
init_db()

from routers import (
    word_problem_routes,
    user_routes,
    attempt_routes,
    quiz_routes,
    sudoku_routes,
    addition_routes,
    subtraction_routes,
    multiplication_routes,
    division_routes,
    submit_score,
    fmc_routes,
    reasoning_routes,
    auth_routes,
    progress_routes,
)

# Create FastAPI app
app = FastAPI()

# Root route
@app.get("/")
def read_root():
    return {"message": "Hello from Autodidact!"}

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled Error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error", "details": str(exc)},
    )

# Admin panel setup
admin = Admin(app, engine)

# Define Admin Views
class QuestionAdmin(ModelView, model=Question):
    column_list = [Question.id, Question.question_text, Question.correct_answer]

class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username, User.email, User.ninja_stars, User.awarded_title]

class FMCAdmin(ModelView, model=UserScore):
    column_list = [UserScore.id, UserScore.score]

class LevelAttemptAdmin(ModelView, model=LevelAttempt):
    column_list = [
        LevelAttempt.id,
        LevelAttempt.user_id,
        LevelAttempt.user_name,
        LevelAttempt.operation,
        LevelAttempt.level,
        LevelAttempt.attempt_number,
        LevelAttempt.score,
        LevelAttempt.total_questions,
        LevelAttempt.is_passed,
        LevelAttempt.timestamp
    ]


# Register admin views
admin.add_view(QuestionAdmin)
admin.add_view(UserAdmin)
admin.add_view(FMCAdmin)
admin.add_view(LevelAttemptAdmin)


# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",                # local Angular dev
        "https://autodidact.uk",                # live Angular site
        "https://www.autodidact.uk",            # optional www version
        "https://api.autodidact.uk/auth/login"  # Backend URI
        
        ],  # Angular frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include Routers
app.include_router(quiz_routes.router)
app.include_router(addition_routes.router)
app.include_router(subtraction_routes.router)
app.include_router(division_routes.router)
app.include_router(multiplication_routes.router)
app.include_router(sudoku_routes.router)
app.include_router(word_problem_routes.router)
app.include_router(submit_score.router)
app.include_router(fmc_routes.router)
app.include_router(progress_routes.router)
app.include_router(reasoning_routes.router)
app.include_router(auth_routes.router)
app.include_router(attempt_routes.router)
app.include_router(user_routes.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
