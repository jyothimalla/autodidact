"""
MCQ wrapper around custom_generators.
Takes a free-answer question and adds 3 plausible wrong answers,
returning A/B/C/D options with a shuffled correct answer.
"""
import random
import re
from generators.custom_generators import generate_question, MODULE_GENERATORS

MODULES = list(MODULE_GENERATORS.keys())
DIFFICULTIES = ['easy', 'medium', 'hard']


# ---------------------------------------------------------------------------
# Distractor helpers
# ---------------------------------------------------------------------------

def _numeric_distractors(correct_val: int | float, count: int = 3) -> list:
    """Generate plausible numeric wrong answers near the correct value."""
    distractors = set()
    offsets = [
        int(correct_val * 0.5) or 1,
        int(correct_val * 1.5) or 2,
        int(correct_val * 0.75) or 1,
        int(correct_val * 1.25) or 2,
        correct_val + random.randint(1, max(2, abs(int(correct_val)) // 5 + 1)),
        correct_val - random.randint(1, max(2, abs(int(correct_val)) // 5 + 1)),
        correct_val + random.choice([-2, -1, 1, 2]) * random.randint(2, 10),
        correct_val * 2,
    ]
    for o in offsets:
        v = int(o) if isinstance(correct_val, int) else round(float(o), 4)
        if v != correct_val and v not in distractors and v > 0:
            distractors.add(v)
        if len(distractors) >= count:
            break

    # fallback: sequential offsets
    delta = 1
    while len(distractors) < count:
        candidate = correct_val + delta
        if candidate != correct_val and candidate not in distractors and candidate > 0:
            distractors.add(candidate)
        candidate = correct_val - delta
        if candidate != correct_val and candidate not in distractors and candidate > 0:
            distractors.add(candidate)
        delta += 1

    return list(distractors)[:count]


def _extract_number(text: str):
    """Pull the first number (int or float) out of an answer string."""
    text = text.replace('£', '').replace(',', '').strip()
    m = re.search(r'-?\d+(\.\d+)?', text)
    if m:
        val = m.group()
        return float(val) if '.' in val else int(val)
    return None


def _fraction_distractors(answer: str, count: int = 3) -> list:
    """Generate wrong fraction strings."""
    m = re.match(r'(\d+)/(\d+)', answer.strip())
    if not m:
        return []
    n, d = int(m.group(1)), int(m.group(2))
    candidates = [
        f'{n + 1}/{d}', f'{n}/{d + 1}', f'{n - 1}/{d}' if n > 1 else f'{n + 2}/{d}',
        f'{n * 2}/{d * 2}', f'{d}/{n}', f'{n}/{d - 1}' if d > 2 else f'{n}/{d + 2}',
    ]
    seen = set()
    result = []
    for c in candidates:
        if c != answer and c not in seen:
            seen.add(c)
            result.append(c)
        if len(result) >= count:
            break
    return result


def _ratio_distractors(answer: str, count: int = 3) -> list:
    """Wrong ratio simplifications."""
    m = re.match(r'(\d+)\s*:\s*(\d+)', answer.strip())
    if not m:
        return []
    a, b = int(m.group(1)), int(m.group(2))
    candidates = [
        f'{a + 1} : {b}', f'{a} : {b + 1}', f'{b} : {a}',
        f'{a * 2} : {b * 2}', f'{a + 1} : {b + 1}',
    ]
    seen = set()
    result = []
    for c in candidates:
        norm = c.replace(' ', '')
        if norm != answer.replace(' ', '') and norm not in seen:
            seen.add(norm)
            result.append(c)
        if len(result) >= count:
            break
    return result


def _make_distractors(answer: str, module_id: str) -> list:
    """Return 3 wrong answer strings for a given correct answer."""
    answer = str(answer).strip()

    # Try fraction pattern first
    if '/' in answer and not answer.startswith('£'):
        ds = _fraction_distractors(answer)
        if ds:
            return ds

    # Try ratio pattern
    if ':' in answer:
        ds = _ratio_distractors(answer)
        if ds:
            return ds

    # Try numeric extraction
    num = _extract_number(answer)
    if num is not None:
        wrong_nums = _numeric_distractors(num)
        prefix = '£' if '£' in answer else ''
        return [f'{prefix}{int(v) if isinstance(v, float) and v == int(v) else v}' for v in wrong_nums]

    # Text answers (e.g., "Estimate: 120 (exact: 117)") — grab key number
    nums = re.findall(r'\d+', answer)
    if nums:
        base = int(nums[0])
        wrong = _numeric_distractors(base)
        return [re.sub(r'\d+', str(int(w)), answer, count=1) for w in wrong[:3]]

    # Last resort: shuffle characters / append noise
    return [answer + ' (approx)', str(random.randint(1, 99)), str(random.randint(100, 500))]


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def generate_mcq(module_id: str, difficulty: str = 'medium') -> dict:
    """
    Generate one MCQ question for the given module.
    Returns:
      {
        module_id, question, options: {A,B,C,D},
        correct_option: 'A'|'B'|'C'|'D',
        correct_answer, explanation
      }
    """
    q = generate_question(module_id, difficulty)
    correct = str(q['answer']).strip()
    distractors = _make_distractors(correct, module_id)

    # Build pool: 1 correct + 3 distractors, shuffle
    pool = [correct] + distractors[:3]
    while len(pool) < 4:
        pool.append(str(random.randint(1, 100)))
    random.shuffle(pool)

    labels = ['A', 'B', 'C', 'D']
    options = {labels[i]: str(pool[i]) for i in range(4)}
    correct_option = labels[pool.index(correct)]

    return {
        'module_id': module_id,
        'question': q['question'],
        'options': options,
        'correct_option': correct_option,
        'correct_answer': correct,
        'explanation': q.get('explanation', ''),
    }


def generate_exam(num_questions: int = 50, difficulty: str = 'mixed') -> list[dict]:
    """
    Generate a full exam of `num_questions` MCQ items drawn from all 8 modules.
    difficulty='mixed' gives roughly 30% easy, 40% medium, 30% hard.
    Returns list of question dicts with question_number and question_id fields added.
    """
    per_module = num_questions // len(MODULES)
    remainder = num_questions % len(MODULES)

    diff_weights = (
        ['easy'] * 3 + ['medium'] * 4 + ['hard'] * 3
        if difficulty == 'mixed'
        else [difficulty] * 10
    )

    questions = []
    for i, mod in enumerate(MODULES):
        count = per_module + (1 if i < remainder else 0)
        for _ in range(count):
            d = random.choice(diff_weights)
            questions.append(generate_mcq(mod, d))

    random.shuffle(questions)

    for idx, q in enumerate(questions):
        q['question_number'] = idx + 1
        q['question_id'] = f'q{idx + 1}'

    return questions
