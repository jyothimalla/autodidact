"""
MCQ wrapper around custom_generators.
Takes a free-answer question and adds 3 plausible wrong answers,
returning A/B/C/D options with a shuffled correct answer.
"""
import random
import re
from generators.custom_generators import generate_question, MODULE_GENERATORS

MODULES = list(MODULE_GENERATORS.keys())
STANDARD_EXAM_MODULES = [m for m in MODULES if m != 'english-cem']
DIFFICULTIES = ['easy', 'medium', 'hard']

CEM_BLUEPRINT = [
    {
        'name': 'Numerical Reasoning',
        'target_ratio': 0.42,
        'modules': [
            'four-operations',
            'fractions-decimals',
            'ratios',
            'percentages',
            'multi-step-word-problems',
            'mental-arithmetic',
            'speed-based-calculation',
        ],
    },
    {
        'name': 'Verbal Reasoning',
        'target_ratio': 0.38,
        'modules': [
            'verbal-reasoning',
        ],
    },
    {
        'name': 'Logic and Pattern Reasoning',
        'target_ratio': 0.20,
        'modules': [
            'logical-number-puzzles',
            'algebra',
            'probability',
            'coordinate-geometry',
        ],
    },
]

ENGLISH_BLUEPRINT = [
    {'name': 'Vocabulary', 'target_ratio': 0.28, 'modules': ['english-cem'], 'minutes': 18},
    {'name': 'Cloze and Grammar', 'target_ratio': 0.36, 'modules': ['english-cem'], 'minutes': 22},
    {'name': 'Spelling and Punctuation', 'target_ratio': 0.22, 'modules': ['english-cem'], 'minutes': 12},
    {'name': 'Language Analysis', 'target_ratio': 0.14, 'modules': ['english-cem'], 'minutes': 8},
]


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


def _extract_trailing_unit(answer: str) -> str:
    """
    Extract simple trailing unit text for answers like:
      48 cm³, 2.5 m^3, 14 cm2
    Returns empty string if no unit-like suffix is detected.
    """
    m = re.match(r'^\s*-?\d+(?:\.\d+)?\s*([a-zA-Zµ]+(?:\s*(?:\^?\d+|[²³]))?)\s*$', answer)
    if not m:
        return ''
    return m.group(1).strip()


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


def _letter_distractors(answer: str, count: int = 3) -> list:
    """Generate nearby alphabet distractors for single-letter answers."""
    if not re.fullmatch(r'[A-Z]', answer.strip()):
        return []
    idx = ord(answer) - ord('A')
    candidates = [
        chr(ord('A') + (idx + 1) % 26),
        chr(ord('A') + (idx - 1) % 26),
        chr(ord('A') + (idx + 2) % 26),
        chr(ord('A') + (idx - 2) % 26),
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

    # Single-letter verbal reasoning answers
    letter_ds = _letter_distractors(answer)
    if letter_ds:
        return letter_ds

    # Try numeric extraction
    num = _extract_number(answer)
    if num is not None:
        wrong_nums = _numeric_distractors(num)
        prefix = '£' if '£' in answer else ''
        unit = _extract_trailing_unit(answer)
        formatted = []
        for v in wrong_nums:
            val = int(v) if isinstance(v, float) and v == int(v) else v
            if prefix:
                formatted.append(f'{prefix}{val}')
            elif unit:
                formatted.append(f'{val} {unit}')
            else:
                formatted.append(str(val))
        return formatted

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
    provided_options = q.get('mcq_options')
    if isinstance(provided_options, list) and len(provided_options) >= 4:
        pool = [str(x).strip() for x in provided_options[:4]]
        if correct not in pool:
            pool[0] = correct
    else:
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


def generate_questions_for_module(module_id: str, num_questions: int = 5, difficulty: str = 'mixed') -> list[dict]:
    """
    Generate practice/challenge questions for a specific module.

    Args:
        module_id: The module to generate questions for
        num_questions: Number of questions to generate (5 for practice, 10 for challenge)
        difficulty: 'easy', 'medium', 'hard', or 'mixed'

    Returns:
        List of MCQ question dicts with question_number and question_id fields
    """
    diff_weights = (
        ['easy'] * 3 + ['medium'] * 4 + ['hard'] * 3
        if difficulty == 'mixed'
        else [difficulty] * 10
    )

    questions = []
    for i in range(num_questions):
        d = random.choice(diff_weights)
        q = generate_mcq(module_id, d)
        q['question_number'] = i + 1
        q['question_id'] = f'q{i + 1}'
        questions.append(q)

    return questions


def _generate_standard_exam(num_questions: int = 50, difficulty: str = 'mixed') -> list[dict]:
    """
    Generate a full exam of `num_questions` MCQ items drawn from all 8 modules.
    difficulty='mixed' gives roughly 30% easy, 40% medium, 30% hard.
    Returns list of question dicts with question_number and question_id fields added.
    """
    per_module = num_questions // len(STANDARD_EXAM_MODULES)
    remainder = num_questions % len(STANDARD_EXAM_MODULES)

    diff_weights = (
        ['easy'] * 3 + ['medium'] * 4 + ['hard'] * 3
        if difficulty == 'mixed'
        else [difficulty] * 10
    )

    questions = []
    for i, mod in enumerate(STANDARD_EXAM_MODULES):
        count = per_module + (1 if i < remainder else 0)
        for _ in range(count):
            d = random.choice(diff_weights)
            questions.append(generate_mcq(mod, d))

    random.shuffle(questions)

    for idx, q in enumerate(questions):
        q['question_number'] = idx + 1
        q['question_id'] = f'q{idx + 1}'

    return questions


def _allocate_counts_by_ratio(total: int, ratios: list[float]) -> list[int]:
    """Allocate integer counts that sum to total, preserving target ratios as closely as possible."""
    raw = [total * r for r in ratios]
    base = [int(v) for v in raw]
    remainder = total - sum(base)
    # distribute remainder to largest fractional parts
    fractional_rank = sorted(range(len(raw)), key=lambda i: (raw[i] - base[i]), reverse=True)
    for i in range(remainder):
        base[fractional_rank[i % len(base)]] += 1
    return base


def _generate_cem_exam(num_questions: int = 50, difficulty: str = 'mixed') -> list[dict]:
    """
    Generate a CEM-style mixed exam blueprint with section tagging.
    This stays deterministic/rule-based but enforces section weighting and variety.
    """
    diff_weights = (
        ['easy'] * 3 + ['medium'] * 4 + ['hard'] * 3
        if difficulty == 'mixed'
        else [difficulty] * 10
    )
    ratios = [s['target_ratio'] for s in CEM_BLUEPRINT]
    section_counts = _allocate_counts_by_ratio(num_questions, ratios)

    questions: list[dict] = []
    for section, count in zip(CEM_BLUEPRINT, section_counts):
        modules = section['modules']
        for i in range(count):
            module_id = modules[i % len(modules)]
            d = random.choice(diff_weights)
            q = generate_mcq(module_id, d)
            q['section_name'] = section['name']
            q['section_minutes'] = max(1, round((count / max(1, num_questions)) * 60))
            questions.append(q)

    random.shuffle(questions)
    for idx, q in enumerate(questions):
        q['question_number'] = idx + 1
        q['question_id'] = f'q{idx + 1}'

    return questions


def _generate_english_exam(num_questions: int = 50, target_year: str = 'year4') -> list[dict]:
    """
    English-focused grammar-school style paper for Year 4/Year 5 preparation.
    """
    if target_year == 'year5':
        diff_weights = ['medium'] * 6 + ['hard'] * 4
    else:
        diff_weights = ['easy'] * 5 + ['medium'] * 5

    ratios = [s['target_ratio'] for s in ENGLISH_BLUEPRINT]
    section_counts = _allocate_counts_by_ratio(num_questions, ratios)

    questions: list[dict] = []
    for section, count in zip(ENGLISH_BLUEPRINT, section_counts):
        modules = section['modules']
        for i in range(count):
            module_id = modules[i % len(modules)]
            d = random.choice(diff_weights)
            q = generate_mcq(module_id, d)
            q['section_name'] = section['name']
            q['section_minutes'] = section['minutes']
            questions.append(q)

    random.shuffle(questions)
    for idx, q in enumerate(questions):
        q['question_number'] = idx + 1
        q['question_id'] = f'q{idx + 1}'

    return questions


def _apply_weak_focus(questions: list[dict], weak_modules: list[str], difficulty: str) -> list[dict]:
    """
    Replace a subset of questions with weak-area module questions.
    Keeps paper length fixed and gently increases weak-topic exposure.
    """
    if not questions or not weak_modules:
        return questions

    replace_count = max(1, int(len(questions) * 0.24))
    indexes = random.sample(range(len(questions)), min(replace_count, len(questions)))
    diff_weights = (
        ['easy'] * 3 + ['medium'] * 4 + ['hard'] * 3
        if difficulty == 'mixed'
        else [difficulty] * 10
    )

    for idx in indexes:
        module_id = random.choice(weak_modules)
        d = random.choice(diff_weights)
        new_q = generate_mcq(module_id, d)
        # keep any section tagging from original slot for timing consistency
        new_q['section_name'] = questions[idx].get('section_name')
        new_q['section_minutes'] = questions[idx].get('section_minutes')
        questions[idx] = new_q

    for idx, q in enumerate(questions):
        q['question_number'] = idx + 1
        q['question_id'] = f'q{idx + 1}'
    return questions


def generate_exam(
    num_questions: int = 50,
    difficulty: str = 'mixed',
    exam_style: str = 'standard',
    target_year: str = 'year4',
    weak_focus_modules: list[str] | None = None,
) -> list[dict]:
    """
    Generate an exam in either:
      - standard: equal spread across all supported modules
      - cem: section-blueprint weighted mix inspired by CEM-style pacing
    """
    if exam_style == 'english':
        return _generate_english_exam(num_questions=num_questions, target_year=target_year)

    if exam_style == 'cem':
        generated = _generate_cem_exam(num_questions=num_questions, difficulty=difficulty)
    else:
        generated = _generate_standard_exam(num_questions=num_questions, difficulty=difficulty)

    return _apply_weak_focus(generated, weak_focus_modules or [], difficulty)
