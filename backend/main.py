import os
import logging
from fastapi.middleware.cors import CORSMiddleware
from model import Base, Question, QuizSession, User, UserScore, LevelAttempt
from database import engine, get_db
from fastapi.responses import JSONResponse, FileResponse
from fastapi import FastAPI, Depends, Request   
from sqlalchemy.orm import Session
from fastapi import FastAPI, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session
import shutil
import pandas as pd
import crud
from utils.pdf_parser import extract_answers_from_pdf
from init_db import init_db
from admin_views import register_admin_views
from routers.fmc_routes import generate_fmc_problem
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse

from fastapi.staticfiles import StaticFiles
# Initialize DB
init_db()

Base.metadata.create_all(bind=engine)

UPLOAD_FOLDER = "uploaded_papers"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)



from routers import (word_problem_routes, user_routes, attempt_routes,
    quiz_routes, sudoku_routes, addition_routes, subtraction_routes,
    multiplication_routes, division_routes, submit_score, fmc_routes,
    reasoning_routes, auth_routes, progress_routes, results, generator_paper, generate_paper_excel)

# Create FastAPI app
app = FastAPI()

from admin_views import register_admin_views
# Register admin views
register_admin_views(app)

# Root route
@app.get("/", response_class=HTMLResponse)
def custom_home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Maths Challenge Admin Panel</title>
        <style>
            body {
                font-family: 'Segoe UI', sans-serif;
                background: linear-gradient(to right, #fdfbfb, #ebedee);
                color: #333;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
                margin: 0;
            }
            .container {
                background: white;
                padding: 40px;
                border-radius: 16px;
                box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
                text-align: center;
                max-width: 400px;
                width: 90%;
            }
            h1 {
                margin-bottom: 12px;
                font-size: 28px;
                color: #0d47a1;
            }
            p {
                margin-bottom: 24px;
                font-size: 16px;
            }
            a {
                text-decoration: none;
                background-color: #1976d2;
                color: white;
                padding: 12px 24px;
                border-radius: 8px;
                font-weight: bold;
                transition: background-color 0.3s ease;
            }
            a:hover {
                background-color: #1565c0;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔐 Admin Access</h1>
            <p>Welcome to the <strong>Maths Challenge</strong> backend panel.</p>
            <a href="/admin">Go to Admin Dashboard</a>
        </div>
    </body>
    </html>
    """

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled Error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error", "details": str(exc)},
    )

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",           # local Angular dev
        "https://autodidact.uk",           # live Angular site
        "https://www.autodidact.uk" ,
        "https://api.autodidact.uk/auth/login" ,      # optional www version
        "https://www.api.autodidact.uk/auth/login" 
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
app.include_router(attempt_routes.router)
app.include_router(results.router)
app.include_router(generator_paper.router)
app.include_router(generate_paper_excel.router)


@app.post("/upload-paper/")
async def upload_and_process_paper(
    student_name: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    answers = extract_answers_from_pdf(file_path)

    data = []
    for q_num, answer in answers:
        crud.save_answer(db, student_name, q_num, answer)
        data.append({
            "Student": student_name,
            "Question": q_num,
            "Answer": answer
        })

    # Save to Excel
    df = pd.DataFrame(data)
    excel_path = os.path.join(UPLOAD_FOLDER, f"{student_name}_answers.xlsx")
    df.to_excel(excel_path, index=False)

    return FileResponse(excel_path, filename=f"{student_name}_answers.xlsx", media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


@app.get("/debug/sessions")
def get_sessions(db: Session = Depends(get_db)):
    return db.query(QuizSession).all()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
