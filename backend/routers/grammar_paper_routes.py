"""
Grammar School Paper endpoints.
  GET  /grammar/papers             → list all seeded papers
  GET  /grammar/papers/seed        → seed 10 fixed papers (idempotent)
  GET  /grammar/papers/{n}/questions        → questions without correct_option
  GET  /grammar/papers/{n}/answers          → questions with correct_option + explanation
  GET  /grammar/papers/{n}/question-pdf     → WeasyPrint PDF (questions only)
  GET  /grammar/papers/{n}/answer-sheet-pdf → WeasyPrint PDF + QR code (blank answer table)

  POST /grammar/papers/{n}/check-typed
    Body: { user_id, answers: {q1:'A',...} }
    → score + full review

  POST /grammar/papers/{n}/check-upload
    Body: multipart file (PDF or image)
    → OCR extract answers → score + full review
"""
import base64
import io
import os
import shutil
import tempfile

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from jinja2 import Template
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from generators.mcq_generator import generate_exam
from model import GrammarPaper
from utils.pdf_parser import extract_answers_from_pdf

router = APIRouter()

FRONTEND_BASE_URL = os.getenv("FRONTEND_BASE_URL", "https://www.autodidact.uk")
PAPERS_DIR = "generated_papers"
NUM_FIXED_PAPERS = 10
QUESTIONS_PER_PAPER = 50

MODULE_LABELS = {
    'four-operations':          'Four Operations',
    'fractions-decimals':       'Fractions & Decimals',
    'ratios':                   'Ratios',
    'percentages':              'Percentages',
    'multi-step-word-problems': 'Multi-step Word Problems',
    'mental-arithmetic':        'Mental Arithmetic',
    'speed-based-calculation':  'Speed-Based Calculation',
    'logical-number-puzzles':   'Logical Number Puzzles',
}


# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------
class CheckTypedRequest(BaseModel):
    user_id: int = 0
    answers: dict[str, str]   # { "q1": "A", "q2": "C", ... }


# ---------------------------------------------------------------------------
# Helpers
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
    return f"data:image/png;base64,{base64.b64encode(buf.read()).decode()}"


def _html_to_pdf(html: str, path: str) -> None:
    from weasyprint import HTML
    os.makedirs(PAPERS_DIR, exist_ok=True)
    HTML(string=html).write_pdf(path)


def _strip_answer(q: dict) -> dict:
    return {k: v for k, v in q.items() if k not in ('correct_option', 'correct_answer', 'explanation')}


def _score_answers(questions: list, submitted: dict) -> dict:
    """Score submitted answers against stored correct_options. Returns full result dict."""
    score = 0
    breakdown: dict[str, dict] = {}
    review = []
    optionLabels = ['A', 'B', 'C', 'D']

    for q in questions:
        qid = q['question_id']
        module = q['module_id']
        selected = (submitted.get(qid) or '').upper()
        is_correct = selected == q['correct_option']
        if is_correct:
            score += 1

        if module not in breakdown:
            breakdown[module] = {'label': MODULE_LABELS.get(module, module), 'score': 0, 'total': 0}
        breakdown[module]['total'] += 1
        if is_correct:
            breakdown[module]['score'] += 1

        review.append({
            'question_number': q['question_number'],
            'question': q['question'],
            'options': q['options'],
            'your_answer': selected,
            'correct_option': q['correct_option'],
            'correct_answer': q['correct_answer'],
            'explanation': q.get('explanation', ''),
            'is_correct': is_correct,
        })

    total = len(questions)
    pct = round(score / total * 100) if total else 0
    return {
        'score': score,
        'total': total,
        'percentage': pct,
        'passed': pct >= 60,
        'breakdown': list(breakdown.values()),
        'review': review,
    }


# ---------------------------------------------------------------------------
# GET /grammar/papers/seed
# ---------------------------------------------------------------------------
@router.get('/papers/seed')
def seed_papers(db: Session = Depends(get_db)):
    """Generate and store 10 fixed grammar papers. Idempotent — skips existing ones."""
    created = []
    for n in range(1, NUM_FIXED_PAPERS + 1):
        existing = db.query(GrammarPaper).filter_by(paper_number=n).first()
        if existing:
            continue
        questions = generate_exam(QUESTIONS_PER_PAPER, 'mixed')
        paper = GrammarPaper(
            paper_number=n,
            title=f"Grammar School Paper {n}",
            difficulty="mixed",
            questions_json=questions,
        )
        db.add(paper)
        created.append(n)
    db.commit()
    return {'created': created, 'message': f'{len(created)} paper(s) seeded.'}


# ---------------------------------------------------------------------------
# GET /grammar/papers
# ---------------------------------------------------------------------------
@router.get('/papers')
def list_papers(db: Session = Depends(get_db)):
    papers = db.query(GrammarPaper).order_by(GrammarPaper.paper_number).all()
    return [
        {
            'id': p.id,
            'paper_number': p.paper_number,
            'title': p.title,
            'difficulty': p.difficulty,
            'num_questions': len(p.questions_json),
        }
        for p in papers
    ]


# ---------------------------------------------------------------------------
# GET /grammar/papers/{n}/questions   (no correct answers)
# ---------------------------------------------------------------------------
@router.get('/papers/{n}/questions')
def get_questions(n: int, db: Session = Depends(get_db)):
    paper = db.query(GrammarPaper).filter_by(paper_number=n).first()
    if not paper:
        raise HTTPException(status_code=404, detail=f'Paper {n} not found. Call /grammar/papers/seed first.')
    return {
        'paper_number': n,
        'title': paper.title,
        'questions': [_strip_answer(q) for q in paper.questions_json],
    }


# ---------------------------------------------------------------------------
# GET /grammar/papers/{n}/answers  (with correct answers + explanations)
# ---------------------------------------------------------------------------
@router.get('/papers/{n}/answers')
def get_answers(n: int, db: Session = Depends(get_db)):
    paper = db.query(GrammarPaper).filter_by(paper_number=n).first()
    if not paper:
        raise HTTPException(status_code=404, detail=f'Paper {n} not found.')
    return {
        'paper_number': n,
        'title': paper.title,
        'questions': paper.questions_json,   # full detail
    }


# ---------------------------------------------------------------------------
# GET /grammar/papers/{n}/question-pdf
# ---------------------------------------------------------------------------
@router.get('/papers/{n}/question-pdf')
def download_question_pdf(n: int, db: Session = Depends(get_db)):
    from fastapi.responses import FileResponse
    paper = db.query(GrammarPaper).filter_by(paper_number=n).first()
    if not paper:
        raise HTTPException(status_code=404, detail=f'Paper {n} not found.')

    questions = [_strip_answer(q) for q in paper.questions_json]

    html = Template("""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body { font-family: Arial, sans-serif; margin: 40px; color: #222; }
  h1   { font-size: 20px; text-align: center; margin-bottom: 4px; }
  .meta { text-align: center; font-size: 13px; color: #555; margin-bottom: 20px; }
  .student-info { display: flex; gap: 40px; margin-bottom: 26px; font-size: 13px; }
  .student-info span { border-bottom: 1px solid #888; min-width: 180px; display: inline-block; }
  .question { margin-bottom: 18px; }
  .question p { margin: 0 0 4px; font-size: 14px; }
  .options { display: flex; flex-wrap: wrap; gap: 4px 24px; font-size: 13px; margin-left: 10px; }
  .option { padding: 2px 0; }
  .work-space { border: 1px solid #ddd; height: 28px; margin-top: 4px; border-radius: 3px; }
  .footer { margin-top: 40px; font-size: 11px; color: #aaa; text-align: center; }
</style>
</head>
<body>
  <h1>{{ title }}</h1>
  <div class="meta">Grammar School Entrance Examination &nbsp;|&nbsp; 50 Questions &nbsp;|&nbsp; 60 Minutes</div>

  <div class="student-info">
    <label>Name: <span>&nbsp;</span></label>
    <label>Date: <span>&nbsp;</span></label>
    <label>Score: <span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span> / 50</label>
  </div>

  <ol>
  {% for q in questions %}
    <li class="question">
      <p>{{ q.question }}</p>
      <div class="options">
        {% for lbl, val in q.options.items() %}
        <span class="option">{{ lbl }}) {{ val }}</span>
        {% endfor %}
      </div>
      <div class="work-space"></div>
    </li>
  {% endfor %}
  </ol>

  <div class="footer">autodidact.uk &mdash; {{ title }}</div>
</body>
</html>
""").render(title=paper.title, questions=questions)

    filename = f"Grammar_Paper_{n}_questions.pdf"
    path = os.path.join(PAPERS_DIR, filename)
    _html_to_pdf(html, path)
    return FileResponse(path, filename=filename, media_type="application/pdf")


# ---------------------------------------------------------------------------
# GET /grammar/papers/{n}/answer-sheet-pdf
# ---------------------------------------------------------------------------
@router.get('/papers/{n}/answer-sheet-pdf')
def download_answer_sheet_pdf(n: int, db: Session = Depends(get_db)):
    from fastapi.responses import FileResponse
    paper = db.query(GrammarPaper).filter_by(paper_number=n).first()
    if not paper:
        raise HTTPException(status_code=404, detail=f'Paper {n} not found.')

    qr_url = f"{FRONTEND_BASE_URL}/test-papers/{n}/submit"
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
  .title-block .meta { font-size: 12px; color: #555; }
  .qr-block { text-align: right; }
  .qr-block img { width: 110px; height: 110px; }
  .qr-block p { font-size: 10px; color: #888; margin: 4px 0 0; }
  .student-info { display: flex; gap: 40px; margin: 20px 0; font-size: 13px; }
  .student-info span { border-bottom: 1px solid #888; min-width: 200px; display: inline-block; }
  table { width: 100%; border-collapse: collapse; margin-top: 8px; }
  th { background: #f0f0f0; padding: 6px 8px; font-size: 12px; border: 1px solid #ccc; }
  td { padding: 8px; border: 1px solid #ccc; font-size: 12px; vertical-align: middle; }
  .q-num  { width: 50px; text-align: center; font-weight: bold; }
  .bubble-row { display: flex; gap: 14px; }
  .bubble { display: inline-flex; align-items: center; justify-content: center;
            width: 22px; height: 22px; border: 1px solid #999; border-radius: 50%;
            font-size: 11px; font-weight: bold; }
  .tick-box { width: 60px; text-align: center; }
  .footer { margin-top: 30px; font-size: 11px; color: #aaa; text-align: center; }
</style>
</head>
<body>
  <div class="header">
    <div class="title-block">
      <h1>{{ title }} — Answer Sheet</h1>
      <div class="meta">50 Questions &nbsp;|&nbsp; Circle one bubble per question</div>
    </div>
    <div class="qr-block">
      <img src="{{ qr_img }}" alt="QR">
      <p>Scan to submit online</p>
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
        <th>Circle your answer</th>
        <th class="tick-box">&#10003; / &#10007;</th>
      </tr>
    </thead>
    <tbody>
    {% for q in questions %}
      <tr>
        <td class="q-num">{{ loop.index }}</td>
        <td>
          <div class="bubble-row">
            <span class="bubble">A</span>
            <span class="bubble">B</span>
            <span class="bubble">C</span>
            <span class="bubble">D</span>
          </div>
        </td>
        <td class="tick-box">&nbsp;</td>
      </tr>
    {% endfor %}
    </tbody>
  </table>

  <div class="footer">autodidact.uk &mdash; {{ title }}</div>
</body>
</html>
""").render(title=paper.title, questions=paper.questions_json, qr_img=qr_img)

    filename = f"Grammar_Paper_{n}_answer_sheet.pdf"
    path = os.path.join(PAPERS_DIR, filename)
    _html_to_pdf(html, path)
    return FileResponse(path, filename=filename, media_type="application/pdf")


# ---------------------------------------------------------------------------
# POST /grammar/papers/{n}/check-typed
# ---------------------------------------------------------------------------
@router.post('/papers/{n}/check-typed')
def check_typed(n: int, req: CheckTypedRequest, db: Session = Depends(get_db)):
    paper = db.query(GrammarPaper).filter_by(paper_number=n).first()
    if not paper:
        raise HTTPException(status_code=404, detail=f'Paper {n} not found.')
    return _score_answers(paper.questions_json, req.answers)


# ---------------------------------------------------------------------------
# POST /grammar/papers/{n}/check-upload
# ---------------------------------------------------------------------------
@router.post('/papers/{n}/check-upload')
async def check_upload(n: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    paper = db.query(GrammarPaper).filter_by(paper_number=n).first()
    if not paper:
        raise HTTPException(status_code=404, detail=f'Paper {n} not found.')

    # Save uploaded file to a temp path
    suffix = os.path.splitext(file.filename or "upload.pdf")[1] or ".pdf"
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    try:
        extracted = extract_answers_from_pdf(tmp_path)   # [{question_number, answer}, ...]
    finally:
        os.unlink(tmp_path)

    # Convert extracted list to {q1: 'A', q2: 'B', ...} keyed by question_id
    submitted: dict[str, str] = {}
    for item in extracted:
        qnum = item.get('question_number')
        ans  = item.get('answer', '').upper()
        if qnum and ans in ('A', 'B', 'C', 'D'):
            submitted[f'q{qnum}'] = ans

    result = _score_answers(paper.questions_json, submitted)
    result['ocr_extracted'] = len(submitted)
    result['ocr_note'] = 'Some answers may not have been detected if handwriting was unclear.'
    return result
