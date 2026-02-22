"""
Grammar-school mock exam endpoints.
  POST /test/generate          → create 50-question MCQ exam
  GET  /test/{test_id}         → fetch questions (no correct_option sent to client)
  POST /test/{test_id}/submit  → score and persist result
  GET  /test/results/{user_id} → list past results for a user
  GET  /test/{test_id}/question-pdf → generate questions PDF
  GET  /test/{test_id}/answer-sheet-pdf → generate answer sheet with QR code
  POST /test/{test_id}/check-upload → OCR answer submission
  POST /test/{test_id}/check-typed → manual answer entry
"""
import base64
import io
import os
import random
import re
import shutil
import tempfile
from datetime import datetime
from uuid import uuid4

import qrcode
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from weasyprint import HTML
from pypdf import PdfWriter, PdfReader

from database import get_db
from generators.mcq_generator import generate_exam, generate_mcq
from model import MockTest, MockTestResult
from routers.grammar_paper_routes import _render_question_html, _render_answer_sheet_html
from utils.pdf_parser import extract_answers_from_pdf

router = APIRouter()

NUM_QUESTIONS = 50
TIME_LIMIT_SECONDS = 3600  # 60 minutes

MODULE_LABELS = {
    'four-operations':          'Four Operations',
    'fractions-decimals':       'Fractions & Decimals',
    'ratios':                   'Ratios',
    'percentages':              'Percentages',
    'multi-step-word-problems': 'Multi-step Word Problems',
    'mental-arithmetic':        'Mental Arithmetic',
    'speed-based-calculation':  'Speed-Based Calculation',
    'logical-number-puzzles':   'Logical Number Puzzles',
    'verbal-reasoning':         'Verbal Reasoning',
    'english-cem':              'English',
}

PAPERS_DIR = "generated_papers"
FRONTEND_BASE_URL = os.getenv("FRONTEND_BASE_URL", "https://www.autodidact.uk")


# ---------------------------------------------------------------------------
# Helper functions for PDF generation
# ---------------------------------------------------------------------------
def _qr_data_uri(content: str) -> str:
    """Generate QR code as data URI"""
    qr = qrcode.QRCode(box_size=6, border=2)
    qr.add_data(content)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return f"data:image/png;base64,{base64.b64encode(buf.read()).decode()}"


def _html_to_pdf(html: str, path: str) -> None:
    """Convert HTML to PDF using WeasyPrint"""
    os.makedirs(PAPERS_DIR, exist_ok=True)
    HTML(string=html).write_pdf(path)


def _merge_pdfs(input_paths: list, output_path: str) -> None:
    """Merge multiple PDF files into one using pypdf."""
    writer = PdfWriter()
    for path in input_paths:
        reader = PdfReader(path)
        for page in reader.pages:
            writer.add_page(page)
    with open(output_path, "wb") as f:
        writer.write(f)


def _combine_html_docs(question_html: str, answer_html: str) -> str:
    """Merge two full HTML documents into one for a single combined PDF."""
    def _parts(html: str) -> tuple[str, str]:
        style_match = re.search(r"<style>(.*?)</style>", html, re.DOTALL | re.IGNORECASE)
        body_match = re.search(r"<body[^>]*>(.*?)</body>", html, re.DOTALL | re.IGNORECASE)
        return (style_match.group(1) if style_match else "", body_match.group(1) if body_match else "")

    q_style, q_body = _parts(question_html)
    a_style, a_body = _parts(answer_html)
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
{q_style}
{a_style}
</style>
</head>
<body>
{q_body}
<div style="page-break-before: always;"></div>
{a_body}
</body>
</html>
"""


def _score_answers(questions: list, submitted: dict) -> dict:
    """Score submitted answers against stored correct_options."""
    score = 0
    breakdown: dict[str, dict] = {}
    review = []

    for q in questions:
        qid = q['question_id']
        module = q['module_id']
        selected = (submitted.get(qid) or '').upper()
        is_correct = selected == q['correct_option']

        if is_correct:
            score += 1

        # Track by module
        if module not in breakdown:
            breakdown[module] = {'label': MODULE_LABELS.get(module, module), 'score': 0, 'total': 0}
        breakdown[module]['total'] += 1
        if is_correct:
            breakdown[module]['score'] += 1

        # Build review
        review.append({
            'question_number': q['question_number'],
            'question': q['question'],
            'options': q['options'],
            'your_answer': selected,
            'correct_option': q['correct_option'],
            'correct_answer': q.get('correct_answer', q['options'].get(q['correct_option'], '')),
            'explanation': q.get('explanation', ''),
            'is_correct': is_correct
        })

    return {
        'score': score,
        'total': len(questions),
        'percentage': round((score / len(questions)) * 100, 1) if questions else 0,
        'passed': score >= len(questions) * 0.6,
        'breakdown': list(breakdown.values()),
        'review': review
    }


def _save_result(db: Session, test_id: str, user_id: int, score: int, total: int, time_taken: int, answers: dict):
    """Save result to database"""
    result = MockTestResult(
        test_id=test_id,
        user_id=user_id,
        score=score,
        total=total,
        time_taken=time_taken,
        answers_json=answers
    )
    db.add(result)
    db.commit()
    return result


# ---------------------------------------------------------------------------
# Request models
# ---------------------------------------------------------------------------
class GenerateExamRequest(BaseModel):
    user_id: int
    difficulty: str = 'mixed'   # 'easy' | 'medium' | 'hard' | 'mixed'
    exam_style: str = 'standard'  # 'standard' | 'cem' | 'english'
    target_year: str = 'year4'    # 'year4' | 'year5'


class SubmitExamRequest(BaseModel):
    user_id: int
    answers: dict[str, str]   # { "q1": "A", "q2": "C", ... }
    time_taken: int = 0        # seconds elapsed


class CheckTypedRequest(BaseModel):
    user_id: int = 0
    answers: dict[str, str]  # {"q1": "A", "q2": "C", ...}


def _build_section_summary(questions: list[dict]) -> list[dict]:
    """Summarise section composition and suggested timings for generated tests."""
    if not questions:
        return []

    section_counts: dict[str, int] = {}
    section_minutes_hint: dict[str, int] = {}
    for q in questions:
        section = q.get('section_name') or MODULE_LABELS.get(q.get('module_id', ''), 'General')
        section_counts[section] = section_counts.get(section, 0) + 1
        if q.get('section_minutes'):
            section_minutes_hint[section] = int(q['section_minutes'])

    total = len(questions)
    time_minutes = TIME_LIMIT_SECONDS // 60
    summary = []
    for section, count in section_counts.items():
        suggested = section_minutes_hint.get(section) or max(1, round((count / total) * time_minutes))
        summary.append({
            'section_name': section,
            'num_questions': count,
            'suggested_minutes': suggested,
        })
    # stable output, larger sections first
    summary.sort(key=lambda x: x['num_questions'], reverse=True)
    return summary


def _compute_user_weak_modules(db: Session, user_id: int, lookback: int = 10) -> list[str]:
    """Infer weaker modules from recent mock tests for targeted generation."""
    if not user_id:
        return []
    recent_results = (
        db.query(MockTestResult)
        .filter(MockTestResult.user_id == user_id)
        .order_by(MockTestResult.submitted_at.desc())
        .limit(lookback)
        .all()
    )
    if not recent_results:
        return []

    totals: dict[str, int] = {}
    corrects: dict[str, int] = {}
    for res in recent_results:
        test = db.query(MockTest).filter(MockTest.test_id == res.test_id).first()
        if not test:
            continue
        answers = res.answers_json or {}
        for q in test.questions_json:
            module = q.get('module_id')
            qid = q.get('question_id')
            if not module or not qid:
                continue
            totals[module] = totals.get(module, 0) + 1
            selected = (answers.get(qid) or '').upper()
            if selected and selected == q.get('correct_option'):
                corrects[module] = corrects.get(module, 0) + 1

    scored = []
    for module, total in totals.items():
        if total < 4:
            continue
        acc = corrects.get(module, 0) / total
        scored.append((acc, total, module))
    scored.sort(key=lambda x: (x[0], -x[1]))
    return [m for _, _, m in scored[:3]]


def _pick_difficulty(requested: str) -> str:
    if requested == 'mixed':
        return random.choice(['easy'] * 3 + ['medium'] * 4 + ['hard'] * 3)
    return requested


def _normalise_question_text(text: str) -> str:
    cleaned = (text or '').lower()
    cleaned = re.sub(r'\s+', ' ', cleaned)
    cleaned = re.sub(r'[^a-z0-9\s./:%-]', '', cleaned)
    return cleaned.strip()


def _question_signature(q: dict) -> str:
    """
    Template-like signature for anti-repeat:
    - keep module to avoid over-filtering across different skills
    - normalize numbers to # to catch near-duplicate variants of same stem
    """
    module = q.get('module_id', 'unknown')
    stem = _normalise_question_text(q.get('question', ''))
    stem = re.sub(r'\d+(\.\d+)?', '#', stem)
    stem = re.sub(r'#+', '#', stem)
    return f'{module}|{stem}'


def _collect_recent_question_signatures(db: Session, user_id: int, lookback_tests: int = 30) -> tuple[set[str], int]:
    tests = (
        db.query(MockTest)
        .filter(MockTest.user_id == user_id)
        .order_by(MockTest.created_at.desc())
        .limit(lookback_tests)
        .all()
    )
    signatures: set[str] = set()
    for t in tests:
        for q in (t.questions_json or []):
            signatures.add(_question_signature(q))
    return signatures, len(tests)


def _apply_anti_repeat(questions: list[dict], blocked_signatures: set[str], requested_difficulty: str) -> tuple[list[dict], int]:
    """
    Replace repeated / near-duplicate questions against user history and within current paper.
    """
    if not questions:
        return questions, 0

    used_in_paper: set[str] = set()
    replaced = 0
    max_attempts_per_slot = 30

    for idx, q in enumerate(questions):
        sig = _question_signature(q)
        should_replace = sig in blocked_signatures or sig in used_in_paper
        if not should_replace:
            used_in_paper.add(sig)
            continue

        module_id = q.get('module_id')
        replacement = None
        for _ in range(max_attempts_per_slot):
            candidate = generate_mcq(module_id, _pick_difficulty(requested_difficulty))
            candidate_sig = _question_signature(candidate)
            if candidate_sig in blocked_signatures or candidate_sig in used_in_paper:
                continue
            # preserve section metadata where present
            if q.get('section_name'):
                candidate['section_name'] = q.get('section_name')
            if q.get('section_minutes'):
                candidate['section_minutes'] = q.get('section_minutes')
            replacement = candidate
            break

        if replacement is not None:
            questions[idx] = replacement
            used_in_paper.add(_question_signature(replacement))
            replaced += 1
        else:
            # keep original if no viable replacement found
            used_in_paper.add(sig)

    for i, q in enumerate(questions):
        q['question_number'] = i + 1
        q['question_id'] = f'q{i + 1}'
    return questions, replaced


# ---------------------------------------------------------------------------
# Helper: strip correct_option before sending to client
# ---------------------------------------------------------------------------
def _sanitise(q: dict) -> dict:
    return {k: v for k, v in q.items() if k != 'correct_option'}


# ---------------------------------------------------------------------------
# POST /test/generate
# ---------------------------------------------------------------------------
@router.post('/generate')
def generate_test(req: GenerateExamRequest, db: Session = Depends(get_db)):
    if req.difficulty not in ('easy', 'medium', 'hard', 'mixed'):
        raise HTTPException(status_code=400, detail='difficulty must be easy | medium | hard | mixed')
    if req.exam_style not in ('standard', 'cem', 'english'):
        raise HTTPException(status_code=400, detail='exam_style must be standard | cem | english')
    if req.target_year not in ('year4', 'year5'):
        raise HTTPException(status_code=400, detail='target_year must be year4 | year5')

    test_id = f"mt_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{uuid4().hex[:8]}"
    weak_modules = _compute_user_weak_modules(db, req.user_id)
    if req.exam_style != 'english':
        weak_modules = [m for m in weak_modules if m != 'english-cem']

    blocked_signatures, history_count = _collect_recent_question_signatures(db, req.user_id)
    questions = generate_exam(
        NUM_QUESTIONS,
        req.difficulty,
        req.exam_style,
        req.target_year,
        weak_modules,
    )
    anti_repeat_replacements = 0
    if history_count >= 5:
        questions, anti_repeat_replacements = _apply_anti_repeat(
            questions,
            blocked_signatures,
            req.difficulty,
        )
    section_summary = _build_section_summary(questions)

    test = MockTest(
        test_id=test_id,
        user_id=req.user_id,
        questions_json=questions,   # stored with correct_option
    )
    db.add(test)
    db.commit()

    # Return questions WITHOUT the correct_option
    return {
        'test_id': test_id,
        'exam_style': req.exam_style,
        'target_year': req.target_year,
        'weak_focus_modules': weak_modules,
        'anti_repeat': {
            'history_tests_considered': history_count,
            'replacements_made': anti_repeat_replacements,
        },
        'num_questions': NUM_QUESTIONS,
        'time_limit_seconds': TIME_LIMIT_SECONDS,
        'section_summary': section_summary,
        'questions': [_sanitise(q) for q in questions],
    }


# ---------------------------------------------------------------------------
# GET /test/{test_id}   (resume / reload)
# ---------------------------------------------------------------------------
@router.get('/{test_id}')
def get_test(test_id: str, db: Session = Depends(get_db)):
    test = db.query(MockTest).filter_by(test_id=test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail='Test not found')
    exam_style = 'cem' if any(q.get('section_name') for q in test.questions_json) else 'standard'
    if all(q.get('module_id') == 'english-cem' for q in test.questions_json):
        exam_style = 'english'
    return {
        'test_id': test_id,
        'exam_style': exam_style,
        'target_year': 'year5' if exam_style == 'english' else 'year4',
        'num_questions': len(test.questions_json),
        'time_limit_seconds': TIME_LIMIT_SECONDS,
        'section_summary': _build_section_summary(test.questions_json),
        'questions': [_sanitise(q) for q in test.questions_json],
    }


# ---------------------------------------------------------------------------
# POST /test/{test_id}/submit
# ---------------------------------------------------------------------------
@router.post('/{test_id}/submit')
def submit_test(test_id: str, req: SubmitExamRequest, db: Session = Depends(get_db)):
    test = db.query(MockTest).filter_by(test_id=test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail='Test not found')

    questions = test.questions_json
    score = 0
    breakdown: dict[str, dict] = {}
    review = []

    for q in questions:
        qid = q['question_id']
        module = q['module_id']
        selected = req.answers.get(qid, '')
        is_correct = selected.upper() == q['correct_option']
        if is_correct:
            score += 1

        # Per-module tallies
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
    pct = round(score / total * 100)
    passed = pct >= 60

    result = MockTestResult(
        test_id=test_id,
        user_id=req.user_id,
        score=score,
        total=total,
        time_taken=min(req.time_taken, TIME_LIMIT_SECONDS),
        answers_json=req.answers,
    )
    db.add(result)
    db.commit()
    db.refresh(result)

    return {
        'result_id': result.id,
        'score': score,
        'total': total,
        'percentage': pct,
        'passed': passed,
        'time_taken': result.time_taken,
        'breakdown': list(breakdown.values()),
        'review': review,
    }


# ---------------------------------------------------------------------------
# GET /test/results/{user_id}
# ---------------------------------------------------------------------------
@router.get('/results/{user_id}')
def get_user_results(user_id: int, db: Session = Depends(get_db)):
    results = (
        db.query(MockTestResult)
        .filter_by(user_id=user_id)
        .order_by(MockTestResult.submitted_at.desc())
        .limit(20)
        .all()
    )
    return [
        {
            'result_id': r.id,
            'test_id': r.test_id,
            'score': r.score,
            'total': r.total,
            'percentage': round(r.score / r.total * 100),
            'passed': round(r.score / r.total * 100) >= 60,
            'submitted_at': r.submitted_at.isoformat(),
        }
        for r in results
    ]


# ---------------------------------------------------------------------------
# GET /test/generated/{user_id}
# Returns generated tests regardless of submission status
# ---------------------------------------------------------------------------
@router.get('/generated/{user_id}')
def get_generated_tests(user_id: int, db: Session = Depends(get_db)):
    tests = (
        db.query(MockTest)
        .filter(MockTest.user_id == user_id)
        .order_by(MockTest.created_at.desc())
        .limit(100)
        .all()
    )
    submitted_test_ids = {
        r.test_id for r in (
            db.query(MockTestResult)
            .filter(MockTestResult.user_id == user_id)
            .all()
        )
    }

    return [
        {
            'test_id': t.test_id,
            'created_at': t.created_at.isoformat() if t.created_at else None,
            'num_questions': len(t.questions_json or []),
            'status': 'submitted' if t.test_id in submitted_test_ids else 'generated'
        }
        for t in tests
    ]


# ---------------------------------------------------------------------------
# GET /test/{test_id}/question-pdf
# Generates question PDF in the same format as Test section practice papers
# ---------------------------------------------------------------------------
@router.get('/{test_id}/question-pdf')
def get_question_pdf(test_id: str, student_name: str = '', db: Session = Depends(get_db)):
    test = db.query(MockTest).filter(MockTest.test_id == test_id).first()
    if not test:
        raise HTTPException(404, "Test not found")

    questions = [
        {k: v for k, v in q.items() if k not in ('correct_option', 'correct_answer', 'explanation')}
        for q in test.questions_json
    ]
    num_questions = len(questions)
    download_date = datetime.now().strftime('%d/%m/%Y')
    total_pages = num_questions // 3 + (1 if num_questions % 3 else 0) + 4
    paper_id = f"MT-{test_id}"

    question_html = _render_question_html(
        title='Grammar School Mock Test — Mathematics',
        questions=questions,
        student_name=student_name,
        download_date=download_date,
        paper_id=paper_id,
        total_pages=total_pages,
        num_questions=num_questions,
        time_minutes=60,
    )
    qr_url = f"{FRONTEND_BASE_URL}/test/{test_id}/submit"
    qr_img = _qr_data_uri(qr_url)
    answer_html = _render_answer_sheet_html(
        title='Grammar School Mock Test — Mathematics',
        questions=questions,
        student_name=student_name,
        download_date=download_date,
        paper_id=paper_id,
        qr_img=qr_img,
        standalone=True,
    )

    # Generate each section as its own PDF so the answer sheet gets its own
    # page context with a repeating compact header, then merge with pypdf.
    q_pdf_path = os.path.join(PAPERS_DIR, f"{test_id}_q_only.pdf")
    a_pdf_path = os.path.join(PAPERS_DIR, f"{test_id}_a_only.pdf")
    pdf_path   = os.path.join(PAPERS_DIR, f"{test_id}_questions.pdf")
    _html_to_pdf(question_html, q_pdf_path)
    _html_to_pdf(answer_html,   a_pdf_path)
    _merge_pdfs([q_pdf_path, a_pdf_path], pdf_path)
    return FileResponse(pdf_path, media_type="application/pdf", filename=f"{test_id}_questions.pdf")


# ---------------------------------------------------------------------------
# GET /test/{test_id}/answer-sheet-pdf
# ---------------------------------------------------------------------------
@router.get('/{test_id}/answer-sheet-pdf')
def get_answer_sheet_pdf(test_id: str, student_name: str = '', db: Session = Depends(get_db)):
    test = db.query(MockTest).filter(MockTest.test_id == test_id).first()
    if not test:
        raise HTTPException(404, "Test not found")

    qr_url = f"{FRONTEND_BASE_URL}/test/{test_id}/submit"
    qr_img = _qr_data_uri(qr_url)
    download_date = datetime.now().strftime('%d/%m/%Y')
    questions = [
        {k: v for k, v in q.items() if k not in ('correct_option', 'correct_answer', 'explanation')}
        for q in test.questions_json
    ]
    html = _render_answer_sheet_html(
        title='Grammar School Mock Test — Mathematics',
        questions=questions,
        student_name=student_name,
        download_date=download_date,
        paper_id=f"MT-{test_id}",
        qr_img=qr_img,
    )

    pdf_path = os.path.join(PAPERS_DIR, f"{test_id}_answer_sheet.pdf")
    _html_to_pdf(html, pdf_path)
    return FileResponse(pdf_path, media_type="application/pdf", filename=f"{test_id}_answer_sheet.pdf")


# ---------------------------------------------------------------------------
# POST /test/{test_id}/check-upload - OCR answer submission
# ---------------------------------------------------------------------------
@router.post('/{test_id}/check-upload')
async def check_upload(test_id: str, user_id: int = Form(0), file: UploadFile = File(...), db: Session = Depends(get_db)):
    test = db.query(MockTest).filter(MockTest.test_id == test_id).first()
    if not test:
        raise HTTPException(404, "Test not found")

    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    try:
        # Extract answers via OCR
        extracted = extract_answers_from_pdf(tmp_path)
        answers = {f"q{item['question_number']}": item['answer'] for item in extracted}

        # Score answers
        result = _score_answers(test.questions_json, answers)

        # Save result
        _save_result(db, test_id, user_id, result['score'], result['total'], 0, answers)

        return {**result, "ocr_extracted_count": len(extracted)}
    finally:
        os.unlink(tmp_path)


# ---------------------------------------------------------------------------
# POST /test/{test_id}/check-typed - Manual answer entry
# ---------------------------------------------------------------------------
@router.post('/{test_id}/check-typed')
def check_typed(test_id: str, req: CheckTypedRequest, db: Session = Depends(get_db)):
    test = db.query(MockTest).filter(MockTest.test_id == test_id).first()
    if not test:
        raise HTTPException(404, "Test not found")

    result = _score_answers(test.questions_json, req.answers)
    _save_result(db, test_id, req.user_id, result['score'], result['total'], 0, req.answers)
    return result
