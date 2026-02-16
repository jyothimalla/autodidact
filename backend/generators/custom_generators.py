"""
Custom question generators for each of the 8 learning modules.
Each generator returns a dict: { question, answer, explanation }
Difficulty: 'easy' | 'medium' | 'hard'
"""
import random
import math
from fractions import Fraction


# ---------------------------------------------------------------------------
# Difficulty number ranges
# ---------------------------------------------------------------------------
RANGES = {
    'easy':   (2, 20),
    'medium': (10, 99),
    'hard':   (50, 500),
}

NAMES = ['Emma', 'Liam', 'Olivia', 'Noah', 'Ava', 'Ethan', 'Sophia', 'Mason',
         'Isabella', 'Lucas', 'Mia', 'Oliver', 'Amelia', 'Elijah', 'Harper']
ITEMS = ['apples', 'books', 'stickers', 'pencils', 'coins', 'sweets', 'cards',
         'marbles', 'stamps', 'biscuits']


def _r(difficulty: str):
    lo, hi = RANGES[difficulty]
    return random.randint(lo, hi)


# ---------------------------------------------------------------------------
# Four Operations
# ---------------------------------------------------------------------------
def _four_operations(difficulty: str) -> dict:
    a, b = _r(difficulty), _r(difficulty)
    op = random.choice(['+', '-', '*', '/'])
    if op == '-' and b > a:
        a, b = b, a
    if op == '/':
        b = random.choice([2, 3, 4, 5, 6, 10]) if difficulty == 'easy' else random.choice([2, 3, 4, 5, 6, 7, 8, 9, 10])
        a = b * random.randint(2, 12)
    answers = {'+': a + b, '-': a - b, '*': a * b, '/': a // b}
    symbols = {'+': 'plus', '-': 'minus', '*': 'multiplied by', '/': 'divided by'}
    ans = answers[op]
    return {
        'question': f'Calculate: {a} {op} {b} = ?',
        'answer': str(ans),
        'explanation': f'{a} {symbols[op]} {b} = {ans}'
    }


# ---------------------------------------------------------------------------
# Fractions and Decimals
# ---------------------------------------------------------------------------
def _fractions_decimals(difficulty: str) -> dict:
    kind = random.choice(['equivalent', 'compare', 'convert'])

    if kind == 'equivalent':
        num = random.randint(1, 5)
        den = random.randint(num + 1, 10)
        mult = random.randint(2, 5)
        return {
            'question': f'Write an equivalent fraction to {num}/{den} by multiplying numerator and denominator by {mult}.',
            'answer': f'{num * mult}/{den * mult}',
            'explanation': f'{num}/{den} = {num*mult}/{den*mult} (multiply both by {mult})'
        }

    if kind == 'compare':
        d1 = random.randint(2, 8)
        d2 = random.randint(2, 8)
        while d2 == d1:
            d2 = random.randint(2, 8)
        n1 = random.randint(1, d1 - 1)
        n2 = random.randint(1, d2 - 1)
        f1 = Fraction(n1, d1)
        f2 = Fraction(n2, d2)
        sign = '>' if f1 > f2 else '<' if f1 < f2 else '='
        return {
            'question': f'Which is larger: {n1}/{d1} or {n2}/{d2}?',
            'answer': f'{n1}/{d1} {sign} {n2}/{d2}',
            'explanation': f'{n1}/{d1} = {float(f1):.4f}, {n2}/{d2} = {float(f2):.4f}'
        }

    # convert fraction to decimal
    den_choices = [2, 4, 5, 8, 10, 20, 25, 100]
    den = random.choice(den_choices)
    num = random.randint(1, den - 1)
    dec = round(num / den, 4)
    return {
        'question': f'Convert {num}/{den} to a decimal.',
        'answer': str(dec),
        'explanation': f'{num} ÷ {den} = {dec}'
    }


# ---------------------------------------------------------------------------
# Ratios
# ---------------------------------------------------------------------------
def _ratios(difficulty: str) -> dict:
    kind = random.choice(['simplify', 'share'])

    if kind == 'simplify':
        factor = random.randint(2, 6)
        a = random.randint(1, 8) * factor
        b = random.randint(1, 8) * factor
        g = math.gcd(a, b)
        return {
            'question': f'Simplify the ratio {a} : {b}.',
            'answer': f'{a // g} : {b // g}',
            'explanation': f'HCF of {a} and {b} is {g}. Divide both by {g}: {a//g} : {b//g}'
        }

    # share in ratio
    lo, hi = RANGES[difficulty]
    p = random.randint(1, 5)
    q = random.randint(1, 5)
    total_parts = p + q
    one_part = random.randint(3, max(4, hi // 20)) * total_parts
    total = one_part
    share_a = (total // total_parts) * p
    share_b = (total // total_parts) * q
    name1, name2 = random.sample(NAMES, 2)
    return {
        'question': f'{name1} and {name2} share £{total} in the ratio {p} : {q}. How much does each person get?',
        'answer': f'{name1} gets £{share_a}, {name2} gets £{share_b}',
        'explanation': f'Total parts = {total_parts}. One part = £{total} ÷ {total_parts} = £{total//total_parts}. {name1}: {p} × £{total//total_parts} = £{share_a}. {name2}: {q} × £{total//total_parts} = £{share_b}.'
    }


# ---------------------------------------------------------------------------
# Percentages
# ---------------------------------------------------------------------------
def _percentages(difficulty: str) -> dict:
    kind = random.choice(['of_quantity', 'increase', 'decrease'])

    if kind == 'of_quantity':
        pct_choices = [10, 20, 25, 30, 40, 50, 75] if difficulty != 'hard' else [15, 35, 60, 70, 80, 90]
        pct = random.choice(pct_choices)
        base = random.randint(20, 400) * (1 if difficulty == 'easy' else 10 if difficulty == 'medium' else 100)
        base = round(base / 10) * 10
        result = base * pct // 100
        return {
            'question': f'Find {pct}% of {base}.',
            'answer': str(result),
            'explanation': f'{pct}% of {base} = ({pct} ÷ 100) × {base} = {result}'
        }

    pct = random.choice([5, 10, 15, 20, 25, 30, 50])
    base = random.randint(2, 40) * 10
    amount = base * pct // 100
    if kind == 'increase':
        result = base + amount
        return {
            'question': f'Increase £{base} by {pct}%.',
            'answer': f'£{result}',
            'explanation': f'{pct}% of £{base} = £{amount}. £{base} + £{amount} = £{result}'
        }
    result = base - amount
    return {
        'question': f'Decrease £{base} by {pct}%.',
        'answer': f'£{result}',
        'explanation': f'{pct}% of £{base} = £{amount}. £{base} - £{amount} = £{result}'
    }


# ---------------------------------------------------------------------------
# Multi-step Word Problems
# ---------------------------------------------------------------------------
def _multi_step_word_problems(difficulty: str) -> dict:
    name = random.choice(NAMES)
    item = random.choice(ITEMS)
    lo, hi = RANGES[difficulty]
    price = random.randint(2, 15)
    qty1 = random.randint(3, 12)
    qty2 = random.randint(1, qty1)
    spent = price * qty1
    remainder_qty = qty1 - qty2
    remainder_value = remainder_qty * price
    return {
        'question': (
            f'{name} buys {qty1} {item} at £{price} each. '
            f'Later, {name} gives away {qty2} of them. '
            f'How much are the remaining {item} worth in total?'
        ),
        'answer': f'£{remainder_value}',
        'explanation': (
            f'Step 1: Remaining {item} = {qty1} - {qty2} = {remainder_qty}. '
            f'Step 2: Value = {remainder_qty} × £{price} = £{remainder_value}.'
        )
    }


# ---------------------------------------------------------------------------
# Mental Arithmetic
# ---------------------------------------------------------------------------
def _mental_arithmetic(difficulty: str) -> dict:
    kind = random.choice(['compensation', 'estimate'])

    if kind == 'compensation':
        a = random.randint(20, 200) if difficulty != 'easy' else random.randint(10, 50)
        near = random.choice([9, 19, 29, 49, 99])
        result = a + near
        return {
            'question': f'Use a mental strategy to calculate: {a} + {near}',
            'answer': str(result),
            'explanation': f'Add {near + 1} then subtract 1: {a} + {near+1} - 1 = {result}'
        }

    a = random.randint(10, 900) if difficulty != 'easy' else random.randint(10, 90)
    b = random.randint(10, 900) if difficulty != 'easy' else random.randint(10, 90)
    rounded_a = round(a / 10) * 10
    rounded_b = round(b / 10) * 10
    estimate = rounded_a + rounded_b
    exact = a + b
    return {
        'question': f'Estimate {a} + {b} by rounding to the nearest 10.',
        'answer': f'Estimate: {estimate} (exact: {exact})',
        'explanation': f'{a} ≈ {rounded_a}, {b} ≈ {rounded_b}. Estimate = {rounded_a} + {rounded_b} = {estimate}'
    }


# ---------------------------------------------------------------------------
# Speed-based Calculation
# ---------------------------------------------------------------------------
def _speed_based_calculation(difficulty: str) -> dict:
    # Mixed arithmetic timed question — same as mental arithmetic but mixed ops
    a = _r(difficulty)
    b = _r(difficulty)
    ops = ['+', '-', '*']
    if difficulty == 'easy':
        ops = ['+', '-']
    op = random.choice(ops)
    if op == '-' and b > a:
        a, b = b, a
    results = {'+': a + b, '-': a - b, '*': a * b}
    ans = results[op]
    return {
        'question': f'Quick! {a} {op} {b} = ?',
        'answer': str(ans),
        'explanation': f'{a} {op} {b} = {ans}'
    }


# ---------------------------------------------------------------------------
# Logical Number Puzzles
# ---------------------------------------------------------------------------
def _logical_number_puzzles(difficulty: str) -> dict:
    kind = random.choice(['sequence', 'missing'])

    if kind == 'sequence':
        start = random.randint(1, 30)
        step = random.randint(2, 10) * (1 if difficulty != 'hard' else random.choice([-1, 1]))
        terms = [start + i * step for i in range(5)]
        next_term = terms[-1] + step
        return {
            'question': f'Find the next term in the sequence: {", ".join(str(t) for t in terms)}, ___',
            'answer': str(next_term),
            'explanation': f'The rule is {"add" if step > 0 else "subtract"} {abs(step)} each time. Next term = {terms[-1]} + ({step}) = {next_term}.'
        }

    # missing number: a * ? = b  or  ? + a = b
    a = random.randint(2, 12)
    b = a * random.randint(2, 9)
    missing = b // a
    return {
        'question': f'Find the missing number: {a} × ___ = {b}',
        'answer': str(missing),
        'explanation': f'{b} ÷ {a} = {missing}, so {a} × {missing} = {b}'
    }


# ---------------------------------------------------------------------------
# Dispatcher
# ---------------------------------------------------------------------------
MODULE_GENERATORS = {
    'four-operations':         _four_operations,
    'fractions-decimals':      _fractions_decimals,
    'ratios':                  _ratios,
    'percentages':             _percentages,
    'multi-step-word-problems': _multi_step_word_problems,
    'mental-arithmetic':       _mental_arithmetic,
    'speed-based-calculation': _speed_based_calculation,
    'logical-number-puzzles':  _logical_number_puzzles,
}


def generate_question(module_id: str, difficulty: str = 'medium') -> dict:
    """
    Generate one question for the given module and difficulty.
    Returns: { question: str, answer: str, explanation: str }
    """
    generator = MODULE_GENERATORS.get(module_id)
    if not generator:
        raise ValueError(f'Unknown module_id: {module_id}')
    if difficulty not in ('easy', 'medium', 'hard'):
        difficulty = 'medium'
    return generator(difficulty)
