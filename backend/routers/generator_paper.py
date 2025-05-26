from fastapi import APIRouter, Query, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from datetime import datetime
import uuid
import os
import json
from fastapi import APIRouter, Query, Depends, HTTPException
from fastapi.responses import StreamingResponse
from database import get_db
from model import User, FMCQuestionSave, FMCPaperSet
from utils.generate_pdf import create_pdf, create_pdf_stream
from utils.generate_excel import create_excel, create_excel_stream
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from utils.paper_generator import generate_paper_pdf
from uuid import uuid4
from typing import List
from routers.fmc_routes import generate_fmc_problem
from fastapi.responses import FileResponse
from jinja2 import Template
from weasyprint import HTML


router = APIRouter(prefix="/paper", tags=["Paper"])


from utils.pdf_utils import create_pdf_stream
from utils.excel_utils import create_excel_stream

@router.get("/fmc/get-paper-json")
def get_paper_json(user_id: int, level: int, sublevel: str = 'C', db: Session = Depends(get_db)):
    paper = db.query(FMCPaperSet).filter_by(
        user_id=user_id, level=level, sublevel=sublevel
    ).order_by(FMCPaperSet.created_at.desc()).first()

    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")

    return paper.questions_json
@router.get("/fmc/generate-paper-pdf")
def generate_and_download_paper(
    user_id: int,
    level: int,
    show_answers: bool = False,
    db: Session = Depends(get_db)
):
    
    paper_id = f"paper_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{uuid4().hex[:6]}"
    questions = []

    for i in range(10):
        q = generate_fmc_problem(level)
        q_dict = q.dict()
        q_dict["question_id"] = f"{paper_id}_{i}"
        questions.append(q_dict)

    # ✅ Save entire paper as one JSON record
    paper = FMCQuestionSave(
        user_id=user_id,
        level=level,
        paper_id=paper_id,
        questions=questions,
        is_exam_ready=show_answers
    )
    db.add(paper)
    db.commit()

    # ✅ HTML template to render as PDF
    html_template = """
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            h1 { color: #444; }
            .question { margin-bottom: 20px; }
            .answer { font-size: 12px; color: green; margin-top: 5px; }
        </style>
    </head>
    <body>
        <h1>Maths Challenge Paper</h1>
        <p><strong>Paper ID:</strong> {{ paper_id }}</p>
        <ol>
        {% for q in questions %}
            <li class="question">
                <p>{{ q.question }}</p>
                {% if show_answers %}
                <div class="answer"><strong>Answer:</strong> {{ q.answer }}</div>
                {% endif %}
            </li>
        {% endfor %}
        </ol>
    </body>
    </html>
    """

    template = Template(html_template)
    html_content = template.render(paper_id=paper_id, questions=questions, show_answers=show_answers)

    filename = f"{paper_id}_{'with_answers' if show_answers else 'student'}.pdf"
    pdf_path = f"generated_papers/{filename}"
    os.makedirs("generated_papers", exist_ok=True)
    HTML(string=html_content).write_pdf(pdf_path)

    return FileResponse(pdf_path, filename=filename, media_type="application/pdf")


@router.post("/fmc/evaluate-paper")
def evaluate_fmc_paper(paper_id: str, answers: List[dict], db: Session = Depends(get_db)):
    record = db.query(FMCQuestionSave).filter_by(paper_id=paper_id).first()
    if not record:
        return {"error": "Paper not found"}

    original_questions = json.loads(record.questions)
    score = 0
    result = []

    for answer in answers:
        qid = answer.get("question_id")
        student_ans = answer.get("student_answer", "").strip().lower()
        match = next((q for q in original_questions if q["question_id"] == qid), None)
        if not match:
            continue
        correct_ans = match["answer"].strip().lower()
        is_correct = student_ans == correct_ans
        score += is_correct
        result.append({
            "question": match["question"],
            "student_answer": student_ans,
            "correct_answer": correct_ans,
            "is_correct": is_correct,
            "explanation": match.get("explanation", "")
        })

    return {
        "score": score,
        "out_of": len(original_questions),
        "results": result
    }
def generate_basic_pdf(text, path="output.pdf"):
    c = canvas.Canvas(path)
    c.drawString(100, 750, "Maths Challenge Paper")
    y = 720
    for line in text.splitlines():
        c.drawString(100, y, line)
        y -= 20
    c.save()