"""
Custom paper generation for parents.
Endpoints:
  POST /paper/custom/generate
  GET  /paper/custom/{paper_id}/question-pdf
  GET  /paper/custom/{paper_id}/answer-sheet-pdf
"""
import base64
import io
import os
from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from jinja2 import Template
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from generators.custom_generators import generate_question
from model import CustomPaper

router = APIRouter()

FRONTEND_BASE_URL = os.getenv("FRONTEND_BASE_URL", "https://www.autodidact.uk")
PAPERS_DIR = "generated_papers"

MODULE_NAMES = {
    "four-operations":          "Four Operations",
    "fractions-decimals":       "Fractions and Decimals",
    "ratios":                   "Ratios",
    "percentages":              "Percentages",
    "multi-step-word-problems": "Multi-step Word Problems",
    "mental-arithmetic":        "Mental Arithmetic",
    "speed-based-calculation":  "Speed-Based Calculation",
    "logical-number-puzzles":   "Logical Number Puzzles",
}


# ---------------------------------------------------------------------------
# Pydantic request model
# ---------------------------------------------------------------------------
class GeneratePaperRequest(BaseModel):
    user_id: int
    module_id: str
    num_questions: int = 10
    difficulty: str = "medium"


# ---------------------------------------------------------------------------
# Helper: generate QR code as base64 PNG data-URI
# ---------------------------------------------------------------------------
def _qr_data_uri(content: str) -> str:
    import qrcode
    qr = qrcode.QRCode(box_size=6, border=2)
    qr.add_data(content)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    b64 = base64.b64encode(buf.read()).decode()
    return f"data:image/png;base64,{b64}"


# ---------------------------------------------------------------------------
# Helper: render HTML → PDF via WeasyPrint
# ---------------------------------------------------------------------------
def _html_to_pdf(html: str, path: str) -> None:
    from weasyprint import HTML
    os.makedirs(PAPERS_DIR, exist_ok=True)
    HTML(string=html).write_pdf(path)


# ---------------------------------------------------------------------------
# POST /paper/custom/generate
# ---------------------------------------------------------------------------
@router.post("/custom/generate")
def generate_custom_paper(req: GeneratePaperRequest, db: Session = Depends(get_db)):
    if req.module_id not in MODULE_NAMES:
        raise HTTPException(status_code=400, detail=f"Unknown module_id: {req.module_id}")
    if req.num_questions not in (5, 10, 15, 20):
        raise HTTPException(status_code=400, detail="num_questions must be 5, 10, 15 or 20")
    if req.difficulty not in ("easy", "medium", "hard"):
        raise HTTPException(status_code=400, detail="difficulty must be easy, medium or hard")

    paper_id = f"cp_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{uuid4().hex[:8]}"

    questions = []
    for i in range(req.num_questions):
        q = generate_question(req.module_id, req.difficulty)
        q["question_number"] = i + 1
        q["question_id"] = f"{paper_id}_q{i + 1}"
        questions.append(q)

    paper = CustomPaper(
        paper_id=paper_id,
        user_id=req.user_id,
        module_id=req.module_id,
        difficulty=req.difficulty,
        num_questions=req.num_questions,
        questions_json=questions,
    )
    db.add(paper)
    db.commit()
    db.refresh(paper)  # populate paper.id from DB

    return {
        "id": paper.id,
        "paper_id": paper_id,
        "module": MODULE_NAMES[req.module_id],
        "difficulty": req.difficulty,
        "num_questions": req.num_questions,
        "questions": questions,
    }


# ---------------------------------------------------------------------------
# GET /paper/custom/{paper_id}/question-pdf
# ---------------------------------------------------------------------------
@router.get("/custom/{paper_id}/question-pdf")
def download_question_pdf(paper_id: str, db: Session = Depends(get_db)):
    paper = db.query(CustomPaper).filter_by(paper_id=paper_id).first()
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")

    module_name = MODULE_NAMES.get(paper.module_id, paper.module_id)

    html = Template("""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body { font-family: Arial, sans-serif; margin: 40px; color: #222; }
  h1   { font-size: 20px; text-align: center; margin-bottom: 4px; }
  .meta { text-align: center; font-size: 13px; color: #555; margin-bottom: 24px; }
  .student-info { display: flex; gap: 40px; margin-bottom: 30px; font-size: 13px; }
  .student-info span { border-bottom: 1px solid #888; min-width: 200px; display: inline-block; }
  .question { margin-bottom: 22px; }
  .question p { margin: 0 0 8px 0; font-size: 14px; }
  .work-space { border: 1px solid #ddd; height: 50px; margin-top: 4px; border-radius: 4px; }
  .footer { margin-top: 40px; font-size: 11px; color: #aaa; text-align: center; }
</style>
</head>
<body>
  <h1>{{ module_name }} — Practice Paper</h1>
  <div class="meta">
    Difficulty: {{ difficulty | capitalize }} &nbsp;|&nbsp;
    {{ num_questions }} Questions &nbsp;|&nbsp;
    Paper ID: {{ paper_id }}
  </div>

  <div class="student-info">
    <label>Name: <span>&nbsp;</span></label>
    <label>Date: <span>&nbsp;</span></label>
    <label>Score: <span>&nbsp;&nbsp;&nbsp;&nbsp;</span> / {{ num_questions }}</label>
  </div>

  <ol>
  {% for q in questions %}
    <li class="question">
      <p>{{ q.question }}</p>
      <div class="work-space"></div>
    </li>
  {% endfor %}
  </ol>

  <div class="footer">autodidact.uk &mdash; {{ paper_id }}</div>
</body>
</html>
""").render(
        module_name=module_name,
        difficulty=paper.difficulty,
        num_questions=paper.num_questions,
        paper_id=paper_id,
        questions=paper.questions_json,
    )

    filename = f"{paper_id}_questions.pdf"
    path = os.path.join(PAPERS_DIR, filename)
    _html_to_pdf(html, path)
    return FileResponse(path, filename=filename, media_type="application/pdf")


# ---------------------------------------------------------------------------
# GET /paper/custom/{paper_id}/answer-sheet-pdf
# ---------------------------------------------------------------------------
@router.get("/custom/{paper_id}/answer-sheet-pdf")
def download_answer_sheet_pdf(paper_id: str, db: Session = Depends(get_db)):
    paper = db.query(CustomPaper).filter_by(paper_id=paper_id).first()
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")

    module_name = MODULE_NAMES.get(paper.module_id, paper.module_id)
    qr_url = f"{FRONTEND_BASE_URL}/submit-answers?paperId={paper_id}"
    qr_img = _qr_data_uri(qr_url)

    html = Template("""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body { font-family: Arial, sans-serif; margin: 40px; color: #222; }
  .header { display: flex; justify-content: space-between; align-items: flex-start; }
  .title-block h1 { font-size: 20px; margin-bottom: 4px; }
  .title-block .meta { font-size: 13px; color: #555; }
  .qr-block { text-align: right; }
  .qr-block img { width: 110px; height: 110px; }
  .qr-block p { font-size: 10px; color: #888; margin: 4px 0 0; }
  .student-info { display: flex; gap: 40px; margin: 24px 0; font-size: 13px; }
  .student-info span { border-bottom: 1px solid #888; min-width: 200px; display: inline-block; }
  table { width: 100%; border-collapse: collapse; margin-top: 10px; }
  th { background: #f0f0f0; padding: 8px; font-size: 13px; border: 1px solid #ccc; }
  td { padding: 10px 8px; border: 1px solid #ccc; font-size: 13px; vertical-align: top; }
  .q-num  { width: 60px; text-align: center; font-weight: bold; }
  .answer-box { min-height: 28px; }
  .tick-box   { width: 70px; text-align: center; }
  .footer { margin-top: 30px; font-size: 11px; color: #aaa; text-align: center; }
  .scan-note { font-size: 12px; color: #444; margin-top: 8px; }
</style>
</head>
<body>
  <div class="header">
    <div class="title-block">
      <h1>{{ module_name }} — Answer Sheet</h1>
      <div class="meta">
        Difficulty: {{ difficulty | capitalize }} &nbsp;|&nbsp;
        {{ num_questions }} Questions &nbsp;|&nbsp;
        Paper ID: {{ paper_id }}
      </div>
    </div>
    <div class="qr-block">
      <img src="{{ qr_img }}" alt="QR Code">
      <p class="scan-note">Scan to submit answers</p>
    </div>
  </div>

  <div class="student-info">
    <label>Name: <span>&nbsp;</span></label>
    <label>Date: <span>&nbsp;</span></label>
  </div>

  <table>
    <thead>
      <tr>
        <th class="q-num">Q</th>
        <th>Your Answer</th>
        <th class="tick-box">&#10003; / &#10007;</th>
      </tr>
    </thead>
    <tbody>
    {% for q in questions %}
      <tr>
        <td class="q-num">{{ loop.index }}</td>
        <td class="answer-box">&nbsp;</td>
        <td class="tick-box">&nbsp;</td>
      </tr>
    {% endfor %}
    </tbody>
  </table>

  <div class="footer">
    autodidact.uk &mdash; {{ paper_id }}
  </div>
</body>
</html>
""").render(
        module_name=module_name,
        difficulty=paper.difficulty,
        num_questions=paper.num_questions,
        paper_id=paper_id,
        questions=paper.questions_json,
        qr_img=qr_img,
    )

    filename = f"{paper_id}_answer_sheet.pdf"
    path = os.path.join(PAPERS_DIR, filename)
    _html_to_pdf(html, path)
    return FileResponse(path, filename=filename, media_type="application/pdf")
