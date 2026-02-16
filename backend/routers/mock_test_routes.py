"""
Grammar-school mock exam endpoints.
  POST /test/generate          → create 50-question MCQ exam
  GET  /test/{test_id}         → fetch questions (no correct_option sent to client)
  POST /test/{test_id}/submit  → score and persist result
  GET  /test/results/{user_id} → list past results for a user
"""
from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from generators.mcq_generator import generate_exam
from model import MockTest, MockTestResult

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
}


# ---------------------------------------------------------------------------
# Request models
# ---------------------------------------------------------------------------
class GenerateExamRequest(BaseModel):
    user_id: int
    difficulty: str = 'mixed'   # 'easy' | 'medium' | 'hard' | 'mixed'


class SubmitExamRequest(BaseModel):
    user_id: int
    answers: dict[str, str]   # { "q1": "A", "q2": "C", ... }
    time_taken: int = 0        # seconds elapsed


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

    test_id = f"mt_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{uuid4().hex[:8]}"
    questions = generate_exam(NUM_QUESTIONS, req.difficulty)

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
        'num_questions': NUM_QUESTIONS,
        'time_limit_seconds': TIME_LIMIT_SECONDS,
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
    return {
        'test_id': test_id,
        'num_questions': len(test.questions_json),
        'time_limit_seconds': TIME_LIMIT_SECONDS,
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
