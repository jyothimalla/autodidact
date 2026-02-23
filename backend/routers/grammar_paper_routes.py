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
    'verbal-reasoning':         'Verbal Reasoning',
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


def _render_question_html(*, title, questions, student_name, download_date,
                          paper_id, total_pages, num_questions, time_minutes,
                          show_preamble=True):
    """Render a Bexley Selection Test style question paper HTML."""
    return Template(r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  @page { size: A4; margin: 15mm 20mm; }
  body { font-family: Arial, Helvetica, sans-serif; margin: 0; padding: 0; color: #222; }

  /* ── Cover Page ───────────────────────────────── */
  .cover-page { page-break-after: always; }
  .cover-banner {
    background: #e8f0fe;
    border-radius: 12px;
    padding: 30px 35px 25px;
    margin-bottom: 40px;
  }
  .cover-brand {
    font-size: 13px;
    font-weight: 700;
    color: #2196F3;
    margin-bottom: 8px;
  }
  .cover-brand span {
    background: #2196F3;
    color: white;
    padding: 2px 6px;
    border-radius: 3px;
    margin-left: 2px;
  }
  .cover-title {
    font-size: 32px;
    font-weight: 900;
    color: #111;
    line-height: 1.2;
    margin: 0;
  }
  .cover-section { margin-bottom: 30px; }
  .cover-section h2 { font-size: 18px; color: #2196F3; margin: 0 0 10px; font-weight: 700; }
  .cover-section p { font-size: 15px; color: #333; line-height: 1.6; margin: 0 0 6px; }
  .cover-section ul { margin: 0; padding-left: 24px; }
  .cover-section ul li { font-size: 15px; color: #333; line-height: 1.8; }
  .cover-meta { font-size: 13px; color: #888; margin-top: 6px; }

  /* ── Page Header/Footer ───────────────────────── */
  .page-header-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #f0f4ff;
    padding: 8px 16px;
    border-radius: 6px;
    margin-bottom: 20px;
    font-size: 13px;
    color: #555;
  }
  .page-header-bar .brand {
    font-weight: 700;
    color: #2196F3;
  }
  .page-header-bar .brand span {
    background: #2196F3;
    color: white;
    padding: 1px 5px;
    border-radius: 3px;
    margin-left: 1px;
  }
  .page-footer {
    border-top: 3px solid #2196F3;
    margin-top: 30px;
    padding-top: 8px;
    display: flex;
    justify-content: space-between;
    font-size: 11px;
    color: #999;
  }

  /* ── Instructions Page ────────────────────────── */
  .instructions-page { page-break-after: always; }
  .instructions-page h2 { font-size: 22px; font-weight: 900; color: #222; margin: 20px 0 20px; }
  .instructions-page ol { padding-left: 28px; margin: 0; }
  .instructions-page ol li {
    font-size: 15px;
    line-height: 1.8;
    margin-bottom: 12px;
    color: #333;
  }
  .instructions-page ol li strong { color: #000; }

  /* ── Student Info Bar ─────────────────────────── */
  .student-info-bar {
    display: flex;
    gap: 30px;
    margin: 20px 0 30px;
    font-size: 15px;
  }
  .student-info-bar label { font-weight: 600; color: #2196F3; font-size: 13px; display: block; margin-bottom: 2px; }
  .student-info-bar .info-value {
    border-bottom: 2px solid #333;
    min-width: 180px;
    display: inline-block;
    padding: 4px 8px;
    font-weight: 500;
    font-size: 15px;
  }

  /* ── Questions ────────────────────────────────── */
  .question-block {
    page-break-inside: avoid;
    margin-bottom: 0;
    padding: 20px 0;
    border-bottom: 2px solid #e0e0e0;
  }
  .question-block:last-child { border-bottom: none; }
  .q-row {
    display: flex;
    gap: 16px;
    align-items: flex-start;
  }
  .q-num {
    font-size: 28px;
    font-weight: 900;
    color: #2196F3;
    min-width: 45px;
    line-height: 1;
    padding-top: 2px;
  }
  .q-body { flex: 1; }
  .q-body .q-text {
    font-size: 15px;
    font-weight: 500;
    line-height: 1.7;
    margin: 0 0 12px;
    color: #222;
  }
  .q-options {
    display: flex;
    flex-wrap: wrap;
    gap: 6px 28px;
    font-size: 15px;
  }
  .q-options .opt {
    padding: 2px 0;
    line-height: 1.6;
  }
  .q-options .opt .opt-label {
    font-weight: 700;
    color: #2196F3;
    margin-right: 4px;
  }

  /* ── Continue prompt ──────────────────────────── */
  .continue-prompt {
    text-align: center;
    margin-top: 30px;
    font-size: 14px;
    font-weight: 600;
    color: #2196F3;
  }
  .continue-prompt .arrow { font-weight: 900; margin-left: 6px; }

  /* ── End of test ──────────────────────────────── */
  .end-of-test {
    text-align: center;
    font-size: 18px;
    font-weight: 900;
    color: #222;
    margin-top: 50px;
    padding-top: 20px;
    border-top: 3px solid #222;
  }
</style>
</head>
<body>

{% if show_preamble %}
<!-- ═══ COVER PAGE ═══ -->
<div class="cover-page">
  <div class="cover-banner">
    <div class="cover-brand">autodidact<span>uk</span></div>
    <h1 class="cover-title">{{ title }}</h1>
  </div>

  <div class="cover-section">
    <h2>About this test</h2>
    <p>This is a practice paper designed to familiarise your child with the types of questions they will see in a Grammar School entrance examination.</p>
    <p class="cover-meta">Paper ID: {{ paper_id }} &nbsp;|&nbsp; {{ num_questions }} Questions &nbsp;|&nbsp; {{ time_minutes }} Minutes</p>
  </div>

  <div class="cover-section">
    <h2>What you'll need</h2>
    <ul>
      <li>Printed practice paper and answer sheet</li>
      <li>Pencil</li>
      <li>Rubber</li>
      <li>Timer</li>
    </ul>
  </div>

  <div class="cover-section">
    <h2>Taking the test</h2>
    <p>Your child should mark their answers on the answer sheet, not in the question paper. This is good practice for the real exam which will have a separate answer sheet.</p>
    <p>On the answer sheet, your child should record their answers by drawing a clear line through the answer box with a pencil. Mistakes should be rubbed out and not crossed out.</p>
  </div>

  <div class="page-footer">
    <span>autodidact.uk</span>
    <span>Page 1 of {{ total_pages }}</span>
  </div>
</div>

<!-- ═══ INSTRUCTIONS PAGE ═══ -->
<div class="instructions-page">
  <div class="page-header-bar">
    <span>{{ title }}</span>
    <span class="brand">autodidact<span>uk</span></span>
  </div>

  <h2>Read the following carefully:</h2>
  <ol>
    <li>This test has been designed to help you practise the types of questions you will see in a Grammar School entrance exam.</li>
    <li>You have <strong>{{ time_minutes }} minutes</strong> to complete this paper.</li>
    <li>Read each question carefully before moving onto the next one.</li>
    <li>Answers should be marked on the <strong>answer sheets</strong> provided. If you make a mistake, rub it out as completely as you can and mark your new answer.</li>
    <li>You may find some of the questions difficult. If you cannot do a question, <strong>do not waste time on it but go on to the next</strong>. If you are not sure of an answer, choose the one you think is best.</li>
    <li>Work as quickly and as carefully as you can.</li>
  </ol>

  <div class="page-footer">
    <span>autodidact.uk</span>
    <span>Page 2 of {{ total_pages }}</span>
  </div>
</div>
{% endif %}

<!-- ═══ STUDENT INFO + QUESTIONS ═══ -->
{% set page_num = [3] %}
{% for q in questions %}
  {% if loop.first %}
  <div class="page-header-bar">
    <span>{{ title }}</span>
    <span class="brand">autodidact<span>uk</span></span>
  </div>
  <div class="student-info-bar">
    <div><label>Name</label><span class="info-value">{{ student_name }}</span></div>
    <div><label>Date</label><span class="info-value">{{ download_date }}</span></div>
    <div><label>Paper ID</label><span class="info-value">{{ paper_id }}</span></div>
  </div>
  {% endif %}

  <div class="question-block">
    <div class="q-row">
      <div class="q-num">{{ loop.index }}</div>
      <div class="q-body">
        <p class="q-text">{{ q.question }}</p>
        <div class="q-options">
          {% for lbl, val in q.options.items() %}
          <span class="opt"><span class="opt-label">{{ lbl }}</span> {{ val }}</span>
          {% endfor %}
        </div>
      </div>
    </div>
  </div>
{% endfor %}

<div class="end-of-test">END OF TEST</div>

<div class="page-footer">
  <span>autodidact.uk</span>
  <span>{{ title }}</span>
</div>

</body>
</html>
""").render(
        title=title, questions=questions, student_name=student_name,
        download_date=download_date, paper_id=paper_id,
        total_pages=total_pages, num_questions=num_questions,
        time_minutes=time_minutes, show_preamble=show_preamble,
    )


def _render_answer_sheet_html(*, title, questions, student_name, download_date,
                              paper_id, qr_img, standalone=True):
    """Render Atom-style answer sheet HTML.

    standalone=True  → header is position:fixed so it repeats on every page (use for
                        standalone answer-sheet PDFs).
    standalone=False → header is static / normal flow (use when embedding inside a
                        combined question+answer PDF via _combine_html_docs, to avoid
                        the fixed element bleeding onto question paper pages).
    """
    return Template(r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: Arial, Helvetica, sans-serif; color: #222; }
{% if standalone %}
  @page {
    size: A4;
    margin: 24mm 10mm 10mm 10mm;
    /* Running element fills the full top margin box on every page */
    @top-left { content: element(page-hdr); }
  }

  /* ── Compact page header: running element — lives in the top margin box,
     never overlaps page content, repeats on every page ── */
  .as-page-hdr {
    position: running(page-hdr);
    width: 100%;
    background: white; border-bottom: 2.5px solid #1f6fff;
    padding: 2.5mm 10mm;
  }
  /* Two-column table: left = stacked Name/Date/Test name, right = QR */
  .as-hdr-inner { width: 100%; border-collapse: collapse; }
  .as-hdr-inner td { vertical-align: middle; padding: 0; }
  /* Left cell: Name, Date, Test Name stacked vertically */
  .as-hdr-left { width: 100%; }
  .as-hdr-row { display: block; line-height: 1.5; }
  .as-hdr-lbl {
    font-size: 8px; font-weight: 700; color: #1f6fff;
    text-transform: uppercase; letter-spacing: 0.5px;
    display: inline; margin-right: 5px;
  }
  .as-hdr-val { font-size: 11px; font-weight: 600; color: #111; display: inline; }
  /* QR cell: image on top, hint text centred below */
  .as-hdr-qr-cell { text-align: center; vertical-align: middle; width: 60px; }
  .as-hdr-qr-cell img { width: 48px; height: 48px; display: block; margin: 0 auto 2px; }
  .as-hdr-qr-hint {
    display: block; font-size: 7px; color: #555;
    line-height: 1.2; text-align: center;
  }

  /* ── First-page title block (normal flow, appears once on page 1) ── */
  /* Use a table so "Answer Sheet — Title" sits left and brand sits right cleanly */
  .as-first-title-wrap { border-bottom: 3px solid #1f6fff; padding-bottom: 5px; margin-bottom: 6px; }
  .as-first-title-inner { width: 100%; border-collapse: collapse; }
  .as-first-title-inner td { vertical-align: bottom; padding: 0; }
  .as-first-title-inner .brand-cell { text-align: right; white-space: nowrap; }
  .as-main-title { font-size: 17px; font-weight: 800; color: #111; }
  .as-brand { font-size: 13px; font-weight: 700; color: #1f6fff; }
  .as-brand .home { background: #1f6fff; color: white; padding: 2px 6px; border-radius: 2px; margin-left: 2px; }
  .as-instruction { font-size: 13px; font-weight: 700; margin: 4px 0 3px; }
  .line-example { display: inline-block; width: 20px; height: 6px; border: 2.5px solid #1f6fff; border-radius: 1px; vertical-align: middle; }
  .as-divider { height: 2px; background: #1f6fff; margin-bottom: 6px; }

{% else %}
  @page { size: A4; margin: 10mm; }
  /* ── Embedded: static header ─────────────────────────────────── */
  .as-title-row {
    display: flex; justify-content: space-between; align-items: center;
    padding-bottom: 6px; border-bottom: 3px solid #1f6fff; margin-bottom: 10px;
  }
  .as-main-title { font-size: 20px; font-weight: 800; color: #111; }
  .as-brand { font-size: 14px; font-weight: 700; color: #1f6fff; }
  .as-brand .home { background: #1f6fff; color: white; padding: 2px 7px; border-radius: 2px; margin-left: 2px; }
  .as-info-row { display: flex; justify-content: space-between; align-items: flex-start; gap: 14px; margin-bottom: 8px; }
  .as-student-section { flex: 1; }
  .as-labels-row { display: flex; gap: 50px; margin-bottom: 3px; }
  .as-vals-row   { display: flex; gap: 50px; margin-bottom: 8px; }
  .as-info-label { color: #1f6fff; font-size: 13px; font-weight: 700; min-width: 90px; display: block; }
  .as-info-value { font-size: 15px; min-width: 90px; display: block; }
  .as-test-name  { font-size: 16px; font-weight: 600; color: #111; }
  .as-qr-box { background: #e9f1ff; border: 1px solid #c8dcff; padding: 8px 10px; display: flex; gap: 10px; align-items: center; width: 240px; flex-shrink: 0; }
  .as-qr-box img { width: 76px; height: 76px; display: block; flex-shrink: 0; }
  .as-qr-box p   { font-size: 12px; line-height: 1.4; color: #2e3a4a; }
  .as-instruction { font-size: 17px; font-weight: 800; margin: 6px 0 5px; }
  .line-example { display: inline-block; width: 22px; height: 7px; border: 2.5px solid #1f6fff; border-radius: 1px; vertical-align: middle; }
  .as-divider { height: 2px; background: #1f6fff; margin-bottom: 0; }
  .as-hdr { margin-bottom: 10px; }
{% endif %}


  /* ── Cards grid ──────────────────────────────────────────────── */
  .as-cards-grid {
    display: grid;
    grid-template-columns: repeat(7, minmax(0, 1fr));
    gap: 6px;
    padding-top: 6px;
  }
  .as-card {
    border-top: 1px solid #c0d0f0;
    border-bottom: 1px solid #c0d0f0;
    border-right: 1px solid #c0d0f0;
    border-left: 3px solid #1f6fff;
    background: #f4f8ff;
    break-inside: avoid; page-break-inside: avoid;
  }
  .as-card-hdr {
    background: #1f6fff; color: #fff;
    font-weight: 700; font-size: 14px; padding: 3px 5px;
  }
  .as-card-body { padding: 4px 5px 6px; }
  /* Table layout for option rows — more reliable than flex in WeasyPrint */
  .as-option-row { display: table; width: 100%; padding: 2px 0; }
  .as-opt-text {
    display: table-cell; font-size: 11.5px; line-height: 1.3;
    color: #111; vertical-align: middle; padding-right: 4px;
    word-break: break-word;
  }
  .as-box-cell { display: table-cell; vertical-align: middle; width: 18px; }
  .as-box {
    width: 18px; height: 10px;
    border: 2px solid #1f6fff; background: #fff;
    display: block;
  }

  /* ── Footer ──────────────────────────────────────────────────── */
  .as-end-footer {
    border-top: 2px solid #1f6fff; margin-top: 12px; padding-top: 8px;
    font-size: 18px; font-weight: 900; color: #222;
    text-align: center;
  }
</style>
</head>
<body>

{% if standalone %}
<!-- Compact page header: position:fixed repeats on every page.
     Full table layout — no flexbox inside fixed elements in WeasyPrint. -->
<div class="as-page-hdr">
  <table class="as-hdr-inner">
    <tr>
      <td class="as-hdr-left">
        <span class="as-hdr-row"><span class="as-hdr-lbl">Name:</span><span class="as-hdr-val">{{ student_name }}</span></span>
        <span class="as-hdr-row"><span class="as-hdr-lbl">Date:</span><span class="as-hdr-val">{{ download_date }}</span></span>
        <span class="as-hdr-row"><span class="as-hdr-lbl">Test:</span><span class="as-hdr-val">{{ title }}</span></span>
      </td>
      <td class="as-hdr-qr-cell">
        <img src="{{ qr_img }}" alt="QR Code">
        <span class="as-hdr-qr-hint">Scan to submit online</span>
      </td>
    </tr>
  </table>
</div>
<!-- First-page title + instruction: table ensures title and brand stay on one line -->
<div class="as-first-title-wrap">
  <table class="as-first-title-inner">
    <tr>
      <td><h1 class="as-main-title">Answer Sheet — {{ title }}</h1></td>
      <td class="brand-cell"><span class="as-brand">Atom <span class="home">Home</span></span></td>
    </tr>
  </table>
</div>
<div class="as-instruction">
  Draw a line clearly through the rectangle next to your answer, like <span class="line-example"></span>.
</div>
<div class="as-divider"></div>
<!-- Answer cards grid -->
<div class="as-cards-grid">
  {% for q in questions %}
  <div class="as-card">
    <div class="as-card-hdr">{{ loop.index }}</div>
    <div class="as-card-body">
    {% for lbl, val in q.options.items() %}
      <div class="as-option-row">
        <span class="as-opt-text">{{ lbl }}. {{ val }}</span>
        <span class="as-box-cell"><span class="as-box"></span></span>
      </div>
    {% endfor %}
    </div>
  </div>
  {% endfor %}
</div>
<div class="as-end-footer">END OF TEST</div>
{% else %}
<!-- Embedded (combined PDF): static header -->
<div class="as-hdr">
  <div class="as-title-row">
    <h1 class="as-main-title">Answer Sheet - {{ title }}</h1>
    <span class="as-brand">Atom <span class="home">Home</span></span>
  </div>
  <div class="as-info-row">
    <div class="as-student-section">
      <div class="as-labels-row">
        <span class="as-info-label">Name</span>
        <span class="as-info-label">Date</span>
      </div>
      <div class="as-vals-row">
        <span class="as-info-value">{{ student_name }}</span>
        <span class="as-info-value">{{ download_date }}</span>
      </div>
      <span class="as-info-label">Test name</span>
      <div class="as-test-name">{{ title }}</div>
    </div>
    <div class="as-qr-box">
      <img src="{{ qr_img }}" alt="QR Code">
      <p>Scan this QR code to add your answers from this test on Atom and get your results</p>
    </div>
  </div>
  <div class="as-instruction">
    Draw a line clearly through the rectangle next to your answer, like <span class="line-example"></span>.
  </div>
  <div class="as-divider"></div>
</div>
<div style="padding-top: 6px;">
  <div class="as-cards-grid">
    {% for q in questions %}
    <div class="as-card">
      <div class="as-card-hdr">{{ loop.index }}</div>
      <div class="as-card-body">
      {% for lbl, val in q.options.items() %}
        <div class="as-option-row">
          <div class="as-opt-text">{{ lbl }}. {{ val }}</div>
          <span class="as-box"></span>
        </div>
      {% endfor %}
      </div>
    </div>
    {% endfor %}
  </div>
  <div class="as-end-footer">END OF TEST</div>
</div>
{% endif %}

</body>
</html>
""").render(
        title=title, questions=questions, student_name=student_name,
        download_date=download_date, paper_id=paper_id, qr_img=qr_img,
        standalone=standalone,
    )


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
def download_question_pdf(n: int, student_name: str = "", db: Session = Depends(get_db)):
    from fastapi.responses import FileResponse
    from datetime import datetime

    paper = db.query(GrammarPaper).filter_by(paper_number=n).first()
    if not paper:
        raise HTTPException(status_code=404, detail=f'Paper {n} not found.')

    questions = [_strip_answer(q) for q in paper.questions_json]
    download_date = datetime.now().strftime("%d/%m/%Y")
    paper_id = f"GP-{n:03d}"
    total_pages = len(questions) // 3 + (1 if len(questions) % 3 else 0) + 2  # cover + instructions + question pages

    html = _render_question_html(
        title=paper.title, questions=questions, student_name=student_name,
        download_date=download_date, paper_id=paper_id, total_pages=total_pages,
        num_questions=len(questions), time_minutes=60
    )

    filename = f"Grammar_Paper_{n}_questions.pdf"
    path = os.path.join(PAPERS_DIR, filename)
    _html_to_pdf(html, path)
    return FileResponse(path, filename=filename, media_type="application/pdf")


# ---------------------------------------------------------------------------
# GET /grammar/papers/{n}/answer-sheet-pdf
# ---------------------------------------------------------------------------
@router.get('/papers/{n}/answer-sheet-pdf')
def download_answer_sheet_pdf(n: int, student_name: str = "", db: Session = Depends(get_db)):
    from fastapi.responses import FileResponse
    from datetime import datetime

    paper = db.query(GrammarPaper).filter_by(paper_number=n).first()
    if not paper:
        raise HTTPException(status_code=404, detail=f'Paper {n} not found.')

    qr_url = f"{FRONTEND_BASE_URL}/test-papers/{n}/submit"
    qr_img = _qr_data_uri(qr_url)
    download_date = datetime.now().strftime("%d/%m/%Y")
    paper_id = f"GP-{n:03d}"

    html = _render_answer_sheet_html(
        title=paper.title, questions=paper.questions_json,
        student_name=student_name, download_date=download_date,
        paper_id=paper_id, qr_img=qr_img,
    )

    filename = f"Grammar_Paper_{n}_answer_sheet.pdf"
    path = os.path.join(PAPERS_DIR, filename)
    _html_to_pdf(html, path)
    return FileResponse(path, filename=filename, media_type="application/pdf")


# ---------------------------------------------------------------------------
# GET /grammar/papers/{n}/combined-pdf (Questions + Answer Sheet in ONE file)
# ---------------------------------------------------------------------------
@router.get('/papers/{n}/combined-pdf')
def download_combined_pdf(n: int, student_name: str = "", db: Session = Depends(get_db)):
    """Generate a single PDF with cover page, instructions, questions, and answer sheet"""
    from fastapi.responses import FileResponse
    from datetime import datetime

    paper = db.query(GrammarPaper).filter_by(paper_number=n).first()
    if not paper:
        raise HTTPException(status_code=404, detail=f'Paper {n} not found.')

    questions = [_strip_answer(q) for q in paper.questions_json]
    download_date = datetime.now().strftime("%d/%m/%Y")
    qr_url = f"{FRONTEND_BASE_URL}/test-papers/{n}/submit"
    qr_img = _qr_data_uri(qr_url)
    paper_id = f"GP-{n:03d}"
    total_pages = len(questions) // 3 + (1 if len(questions) % 3 else 0) + 4  # cover + instructions + questions + answer sheets

    # Build the question section HTML
    question_html = _render_question_html(
        title=paper.title, questions=questions, student_name=student_name,
        download_date=download_date, paper_id=paper_id,
        total_pages=total_pages, num_questions=len(questions), time_minutes=60,
    )

    # Build the answer sheet HTML
    answer_html = _render_answer_sheet_html(
        title=paper.title, questions=paper.questions_json,
        student_name=student_name, download_date=download_date,
        paper_id=paper_id, qr_img=qr_img,
        standalone=False,
    )

    # Combine both: strip the <html>/<head>/<body> tags from answer_html and inject after questions
    # Simple approach: render both into the same document
    combined_html = Template(r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  @page { size: A4; margin: 15mm 18mm; }
  body { font-family: Arial, Helvetica, sans-serif; margin: 0; padding: 0; color: #222; }

  /* ── Cover Page ───────────────────────────── */
  .cover-page { page-break-after: always; }
  .cover-banner {
    background: #e8f0fe;
    border-radius: 12px;
    padding: 30px 35px 25px;
    margin-bottom: 40px;
  }
  .cover-brand {
    font-size: 13px;
    font-weight: 700;
    color: #2196F3;
    margin-bottom: 8px;
  }
  .cover-brand span {
    background: #2196F3;
    color: white;
    padding: 2px 6px;
    border-radius: 3px;
    margin-left: 2px;
  }
  .cover-title {
    font-size: 32px;
    font-weight: 900;
    color: #111;
    line-height: 1.2;
    margin: 0;
  }
  .cover-section { margin-bottom: 30px; }
  .cover-section h2 { font-size: 18px; color: #2196F3; margin: 0 0 10px; font-weight: 700; }
  .cover-section p { font-size: 15px; color: #333; line-height: 1.6; margin: 0 0 6px; }
  .cover-section ul { margin: 0; padding-left: 24px; }
  .cover-section ul li { font-size: 15px; color: #333; line-height: 1.8; }
  .cover-meta { font-size: 13px; color: #888; margin-top: 6px; }

  /* ── Page Header/Footer ───────────────────────── */
  .page-header-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #f0f4ff;
    padding: 8px 16px;
    border-radius: 6px;
    margin-bottom: 20px;
    font-size: 13px;
    color: #555;
  }
  .page-header-bar .brand {
    font-weight: 700;
    color: #2196F3;
  }
  .page-header-bar .brand span {
    background: #2196F3;
    color: white;
    padding: 1px 5px;
    border-radius: 3px;
    margin-left: 1px;
  }
  .page-footer {
    border-top: 3px solid #2196F3;
    margin-top: 30px;
    padding-top: 8px;
    display: flex;
    justify-content: space-between;
    font-size: 11px;
    color: #999;
  }

  /* ── Instructions Page ────────────────────────── */
  .instructions-page { page-break-after: always; }
  .instructions-page h2 { font-size: 22px; font-weight: 900; color: #222; margin: 20px 0 20px; }
  .instructions-page ol { padding-left: 28px; margin: 0; }
  .instructions-page ol li {
    font-size: 15px;
    line-height: 1.8;
    margin-bottom: 12px;
    color: #333;
  }
  .instructions-page ol li strong { color: #000; }

  /* ── Student Info Bar ─────────────────────────── */
  .student-info-bar {
    display: flex;
    gap: 30px;
    margin: 20px 0 30px;
    font-size: 15px;
  }
  .student-info-bar label { font-weight: 600; color: #2196F3; font-size: 13px; display: block; margin-bottom: 2px; }
  .student-info-bar .info-value {
    border-bottom: 2px solid #333;
    min-width: 180px;
    display: inline-block;
    padding: 4px 8px;
    font-weight: 500;
    font-size: 15px;
  }

  /* ── Questions ────────────────────────────────── */
  .question-block {
    page-break-inside: avoid;
    margin-bottom: 0;
    padding: 20px 0;
    border-bottom: 2px solid #e0e0e0;
  }
  .question-block:last-child { border-bottom: none; }
  .q-row {
    display: flex;
    gap: 16px;
    align-items: flex-start;
  }
  .q-num {
    font-size: 28px;
    font-weight: 900;
    color: #2196F3;
    min-width: 45px;
    line-height: 1;
    padding-top: 2px;
  }
  .q-body { flex: 1; }
  .q-body .q-text {
    font-size: 15px;
    font-weight: 500;
    line-height: 1.7;
    margin: 0 0 12px;
    color: #222;
  }
  .q-options {
    display: flex;
    flex-wrap: wrap;
    gap: 6px 28px;
    font-size: 15px;
  }
  .q-options .opt {
    padding: 2px 0;
    line-height: 1.6;
  }
  .q-options .opt .opt-label {
    font-weight: 700;
    color: #2196F3;
    margin-right: 4px;
  }
  .end-of-test {
    text-align: center;
    font-size: 18px;
    font-weight: 900;
    color: #222;
    margin-top: 50px;
    padding-top: 20px;
    border-top: 3px solid #222;
  }

  /* ── Answer Sheet ─────────────────────────────── */
  .answer-sheet-section { page-break-before: always; }
  .as-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 16px;
    padding-bottom: 16px;
    border-bottom: 3px solid #2196F3;
  }
  .as-header h1 {
    font-size: 20px;
    font-weight: 900;
    margin: 0;
    color: #111;
  }
  .as-brand {
    font-size: 13px;
    font-weight: 700;
    color: #2196F3;
  }
  .as-brand span {
    background: #2196F3;
    color: white;
    padding: 1px 5px;
    border-radius: 3px;
    margin-left: 1px;
  }
  .as-info-row {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 20px;
  }
  .as-student-info { flex: 1; }
  .as-student-info .info-line {
    margin-bottom: 10px;
    font-size: 14px;
  }
  .as-student-info .info-line label {
    font-weight: 700;
    color: #2196F3;
    display: inline-block;
    min-width: 80px;
  }
  .as-student-info .info-line span {
    border-bottom: 2px solid #333;
    min-width: 180px;
    display: inline-block;
    padding: 2px 8px;
  }
  .as-qr-box {
    text-align: center;
    border: 2px solid #ccc;
    padding: 10px;
    border-radius: 8px;
    background: #fafafa;
  }
  .as-qr-box img { width: 100px; height: 100px; display: block; margin: 0 auto 6px; }
  .as-qr-box p { font-size: 10px; color: #666; margin: 0; line-height: 1.3; }
  .as-instructions {
    font-size: 14px;
    font-weight: 700;
    color: #222;
    margin-bottom: 16px;
    padding: 10px 0;
    border-bottom: 2px solid #e0e0e0;
  }
  .as-instructions .line-example {
    display: inline-block;
    width: 30px;
    height: 3px;
    background: #333;
    vertical-align: middle;
    margin: 0 4px;
  }
  .as-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(70px, 1fr));
    gap: 6px;
    margin-bottom: 20px;
  }
  .as-cell {
    border: 2px solid #bbdefb;
    border-radius: 4px;
    padding: 6px 4px;
    text-align: left;
    font-size: 12px;
    background: white;
  }
  .as-cell-header {
    background: #e3f2fd;
    font-weight: 700;
    font-size: 13px;
    color: #1565c0;
    padding: 3px 6px;
    margin: -6px -4px 6px;
    border-radius: 2px 2px 0 0;
    border-bottom: 1px solid #bbdefb;
  }
  .as-option-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 2px 4px;
    font-size: 12px;
  }
  .as-option-row .opt-text { flex: 1; }
  .as-checkbox {
    display: inline-block;
    width: 16px;
    height: 16px;
    border: 2px solid #333;
    background: white;
    flex-shrink: 0;
  }
  .as-footer {
    margin-top: 20px;
    text-align: center;
    font-size: 18px;
    font-weight: 900;
    color: #222;
  }
</style>
</head>
<body>

<!-- ═══ COVER PAGE ═══ -->
<div class="cover-page">
  <div class="cover-banner">
    <div class="cover-brand">autodidact<span>uk</span></div>
    <h1 class="cover-title">{{ title }}</h1>
  </div>
  <div class="cover-section">
    <h2>About this test</h2>
    <p>This is a practice paper designed to familiarise your child with the types of questions they will see in a Grammar School entrance examination.</p>
    <p class="cover-meta">Paper ID: {{ paper_id }} | {{ num_questions }} Questions | {{ time_minutes }} Minutes</p>
  </div>
  <div class="cover-section">
    <h2>What you'll need</h2>
    <ul>
      <li>Printed practice paper and answer sheet</li>
      <li>Pencil</li>
      <li>Rubber</li>
      <li>Timer</li>
    </ul>
  </div>
  <div class="cover-section">
    <h2>Taking the test</h2>
    <p>Your child should mark their answers on the answer sheet, not in the question paper.</p>
    <p>On the answer sheet, record answers by drawing a clear line through the answer box with a pencil. Mistakes should be rubbed out and not crossed out.</p>
  </div>
  <div class="page-footer">
    <span>autodidact.uk</span>
    <span>{{ title }}</span>
  </div>
</div>

<!-- ═══ INSTRUCTIONS PAGE ═══ -->
<div class="instructions-page">
  <div class="page-header-bar">
    <span>{{ title }}</span>
    <span class="brand">autodidact<span>uk</span></span>
  </div>
  <h2>Read the following carefully:</h2>
  <ol>
    <li>This test has been designed to help you practise the types of questions you will see in a Grammar School entrance exam.</li>
    <li>You have <strong>{{ time_minutes }} minutes</strong> to complete this paper.</li>
    <li>Read each question carefully before moving onto the next one.</li>
    <li>Answers should be marked on the <strong>answer sheets</strong> provided. If you make a mistake, rub it out as completely as you can and mark your new answer.</li>
    <li>You may find some of the questions difficult. If you cannot do a question, <strong>do not waste time on it but go on to the next</strong>. If you are not sure of an answer, choose the one you think is best.</li>
    <li>Work as quickly and as carefully as you can.</li>
  </ol>
  <div class="page-footer">
    <span>autodidact.uk</span>
    <span>{{ title }}</span>
  </div>
</div>

<!-- ═══ QUESTIONS ═══ -->
<div class="page-header-bar">
  <span>{{ title }}</span>
  <span class="brand">autodidact<span>uk</span></span>
</div>
<div class="student-info-bar">
  <div><label>Name</label><span class="info-value">{{ student_name }}</span></div>
  <div><label>Date</label><span class="info-value">{{ download_date }}</span></div>
  <div><label>Paper ID</label><span class="info-value">{{ paper_id }}</span></div>
</div>

{% for q in questions %}
<div class="question-block">
  <div class="q-row">
    <div class="q-num">{{ loop.index }}</div>
    <div class="q-body">
      <p class="q-text">{{ q.question }}</p>
      <div class="q-options">
        {% for lbl, val in q.options.items() %}
        <span class="opt"><span class="opt-label">{{ lbl }}</span> {{ val }}</span>
        {% endfor %}
      </div>
    </div>
  </div>
</div>
{% endfor %}

<div class="end-of-test">END OF TEST</div>
<div class="page-footer">
  <span>autodidact.uk</span>
  <span>{{ title }}</span>
</div>

<!-- ═══ ANSWER SHEET ═══ -->
<div class="answer-sheet-section">
  <div class="as-header">
    <h1>Answer Sheet - {{ title }}</h1>
    <span class="as-brand">autodidact<span>uk</span></span>
  </div>
  <div class="as-info-row">
    <div class="as-student-info">
      <div class="info-line"><label>Name</label><span>{{ student_name }}</span></div>
      <div class="info-line"><label>Date</label><span>{{ download_date }}</span></div>
      <div class="info-line"><label>Test name</label><span>{{ title }}</span></div>
    </div>
    <div class="as-qr-box">
      <img src="{{ qr_img }}" alt="QR Code">
      <p>Scan this QR code to<br>submit your answers<br>and get your results</p>
    </div>
  </div>
  <div class="as-instructions">
    Draw a line clearly through the rectangle next to your answer, like <span class="line-example"></span>.
  </div>
  <div class="as-grid">
    {% for q in all_questions %}
    <div class="as-cell">
      <div class="as-cell-header">{{ loop.index }}</div>
      {% for lbl, val in q.options.items() %}
      <div class="as-option-row">
        <span class="opt-text">{{ lbl }}{% if val|length <= 12 %} {{ val }}{% endif %}</span>
        <span class="as-checkbox"></span>
      </div>
      {% endfor %}
    </div>
    {% endfor %}
  </div>
  <div class="as-footer">END OF TEST</div>
</div>

</body>
</html>
""").render(
        title=paper.title,
        questions=questions,
        all_questions=paper.questions_json,
        qr_img=qr_img,
        student_name=student_name,
        download_date=download_date,
        paper_id=paper_id,
        num_questions=len(questions),
        time_minutes=60,
    )

    filename = f"Grammar_Paper_{n}_complete.pdf"
    path = os.path.join(PAPERS_DIR, filename)
    _html_to_pdf(combined_html, path)
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
