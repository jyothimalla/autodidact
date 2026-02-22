from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
import os
import re
import uuid
import tempfile
import shutil
from datetime import datetime

from database import get_db
from model import PracticeAttempt
from generators.mcq_generator import generate_questions_for_module
from routers.grammar_paper_routes import _render_question_html, _render_answer_sheet_html
from utils.pdf_parser import extract_answers_from_pdf

# Import PDF/QR utilities
import base64
import io
import qrcode
from weasyprint import HTML
from jinja2 import Template
from pypdf import PdfWriter, PdfReader

router = APIRouter()

# Configuration
PAPERS_DIR = "generated_papers/practice"
FRONTEND_BASE_URL = os.getenv("FRONTEND_BASE_URL", "https://www.autodidact.uk")

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

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
    os.makedirs(os.path.dirname(path), exist_ok=True)
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

def _generate_question_pdf(questions: list, attempt_id: str, title: str, student_name: str, downloaded_date: str) -> str:
    """Generate Bexley-style question paper with Atom-style answer sheet as final page."""
    qr_url = f"{FRONTEND_BASE_URL}/practice-submit/{attempt_id}"
    qr_data = _qr_data_uri(qr_url)

    template = Template("""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  @page { size: A4; margin: 0; }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: Arial, Helvetica, sans-serif; color: #1a1a1a; }
  .intro-page { padding: 40px 46px 28px; background: #f2f5fb; min-height: 100vh; }
  .intro-title-card { background: #d9e0ec; border-radius: 12px; padding: 22px 24px; margin-bottom: 34px; }
  .intro-logo { font-size: 12px; font-weight: 700; color: #2f8de4; margin-bottom: 8px; }
  .intro-logo span { background: #2f8de4; color: white; border-radius: 3px; padding: 1px 4px; margin-left: 2px; font-size: 10px; }
  .intro-title { font-size: 44px; font-weight: 800; line-height: 1.05; letter-spacing: -0.8px; }
  .intro-section { margin-bottom: 24px; }
  .intro-section h3 { color: #2f8de4; font-size: 31px; margin-bottom: 8px; }
  .intro-section p { color: #303641; font-size: 22px; line-height: 1.45; margin-bottom: 4px; }
  .intro-section ul { margin-left: 22px; }
  .intro-section li { color: #303641; font-size: 22px; line-height: 1.6; }
  .intro-meta { color: #303641; font-size: 22px; margin-top: 8px; }
  .intro-footer-line { margin-top: 26px; border-bottom: 4px solid #2f8de4; }
  .intro-footer { display: flex; justify-content: space-between; color: #8f99a8; font-size: 12px; padding-top: 8px; }
  .question-paper-page { page-break-before: always; }

  /* ── Bexley-style Blue Banner ─────────────────────────────────── */
  .bexley-banner {
    background: #1565C0;
    color: white;
    padding: 14px 20px 12px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .banner-title  { font-size: 17px; font-weight: 700; letter-spacing: 0.4px; }
  .banner-sub    { font-size: 10.5px; opacity: 0.88; margin-top: 3px; }
  .banner-right  { text-align: right; font-size: 11px; opacity: 0.9; line-height: 1.6; }
  .banner-rule   { height: 4px; background: #0D47A1; }

  .page-body { padding: 14px 20px; }

  /* ── Student details strip ──────────────────────────────────────── */
  .student-strip {
    display: flex;
    border: 1px solid #1565C0;
    margin-bottom: 12px;
    font-size: 11px;
  }
  .student-cell { flex: 1; padding: 6px 10px; border-right: 1px solid #1565C0; }
  .student-cell:last-child { border-right: none; }
  .student-cell label { font-weight: 700; color: #1565C0; display: block; margin-bottom: 2px; }
  .student-cell .line { border-bottom: 1px solid #888; min-height: 16px; display: block; }

  /* ── Instructions ───────────────────────────────────────────────── */
  .instructions-box {
    background: #E3F2FD;
    border: 1px solid #90CAF9;
    border-left: 5px solid #1565C0;
    padding: 8px 12px;
    margin-bottom: 14px;
    font-size: 11px;
    line-height: 1.55;
  }
  .instructions-box strong { color: #0D47A1; }
  .instructions-box ul { margin-left: 16px; margin-top: 4px; }
  .instructions-box li { margin-bottom: 3px; }

  /* ── Questions ──────────────────────────────────────────────────── */
  .question-block {
    margin-bottom: 14px;
    page-break-inside: avoid;
    padding: 8px 10px;
    border-bottom: 1px solid #e0e0e0;
  }
  .q-header { display: flex; gap: 8px; align-items: baseline; }
  .q-num {
    background: #1565C0; color: white;
    font-size: 10px; font-weight: 700;
    width: 22px; height: 22px; border-radius: 50%;
    text-align: center; line-height: 22px; flex-shrink: 0;
  }
  .q-text { font-size: 12px; line-height: 1.5; }
  .options-row {
    display: flex; flex-wrap: wrap; gap: 6px 18px;
    margin-top: 6px; margin-left: 30px;
  }
  .opt { font-size: 11px; color: #333; display: flex; gap: 4px; align-items: center; }
  .opt-lbl {
    background: #E3F2FD; color: #1565C0; font-weight: 700; font-size: 10px;
    border: 1px solid #90CAF9; border-radius: 3px;
    padding: 1px 5px; min-width: 18px; text-align: center;
  }

  .end-marker {
    border-top: 2px solid #1565C0; margin-top: 20px; padding-top: 8px;
    display: flex; justify-content: space-between;
    font-size: 10px; color: #555;
  }
  .end-text { font-weight: 700; font-size: 12px; color: #1565C0; }

  /* ── Answer Sheet (new page — two-column card grid) ────────────── */
  .answer-sheet-page { page-break-before: always; }
  .as-page-header { display: flex; justify-content: space-between; align-items: center; padding: 10px 20px 8px; border-bottom: 2px solid #1565C0; }
  .as-page-title { font-size: 14px; font-weight: 700; }
  .as-logo { background: #1565C0; color: white; font-weight: 700; font-size: 10px; padding: 3px 10px; border-radius: 4px; }
  .as-meta { display: flex; justify-content: space-between; align-items: flex-start; padding: 8px 20px 4px; }
  .as-fields { font-size: 10.5px; }
  .as-field-row { margin-bottom: 5px; display: flex; align-items: baseline; gap: 8px; }
  .as-field-label { color: #1565C0; font-weight: 700; min-width: 65px; display: inline-block; }
  .as-field-line { border-bottom: 1px solid #aaa; min-width: 160px; display: inline-block; min-height: 13px; }
  .as-field-val { color: #1565C0; font-weight: 700; font-size: 10.5px; }
  .as-qr-block { background: #E3F2FD; padding: 6px 8px; border-radius: 6px; text-align: center; max-width: 140px; }
  .as-qr-block img { width: 80px; height: 80px; display: block; margin: 0 auto 3px; }
  .as-qr-block p { font-size: 7.5px; color: #444; line-height: 1.4; }
  .as-instruction { padding: 6px 20px; font-size: 11px; font-weight: 700; }
  .rect-sample { display: inline-block; width: 10px; height: 4px; border: 2px solid #000; vertical-align: middle; }
  .as-divider { height: 2px; background: #1565C0; margin: 0 0 6px; }
  .as-cards-grid { display: grid; grid-template-columns: repeat(8, 1fr); gap: 5px; padding: 0 14px 14px; }
  .as-card { border: 1px solid #b3c8e8; border-radius: 3px; overflow: hidden; break-inside: avoid; }
  .as-card-hdr { background: #1565C0; color: white; font-weight: 700; font-size: 9px; padding: 3px 6px; text-align: center; }
  .as-card-body { display: flex; }
  .as-opt-col { flex: 1; background: #E3EEFF; border-right: 1px solid #c0d0ee; overflow: hidden; min-width: 0; }
  .as-opt-text { font-size: 7px; color: #1a1a1a; padding: 1px 3px; border-bottom: 1px solid #cdd8f0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; min-height: 13px; line-height: 13px; }
  .as-opt-text:last-child { border-bottom: none; }
  .as-rect-col { background: #F0F5FF; width: 26px; flex-shrink: 0; display: flex; flex-direction: column; }
  .as-rect-cell { display: flex; align-items: center; justify-content: center; border-bottom: 1px solid #cdd8f0; min-height: 13px; flex: 1; }
  .as-rect-cell:last-child { border-bottom: none; }
  .as-rect { display: inline-block; width: 18px; height: 6px; border: 1.5px solid #1565C0; border-radius: 1px; }
</style>
</head>
<body>
<div class="intro-page">
  <div class="intro-title-card">
    <div class="intro-logo">autodidact<span>uk</span></div>
    <div class="intro-title">Grammar School Paper</div>
  </div>

  <div class="intro-section">
    <h3>About this test</h3>
    <p>This is a practice paper designed to familiarise your child with the types of questions they will see in a Grammar School entrance examination.</p>
    <div class="intro-meta">Paper ID: {{ attempt_id }} | {{ questions|length }} Questions | 60 Minutes</div>
  </div>

  <div class="intro-section">
    <h3>What you'll need</h3>
    <ul>
      <li>Printed practice paper and answer sheet</li>
      <li>Pencil</li>
      <li>Rubber</li>
      <li>Timer</li>
    </ul>
  </div>

  <div class="intro-section">
    <h3>Taking the test</h3>
    <p>Your child should mark their answers on the answer sheet, not in the question paper.</p>
    <p>On the answer sheet, record answers by drawing a clear line through the answer box with a pencil.</p>
    <p>Mistakes should be rubbed out and not crossed out.</p>
  </div>

  <div class="intro-footer-line"></div>
  <div class="intro-footer">
    <span>autodidact.uk</span>
    <span>{{ title }}</span>
  </div>
</div>

<div class="question-paper-page">

<!-- ── Question Paper ──────────────────────────────────────────────── -->
<div class="bexley-banner">
  <div>
    <div class="banner-title">Grammar School Selection Test — Mathematics</div>
    <div class="banner-sub">Autodidact Practice Paper &nbsp;|&nbsp; Test ID: {{ attempt_id }}</div>
  </div>
  <div class="banner-right">
    {{ questions|length }} Questions<br>
    Do NOT open until told to do so
  </div>
</div>
<div class="banner-rule"></div>

<div class="page-body">
  <div class="student-strip">
    <div class="student-cell">
      <label>Candidate Name</label><span class="line">{{ student_name }}</span>
    </div>
    <div class="student-cell">
      <label>Date</label><span class="line">{{ downloaded_date }}</span>
    </div>
    <div class="student-cell" style="max-width:100px;">
      <label>Score</label>
      <span class="line">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/ {{ questions|length }}</span>
    </div>
  </div>

  <div class="instructions-box">
    <strong>Instructions &mdash; read carefully before you start:</strong>
    <ul>
      <li>Mark your answers on the <strong>Answer Sheet</strong> at the back of this booklet.</li>
      <li>For each question, circle or shade ONE letter only: <strong>A, B, C or D</strong>.</li>
      <li>If you change your mind, cross out your first answer clearly and shade the correct one.</li>
      <li>Calculators are <strong>NOT</strong> permitted.</li>
      <li>Work quickly and carefully — marks are only awarded for correct answers.</li>
    </ul>
  </div>

  {% for q in questions %}
  <div class="question-block">
    <div class="q-header">
      <div class="q-num">{{ q.question_number }}</div>
      <div class="q-text">{{ q.question }}</div>
    </div>
    <div class="options-row">
      {% for lbl in ['A', 'B', 'C', 'D'] %}
      <div class="opt">
        <span class="opt-lbl">{{ lbl }}</span>
        <span>{{ q.options[lbl] }}</span>
      </div>
      {% endfor %}
    </div>
  </div>
  {% endfor %}

  <div class="end-marker">
    <span>autodidact.uk</span>
    <span class="end-text">END OF QUESTIONS — See Answer Sheet overleaf</span>
    <span>&copy; Autodidact</span>
  </div>
</div>

<!-- ── Answer Sheet (same PDF, new page — two-column card grid) ───── -->
<div class="answer-sheet-page">
  <div class="as-page-header">
    <div class="as-page-title">Answer Sheet — Grammar School Mock Test</div>
    <div class="as-logo">Autodidact</div>
  </div>

  <div class="as-meta">
    <div class="as-fields">
      <div class="as-field-row">
        <span class="as-field-label">Name</span>
        <span class="as-field-line">{{ student_name }}</span>
      </div>
      <div class="as-field-row">
        <span class="as-field-label">Date</span>
        <span class="as-field-line">{{ downloaded_date }}</span>
      </div>
      <div class="as-field-row">
        <span class="as-field-label">Test name</span>
        <span class="as-field-val">Grammar School Mock Test — Mathematics</span>
      </div>
    </div>
    <div class="as-qr-block">
      <img src="{{ qr_data }}" alt="QR Code">
      <p>Scan this QR code to add your answers on Autodidact and get your results</p>
    </div>
  </div>

  <div class="as-instruction">
    Draw a line clearly through the rectangle next to your answer, like <span class="rect-sample"></span>.
  </div>
  <div class="as-divider"></div>

  <div class="as-cards-grid">
    {% for q in questions %}
    <div class="as-card">
      <div class="as-card-hdr">{{ q.question_number }}</div>
      <div class="as-card-body">
        <div class="as-opt-col">
          {% for lbl in ['A', 'B', 'C', 'D'] %}
          <div class="as-opt-text">{{ q.options[lbl] }}</div>
          {% endfor %}
        </div>
        <div class="as-rect-col">
          {% for lbl in ['A', 'B', 'C', 'D'] %}
          <div class="as-rect-cell"><span class="as-rect"></span></div>
          {% endfor %}
        </div>
      </div>
    </div>
    {% endfor %}
  </div>

  <div class="end-marker" style="margin: 0 20px 14px 20px;">
    <span>autodidact.uk</span>
    <span class="end-text">END OF ANSWER SHEET</span>
    <span>&copy; Autodidact</span>
  </div>
</div>

</div>
</body>
</html>
    """)

    html = template.render(
        questions=questions,
        attempt_id=attempt_id,
        title=title,
        qr_data=qr_data,
        student_name=student_name,
        downloaded_date=downloaded_date
    )
    pdf_path = os.path.join(PAPERS_DIR, f"{attempt_id}_questions.pdf")
    _html_to_pdf(html, pdf_path)
    return pdf_path

def _generate_answer_sheet_pdf(questions: list, attempt_id: str, title: str, student_name: str, downloaded_date: str) -> str:
    """Generate standalone answer sheet PDF."""
    pdf_path = os.path.join(PAPERS_DIR, f"{attempt_id}_answer_sheet.pdf")
    qr_url = f"{FRONTEND_BASE_URL}/practice-submit/{attempt_id}"
    qr_data = _qr_data_uri(qr_url)

    template = Template("""
<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
  @page { size: A4; margin: 0; }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: Arial, Helvetica, sans-serif; color: #1a1a1a; padding-top: 28px; }
  .as-running-hdr {
    position: fixed; top: 0; left: 0; right: 0;
    height: 26px; background: #1565C0; color: white;
    display: flex; justify-content: space-between; align-items: center;
    padding: 0 16px; font-size: 8px; font-weight: 700; z-index: 1000;
  }
  .as-running-title { font-size: 9px; }
  .as-running-logo { background: rgba(255,255,255,0.2); padding: 2px 8px; border-radius: 3px; }
  .as-page-header { display: flex; justify-content: space-between; align-items: center; padding: 10px 20px 8px; border-bottom: 2px solid #1565C0; }
  .as-page-title { font-size: 14px; font-weight: 700; }
  .as-logo { background: #1565C0; color: white; font-weight: 700; font-size: 10px; padding: 3px 10px; border-radius: 4px; }
  .as-meta { display: flex; justify-content: space-between; align-items: flex-start; padding: 8px 20px 4px; }
  .as-fields { font-size: 10.5px; }
  .as-field-row { margin-bottom: 5px; display: flex; align-items: baseline; gap: 8px; }
  .as-field-label { color: #1565C0; font-weight: 700; min-width: 65px; display: inline-block; }
  .as-field-line { border-bottom: 1px solid #aaa; min-width: 160px; display: inline-block; min-height: 13px; }
  .as-field-val { color: #1565C0; font-weight: 700; font-size: 10.5px; }
  .as-qr-block { background: #E3F2FD; padding: 6px 8px; border-radius: 6px; text-align: center; max-width: 140px; }
  .as-qr-block img { width: 80px; height: 80px; display: block; margin: 0 auto 3px; }
  .as-qr-block p { font-size: 7.5px; color: #444; line-height: 1.4; }
  .as-instruction { padding: 6px 20px; font-size: 11px; font-weight: 700; }
  .rect-sample { display: inline-block; width: 10px; height: 4px; border: 2px solid #000; vertical-align: middle; }
  .as-divider { height: 2px; background: #1565C0; margin: 0 0 6px; }
  .as-cards-grid { display: grid; grid-template-columns: repeat(8, 1fr); gap: 5px; padding: 0 14px 14px; }
  .as-card { border: 1px solid #b3c8e8; border-radius: 3px; overflow: hidden; break-inside: avoid; }
  .as-card-hdr { background: #1565C0; color: white; font-weight: 700; font-size: 9px; padding: 3px 6px; text-align: center; }
  .as-card-body { display: flex; }
  .as-opt-col { flex: 1; background: #E3EEFF; border-right: 1px solid #c0d0ee; overflow: hidden; min-width: 0; }
  .as-opt-text { font-size: 7px; color: #1a1a1a; padding: 1px 3px; border-bottom: 1px solid #cdd8f0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; min-height: 13px; line-height: 13px; }
  .as-opt-text:last-child { border-bottom: none; }
  .as-rect-col { background: #F0F5FF; width: 26px; flex-shrink: 0; display: flex; flex-direction: column; }
  .as-rect-cell { display: flex; align-items: center; justify-content: center; border-bottom: 1px solid #cdd8f0; min-height: 13px; flex: 1; }
  .as-rect-cell:last-child { border-bottom: none; }
  .as-rect { display: inline-block; width: 18px; height: 6px; border: 1.5px solid #1565C0; border-radius: 1px; }
  .end-marker { border-top: 2px solid #1565C0; margin: 0 20px 14px; padding-top: 8px; display: flex; justify-content: space-between; font-size: 10px; color: #555; }
  .end-text { font-weight: 700; font-size: 12px; color: #1565C0; }
</style></head><body>

  <div class="as-running-hdr">
    <span class="as-running-title">Answer Sheet — Grammar School Mock Test &nbsp;|&nbsp; Test ID: {{ attempt_id }}</span>
    <span class="as-running-logo">Autodidact</span>
  </div>

  <div class="as-page-header">
    <div class="as-page-title">Answer Sheet — Grammar School Mock Test</div>
    <div class="as-logo">Autodidact</div>
  </div>
  <div class="as-meta">
    <div class="as-fields">
      <div class="as-field-row"><span class="as-field-label">Name</span><span class="as-field-line">{{ student_name }}</span></div>
      <div class="as-field-row"><span class="as-field-label">Date</span><span class="as-field-line">{{ downloaded_date }}</span></div>
      <div class="as-field-row"><span class="as-field-label">Test name</span><span class="as-field-val">Grammar School Mock Test — Mathematics</span></div>
    </div>
    <div class="as-qr-block">
      <img src="{{ qr_data }}" alt="QR Code">
      <p>Scan this QR code to add your answers on Autodidact and get your results</p>
    </div>
  </div>
  <div class="as-instruction">
    Draw a line clearly through the rectangle next to your answer, like <span class="rect-sample"></span>.
  </div>
  <div class="as-divider"></div>
  <div class="as-cards-grid">
    {% for q in questions %}
    <div class="as-card">
      <div class="as-card-hdr">{{ q.question_number }}</div>
      <div class="as-card-body">
        <div class="as-opt-col">
          {% for lbl in ['A', 'B', 'C', 'D'] %}
          <div class="as-opt-text">{{ q.options[lbl] }}</div>
          {% endfor %}
        </div>
        <div class="as-rect-col">
          {% for lbl in ['A', 'B', 'C', 'D'] %}
          <div class="as-rect-cell"><span class="as-rect"></span></div>
          {% endfor %}
        </div>
      </div>
    </div>
    {% endfor %}
  </div>
  <div class="end-marker">
    <span>autodidact.uk</span>
    <span class="end-text">END OF ANSWER SHEET</span>
    <span>&copy; Autodidact</span>
  </div>

</body></html>
    """)
    html = template.render(
        questions=questions,
        attempt_id=attempt_id,
        title=title,
        qr_data=qr_data,
        student_name=student_name,
        downloaded_date=downloaded_date
    )
    _html_to_pdf(html, pdf_path)
    return pdf_path

def _score_answers(questions: list, submitted: dict) -> dict:
    """Score submitted answers"""
    score = 0
    review = []

    for q in questions:
        qid = q.get('question_id') or f"q{q['question_number']}"
        selected = (submitted.get(qid) or '').upper()
        is_correct = selected == q['correct_option']

        if is_correct:
            score += 1

        review.append({
            'question_number': q['question_number'],
            'question': q['question'],
            'options': q['options'],
            'your_answer': selected,
            'correct_option': q['correct_option'],
            'correct_answer': q['options'].get(q['correct_option'], ''),
            'explanation': q.get('explanation', ''),
            'is_correct': is_correct
        })

    total = len(questions)
    percentage = round((score / total) * 100, 1) if total > 0 else 0

    return {
        'score': score,
        'total': total,
        'percentage': percentage,
        'passed': percentage >= 60,
        'review': review
    }


def _normalise_submitted_answers(questions: list, submitted: dict) -> dict:
    """
    Accept either question_id keys or q<number> keys and normalize to question_id keys.
    This keeps manual and OCR submissions compatible with different frontend formats.
    """
    if not submitted:
        return {}

    by_question_id = {q.get('question_id'): q for q in questions if q.get('question_id')}
    by_qnum = {str(q.get('question_number')): q.get('question_id') for q in questions if q.get('question_number') is not None}

    normalized: dict[str, str] = {}
    for raw_key, raw_val in submitted.items():
        if raw_val is None:
            continue
        key = str(raw_key)
        val = str(raw_val).strip().upper()
        if not val:
            continue

        # Already a question_id
        if key in by_question_id:
            normalized[key] = val
            continue

        # q12 -> 12
        if key.lower().startswith('q') and key[1:].isdigit():
            mapped = by_qnum.get(key[1:])
            if mapped:
                normalized[mapped] = val
            continue

        # plain numeric key "12"
        if key.isdigit():
            mapped = by_qnum.get(key)
            if mapped:
                normalized[mapped] = val

    return normalized

# ============================================================================
# API ROUTES
# ============================================================================

class GenerateRequest(BaseModel):
    user_id: int
    subject_id: str
    module_id: str
    topic_id: Optional[str] = None
    level: int = 1
    attempt_type: str = 'practice'  # 'practice' or 'challenge'
    mode: str = 'online'  # 'online' or 'download'
    num_questions: int = 5
    difficulty: str = 'mixed'
    time_limit: Optional[int] = None

@router.post("/generate")
def generate_practice_challenge(req: GenerateRequest, db: Session = Depends(get_db)):
    """Generate practice or challenge questions"""

    num_questions = req.num_questions

    # Determine which generator key to use.
    # Some modules (e.g. 'python-programming') are parent containers whose
    # children are the real generator keys (e.g. 'python-with-karel').
    # Fall back to topic_id when module_id has no direct generator.
    from generators.custom_generators import MODULE_GENERATORS
    generator_key = req.module_id
    if generator_key not in MODULE_GENERATORS and req.topic_id and req.topic_id in MODULE_GENERATORS:
        generator_key = req.topic_id

    # Generate questions using MCQ generator
    questions = generate_questions_for_module(generator_key, num_questions, req.difficulty)

    # Create attempt ID
    attempt_id = f"{req.attempt_type}_{req.module_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:8]}"

    # Save to database
    attempt = PracticeAttempt(
        attempt_id=attempt_id,
        user_id=req.user_id,
        subject_id=req.subject_id,
        module_id=req.module_id,
        topic_id=req.topic_id,
        level=req.level,
        attempt_type=req.attempt_type,
        mode=req.mode,
        num_questions=num_questions,
        questions_json=questions,
        answers_json=None,
        score=None,
        percentage=None
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    return {
        "attempt_id": attempt_id,
        "paper_id": attempt_id,
        "num_questions": num_questions,
        "questions": questions if req.mode == 'online' else [],
        "mode": req.mode
    }

@router.get("/{attempt_id}/details")
def get_attempt_details(attempt_id: str, db: Session = Depends(get_db)):
    """Get attempt details (for submission page)"""
    attempt = db.query(PracticeAttempt).filter(PracticeAttempt.attempt_id == attempt_id).first()
    if not attempt:
        raise HTTPException(404, "Attempt not found")

    questions_for_display = [
        {k: v for k, v in q.items() if k not in ('correct_option', 'correct_answer', 'explanation')}
        for q in attempt.questions_json
    ]

    return {
        "attempt_id": attempt.attempt_id,
        "num_questions": attempt.num_questions,
        "attempt_type": attempt.attempt_type,
        "module_id": attempt.module_id,
        "status": "submitted" if attempt.submitted_at else "pending",
        "questions": questions_for_display,
    }

@router.get("/{attempt_id}/question-pdf")
def get_question_pdf(attempt_id: str, student_name: str = '', db: Session = Depends(get_db)):
    """Download questions PDF"""
    attempt = db.query(PracticeAttempt).filter(PracticeAttempt.attempt_id == attempt_id).first()
    if not attempt:
        raise HTTPException(404, "Attempt not found")

    title = f"{attempt.attempt_type.title()} - {attempt.module_id.replace('-', ' ').title()}"
    download_date = datetime.now().strftime('%d/%m/%Y')
    questions = [
        {k: v for k, v in q.items() if k not in ('correct_option', 'correct_answer', 'explanation')}
        for q in attempt.questions_json
    ]
    num_questions = len(questions)
    # No cover/instructions pages for practice — questions start immediately
    total_pages = num_questions // 3 + (1 if num_questions % 3 else 0) + 2
    paper_id = f"PR-{attempt_id}"
    question_html = _render_question_html(
        title=title,
        questions=questions,
        student_name=student_name,
        download_date=download_date,
        paper_id=paper_id,
        total_pages=total_pages,
        num_questions=num_questions,
        time_minutes=60,
        show_preamble=False,
    )
    qr_url = f"{FRONTEND_BASE_URL}/practice-submit/{attempt_id}"
    qr_img = _qr_data_uri(qr_url)
    # standalone=True so the answer sheet gets its own page context with a
    # repeating compact header on every page (name/date/paper-id + QR).
    answer_html = _render_answer_sheet_html(
        title=title,
        questions=questions,
        student_name=student_name,
        download_date=download_date,
        paper_id=paper_id,
        qr_img=qr_img,
        standalone=True,
    )

    # Generate each section as its own PDF so WeasyPrint gives the answer
    # sheet its own page context (enabling the fixed repeating header),
    # then merge with pypdf.
    os.makedirs(PAPERS_DIR, exist_ok=True)
    q_pdf_path = os.path.join(PAPERS_DIR, f"{attempt_id}_q_only.pdf")
    a_pdf_path = os.path.join(PAPERS_DIR, f"{attempt_id}_a_only.pdf")
    pdf_path   = os.path.join(PAPERS_DIR, f"{attempt_id}_questions.pdf")

    _html_to_pdf(question_html, q_pdf_path)
    _html_to_pdf(answer_html,   a_pdf_path)
    _merge_pdfs([q_pdf_path, a_pdf_path], pdf_path)

    return FileResponse(pdf_path, media_type="application/pdf", filename=f"{attempt_id}_questions.pdf")

@router.get("/{attempt_id}/answer-sheet-pdf")
def get_answer_sheet_pdf(attempt_id: str, student_name: str = '', db: Session = Depends(get_db)):
    """Download answer sheet PDF with QR code"""
    attempt = db.query(PracticeAttempt).filter(PracticeAttempt.attempt_id == attempt_id).first()
    if not attempt:
        raise HTTPException(404, "Attempt not found")

    title = f"{attempt.attempt_type.title()} - {attempt.module_id.replace('-', ' ').title()}"
    download_date = datetime.now().strftime('%d/%m/%Y')
    questions = [
        {k: v for k, v in q.items() if k not in ('correct_option', 'correct_answer', 'explanation')}
        for q in attempt.questions_json
    ]
    qr_url = f"{FRONTEND_BASE_URL}/practice-submit/{attempt_id}"
    qr_img = _qr_data_uri(qr_url)
    html = _render_answer_sheet_html(
        title=title,
        questions=questions,
        student_name=student_name,
        download_date=download_date,
        paper_id=f"PR-{attempt_id}",
        qr_img=qr_img,
    )
    pdf_path = os.path.join(PAPERS_DIR, f"{attempt_id}_answer_sheet.pdf")
    _html_to_pdf(html, pdf_path)

    return FileResponse(pdf_path, media_type="application/pdf", filename=f"{attempt_id}_answer_sheet.pdf")

class SubmitAnswersRequest(BaseModel):
    answers: dict  # {"q1": "A", "q2": "C", ...}

@router.post("/{attempt_id}/submit")
def submit_answers(attempt_id: str, req: SubmitAnswersRequest, db: Session = Depends(get_db)):
    """Submit answers for an attempt (online mode)"""
    attempt = db.query(PracticeAttempt).filter(PracticeAttempt.attempt_id == attempt_id).first()
    if not attempt:
        raise HTTPException(404, "Attempt not found")

    normalized_answers = _normalise_submitted_answers(attempt.questions_json, req.answers)
    result = _score_answers(attempt.questions_json, normalized_answers)

    # Update attempt
    attempt.answers_json = normalized_answers
    attempt.score = result['score']
    attempt.percentage = result['percentage']
    attempt.submitted_at = datetime.utcnow()
    db.commit()

    return {
        "attempt_id": attempt_id,
        **result
    }

@router.post("/{attempt_id}/submit-upload")
async def submit_upload(attempt_id: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Submit scanned answer sheet (OCR mode)"""
    attempt = db.query(PracticeAttempt).filter(PracticeAttempt.attempt_id == attempt_id).first()
    if not attempt:
        raise HTTPException(404, "Attempt not found")

    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    try:
        extracted = extract_answers_from_pdf(tmp_path)
        extracted_answers = {f"q{item['question_number']}": item['answer'] for item in extracted}
        normalized_answers = _normalise_submitted_answers(attempt.questions_json, extracted_answers)

        # Score the answers
        result = _score_answers(attempt.questions_json, normalized_answers)

        # Update attempt
        attempt.answers_json = normalized_answers
        attempt.score = result['score']
        attempt.percentage = result['percentage']
        attempt.submitted_at = datetime.utcnow()
        db.commit()

        return {
            "attempt_id": attempt_id,
            **result,
            "ocr_extracted_count": len(normalized_answers)
        }
    finally:
        os.unlink(tmp_path)

@router.get("/history/{user_id}")
def get_user_history(user_id: int, subject_id: Optional[str] = None, db: Session = Depends(get_db)):
    """Get practice/challenge history for a user"""
    query = db.query(PracticeAttempt).filter(PracticeAttempt.user_id == user_id)

    if subject_id:
        query = query.filter(PracticeAttempt.subject_id == subject_id)

    attempts = query.order_by(PracticeAttempt.created_at.desc()).all()

    return [
        {
            "attempt_id": a.attempt_id,
            "paper_id": a.attempt_id,
            "subject_id": a.subject_id,
            "module_id": a.module_id,
            "topic_id": a.topic_id,
            "level": a.level,
            "attempt_type": a.attempt_type,
            "mode": a.mode,
            "num_questions": a.num_questions,
            "difficulty": "mixed",
            "score": a.score,
            "percentage": a.percentage,
            "created_at": a.created_at.isoformat() if a.created_at else None,
            "submitted_at": a.submitted_at.isoformat() if a.submitted_at else None,
            "status": "submitted" if a.submitted_at else "pending"
        }
        for a in attempts
    ]

@router.get("/analytics/{user_id}")
def get_user_analytics(user_id: int, db: Session = Depends(get_db)):
    """Get analytics data for user's practice attempts"""
    attempts = db.query(PracticeAttempt).filter(
        PracticeAttempt.user_id == user_id,
        PracticeAttempt.submitted_at.isnot(None)
    ).all()

    # Group by subject
    by_subject = {}
    for a in attempts:
        if a.subject_id not in by_subject:
            by_subject[a.subject_id] = {
                'total_attempts': 0,
                'total_score': 0,
                'total_questions': 0,
                'avg_percentage': 0,
                'by_module': {}
            }

        by_subject[a.subject_id]['total_attempts'] += 1
        by_subject[a.subject_id]['total_score'] += a.score or 0
        by_subject[a.subject_id]['total_questions'] += a.num_questions

        # By module
        if a.module_id not in by_subject[a.subject_id]['by_module']:
            by_subject[a.subject_id]['by_module'][a.module_id] = {
                'attempts': 0,
                'score': 0,
                'total': 0
            }

        by_subject[a.subject_id]['by_module'][a.module_id]['attempts'] += 1
        by_subject[a.subject_id]['by_module'][a.module_id]['score'] += a.score or 0
        by_subject[a.subject_id]['by_module'][a.module_id]['total'] += a.num_questions

    # Calculate averages
    for subject in by_subject.values():
        if subject['total_questions'] > 0:
            subject['avg_percentage'] = round((subject['total_score'] / subject['total_questions']) * 100, 1)

        for module in subject['by_module'].values():
            if module['total'] > 0:
                module['percentage'] = round((module['score'] / module['total']) * 100, 1)

    return by_subject
