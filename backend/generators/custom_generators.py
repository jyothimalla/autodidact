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
# Probability
# ---------------------------------------------------------------------------
def _probability(difficulty: str) -> dict:
    kind = random.choice(['single', 'not', 'combined'])

    COLOURS = ['red', 'blue', 'green', 'yellow', 'white', 'black', 'purple', 'orange']

    if kind == 'single' or difficulty == 'easy':
        # Basic probability from a bag of coloured balls
        total = random.randint(5, 20) if difficulty != 'hard' else random.randint(10, 40)
        colour = random.choice(COLOURS)
        favourable = random.randint(1, total - 1)
        g = math.gcd(favourable, total)
        numer, denom = favourable // g, total // g
        ans = f'{numer}/{denom}' if denom != 1 else '1'
        return {
            'question': (f'A bag contains {total} balls. {favourable} of them are {colour}. '
                         f'A ball is chosen at random. What is the probability it is {colour}?'),
            'answer': ans,
            'explanation': f'P({colour}) = {favourable}/{total} = {ans}'
        }

    if kind == 'not':
        total = random.randint(6, 24)
        colour = random.choice(COLOURS)
        favourable = random.randint(1, total - 2)
        not_fav = total - favourable
        g = math.gcd(not_fav, total)
        numer, denom = not_fav // g, total // g
        ans = f'{numer}/{denom}' if denom != 1 else '1'
        return {
            'question': (f'A bag contains {total} balls. {favourable} are {colour}. '
                         f'What is the probability of NOT picking a {colour} ball?'),
            'answer': ans,
            'explanation': f'P(not {colour}) = (total − favourable) / total = {not_fav}/{total} = {ans}'
        }

    # combined: two spinners / two events
    sides_a = random.randint(2, 6)
    sides_b = random.randint(2, 6)
    total_outcomes = sides_a * sides_b
    favourable = 1
    g = math.gcd(favourable, total_outcomes)
    numer, denom = favourable // g, total_outcomes // g
    ans = f'{numer}/{denom}' if denom != 1 else '1'
    return {
        'question': (f'Spinner A has {sides_a} equal sections (numbered 1–{sides_a}). '
                     f'Spinner B has {sides_b} equal sections (numbered 1–{sides_b}). '
                     f'Both are spun once. What is the probability both land on 1?'),
        'answer': ans,
        'explanation': (f'Total outcomes = {sides_a} × {sides_b} = {total_outcomes}. '
                        f'Favourable = 1 (both show 1). P = 1/{total_outcomes} = {ans}')
    }


# ---------------------------------------------------------------------------
# Algebra
# ---------------------------------------------------------------------------
def _algebra(difficulty: str) -> dict:
    kind = random.choice(['solve_linear', 'expression', 'formula'])

    if kind == 'solve_linear' or difficulty == 'easy':
        # ax + b = c  →  solve for x
        a = random.randint(2, 5 if difficulty == 'easy' else 10)
        x = random.randint(1, 10 if difficulty != 'hard' else 20)
        b = random.randint(1, 20 if difficulty != 'hard' else 50)
        c = a * x + b
        return {
            'question': f'Solve for x: {a}x + {b} = {c}',
            'answer': str(x),
            'explanation': f'{a}x = {c} − {b} = {c - b}. x = {c - b} ÷ {a} = {x}'
        }

    if kind == 'expression':
        # Evaluate ax² + b when x = n  (easy: ax + b)
        a = random.randint(1, 5)
        b = random.randint(1, 20)
        x = random.randint(1, 8 if difficulty != 'hard' else 12)
        if difficulty == 'hard':
            result = a * x * x + b
            return {
                'question': f'Evaluate {a}x² + {b} when x = {x}.',
                'answer': str(result),
                'explanation': f'{a} × {x}² + {b} = {a} × {x*x} + {b} = {a*x*x} + {b} = {result}'
            }
        result = a * x + b
        return {
            'question': f'Evaluate {a}x + {b} when x = {x}.',
            'answer': str(result),
            'explanation': f'{a} × {x} + {b} = {a*x} + {b} = {result}'
        }

    # Substitution into a formula: e.g. Area = l × w, find A
    l = random.randint(3, 20)
    w = random.randint(3, 15)
    area = l * w
    return {
        'question': f'Use the formula A = l × w to find A when l = {l} and w = {w}.',
        'answer': str(area),
        'explanation': f'A = {l} × {w} = {area}'
    }


# ---------------------------------------------------------------------------
# Perimeter and Area
# ---------------------------------------------------------------------------
def _perimeter_area(difficulty: str) -> dict:
    shape = random.choice(['rectangle', 'triangle', 'square', 'parallelogram', 'trapezium'])
    find = random.choice(['area', 'perimeter']) if shape not in ('parallelogram', 'trapezium') else 'area'

    if shape == 'rectangle':
        l = random.randint(3, 20 if difficulty != 'hard' else 50)
        w = random.randint(2, l)
        if find == 'area':
            ans = l * w
            return {
                'question': f'Find the area of a rectangle with length {l} cm and width {w} cm.',
                'answer': f'{ans} cm²',
                'explanation': f'Area = length × width = {l} × {w} = {ans} cm²'
            }
        ans = 2 * (l + w)
        return {
            'question': f'Find the perimeter of a rectangle with length {l} cm and width {w} cm.',
            'answer': f'{ans} cm',
            'explanation': f'Perimeter = 2 × (length + width) = 2 × ({l} + {w}) = 2 × {l+w} = {ans} cm'
        }

    if shape == 'square':
        s = random.randint(2, 20 if difficulty != 'hard' else 40)
        if find == 'area':
            ans = s * s
            return {
                'question': f'Find the area of a square with side {s} cm.',
                'answer': f'{ans} cm²',
                'explanation': f'Area = side² = {s}² = {ans} cm²'
            }
        ans = 4 * s
        return {
            'question': f'Find the perimeter of a square with side {s} cm.',
            'answer': f'{ans} cm',
            'explanation': f'Perimeter = 4 × side = 4 × {s} = {ans} cm'
        }

    if shape == 'triangle':
        base = random.randint(4, 20 if difficulty != 'hard' else 40)
        height = random.randint(3, 15 if difficulty != 'hard' else 30)
        a = random.randint(3, 15)
        b = random.randint(3, 15)
        if find == 'area':
            area = (base * height) // 2
            extra = '' if (base * height) % 2 == 0 else '.5'
            ans_val = base * height / 2
            return {
                'question': f'Find the area of a triangle with base {base} cm and height {height} cm.',
                'answer': f'{ans_val} cm²',
                'explanation': f'Area = ½ × base × height = ½ × {base} × {height} = {ans_val} cm²'
            }
        # perimeter of triangle (right-angled for clean answers)
        c = random.choice([3, 4, 5, 5, 6, 8, 10, 12, 13, 15])
        triples = [(3,4,5),(5,12,13),(6,8,10),(8,15,17),(9,12,15)]
        t = random.choice(triples)
        scale = random.randint(1, 3 if difficulty != 'hard' else 5)
        sa, sb, sc = t[0]*scale, t[1]*scale, t[2]*scale
        peri = sa + sb + sc
        return {
            'question': f'Find the perimeter of a triangle with sides {sa} cm, {sb} cm and {sc} cm.',
            'answer': f'{peri} cm',
            'explanation': f'Perimeter = {sa} + {sb} + {sc} = {peri} cm'
        }

    if shape == 'parallelogram':
        base = random.randint(4, 20 if difficulty != 'hard' else 40)
        height = random.randint(3, 15 if difficulty != 'hard' else 25)
        ans = base * height
        return {
            'question': f'Find the area of a parallelogram with base {base} cm and perpendicular height {height} cm.',
            'answer': f'{ans} cm²',
            'explanation': f'Area = base × height = {base} × {height} = {ans} cm²'
        }

    # trapezium
    a = random.randint(4, 15)
    b = random.randint(a + 1, a + 10)
    h = random.randint(3, 12 if difficulty != 'hard' else 20)
    area = (a + b) * h / 2
    return {
        'question': f'Find the area of a trapezium with parallel sides {a} cm and {b} cm, and height {h} cm.',
        'answer': f'{area} cm²',
        'explanation': f'Area = ½ × (a + b) × h = ½ × ({a} + {b}) × {h} = ½ × {a+b} × {h} = {area} cm²'
    }


# ---------------------------------------------------------------------------
# Angles
# ---------------------------------------------------------------------------
def _angles(difficulty: str) -> dict:
    kind = random.choice(['straight_line', 'triangle', 'quadrilateral', 'vertically_opposite', 'around_point'])

    if kind == 'straight_line' or difficulty == 'easy':
        a = random.randint(20, 160)
        b = 180 - a
        return {
            'question': f'Two angles on a straight line. One angle is {a}°. What is the other angle?',
            'answer': f'{b}°',
            'explanation': f'Angles on a straight line sum to 180°. {a}° + ? = 180°. ? = {b}°'
        }

    if kind == 'triangle':
        a = random.randint(30, 80)
        b = random.randint(30, 80)
        while a + b >= 180:
            b = random.randint(20, 70)
        c = 180 - a - b
        return {
            'question': f'A triangle has two angles of {a}° and {b}°. Find the third angle.',
            'answer': f'{c}°',
            'explanation': f'Angles in a triangle sum to 180°. {a}° + {b}° + ? = 180°. ? = {c}°'
        }

    if kind == 'quadrilateral':
        angles = [random.randint(60, 120) for _ in range(3)]
        while sum(angles) >= 360:
            angles[-1] = random.randint(40, 90)
        fourth = 360 - sum(angles)
        if fourth <= 0:
            fourth = 30
            angles[0] = 360 - angles[1] - angles[2] - fourth
        return {
            'question': (f'A quadrilateral has three angles: {angles[0]}°, {angles[1]}° and {angles[2]}°. '
                         f'Find the fourth angle.'),
            'answer': f'{fourth}°',
            'explanation': (f'Angles in a quadrilateral sum to 360°. '
                            f'{angles[0]}° + {angles[1]}° + {angles[2]}° + ? = 360°. ? = {fourth}°')
        }

    if kind == 'vertically_opposite':
        a = random.randint(20, 160)
        return {
            'question': (f'Two straight lines cross. One of the angles formed is {a}°. '
                         f'What is the vertically opposite angle?'),
            'answer': f'{a}°',
            'explanation': f'Vertically opposite angles are equal. The answer is {a}°.'
        }

    # around a point
    angles = [random.randint(40, 150) for _ in range(3)]
    while sum(angles) >= 360:
        angles[-1] = random.randint(30, 80)
    last = 360 - sum(angles)
    if last <= 0:
        last = 40
        angles[0] = 360 - angles[1] - angles[2] - last
    return {
        'question': (f'Angles around a point: {angles[0]}°, {angles[1]}° and {angles[2]}°. '
                     f'Find the remaining angle.'),
        'answer': f'{last}°',
        'explanation': (f'Angles around a point sum to 360°. '
                        f'{angles[0]}° + {angles[1]}° + {angles[2]}° + ? = 360°. ? = {last}°')
    }


# ---------------------------------------------------------------------------
# Coordinate Geometry
# ---------------------------------------------------------------------------
def _coordinate_geometry(difficulty: str) -> dict:
    kind = random.choice(['plot_describe', 'midpoint', 'quadrant', 'distance'])

    rng = 5 if difficulty == 'easy' else (10 if difficulty == 'medium' else 20)

    if kind == 'plot_describe' or difficulty == 'easy':
        x = random.randint(1, rng)
        y = random.randint(1, rng)
        return {
            'question': f'What are the coordinates of a point that is {x} units right and {y} units up from the origin?',
            'answer': f'({x}, {y})',
            'explanation': f'Moving {x} right gives x = {x}; moving {y} up gives y = {y}. Coordinates: ({x}, {y})'
        }

    if kind == 'midpoint':
        x1, y1 = random.randint(-rng, rng), random.randint(-rng, rng)
        x2, y2 = random.randint(-rng, rng), random.randint(-rng, rng)
        # ensure whole-number midpoint
        if (x1 + x2) % 2 != 0:
            x2 += 1
        if (y1 + y2) % 2 != 0:
            y2 += 1
        mx, my = (x1 + x2) // 2, (y1 + y2) // 2
        return {
            'question': f'Find the midpoint of the line segment joining ({x1}, {y1}) and ({x2}, {y2}).',
            'answer': f'({mx}, {my})',
            'explanation': f'Midpoint = (({x1}+{x2})/2, ({y1}+{y2})/2) = ({mx}, {my})'
        }

    if kind == 'quadrant':
        quadrant_data = [
            (random.randint(1, rng),  random.randint(1, rng),  'first'),
            (random.randint(-rng, -1), random.randint(1, rng),  'second'),
            (random.randint(-rng, -1), random.randint(-rng,-1), 'third'),
            (random.randint(1, rng),  random.randint(-rng,-1), 'fourth'),
        ]
        x, y, name = random.choice(quadrant_data)
        return {
            'question': f'In which quadrant does the point ({x}, {y}) lie?',
            'answer': f'{name.capitalize()} quadrant',
            'explanation': (f'x = {x} ({"positive" if x > 0 else "negative"}), '
                            f'y = {y} ({"positive" if y > 0 else "negative"}). '
                            f'That places the point in the {name} quadrant.')
        }

    # Horizontal / vertical distance
    x1 = random.randint(-rng, rng)
    x2 = random.randint(-rng, rng)
    while x2 == x1:
        x2 = random.randint(-rng, rng)
    y = random.randint(-rng, rng)
    dist = abs(x2 - x1)
    return {
        'question': f'What is the distance between points ({x1}, {y}) and ({x2}, {y})?',
        'answer': f'{dist} units',
        'explanation': f'Both points share the same y-coordinate, so distance = |{x2} − {x1}| = {dist} units'
    }


# ---------------------------------------------------------------------------
# Volumes
# ---------------------------------------------------------------------------
def _volumes(difficulty: str) -> dict:
    shape = random.choice(['cuboid', 'cube', 'cylinder', 'triangular_prism'])

    if shape == 'cube':
        s = random.randint(2, 10 if difficulty != 'hard' else 20)
        vol = s ** 3
        return {
            'question': f'Find the volume of a cube with side length {s} cm.',
            'answer': f'{vol} cm³',
            'explanation': f'Volume = side³ = {s}³ = {vol} cm³'
        }

    if shape == 'cuboid' or difficulty == 'easy':
        l = random.randint(2, 15 if difficulty != 'hard' else 30)
        w = random.randint(2, 12 if difficulty != 'hard' else 20)
        h = random.randint(2, 10 if difficulty != 'hard' else 15)
        vol = l * w * h
        return {
            'question': f'Find the volume of a cuboid with length {l} cm, width {w} cm and height {h} cm.',
            'answer': f'{vol} cm³',
            'explanation': f'Volume = l × w × h = {l} × {w} × {h} = {vol} cm³'
        }

    if shape == 'cylinder':
        r = random.randint(2, 8 if difficulty != 'hard' else 15)
        h = random.randint(3, 15 if difficulty != 'hard' else 30)
        vol = round(math.pi * r * r * h, 2)
        return {
            'question': f'Find the volume of a cylinder with radius {r} cm and height {h} cm. Give your answer to 2 decimal places. (Use π = 3.14159)',
            'answer': f'{vol} cm³',
            'explanation': f'Volume = π × r² × h = π × {r}² × {h} = π × {r*r} × {h} = {vol} cm³'
        }

    # triangular prism
    base = random.randint(3, 12 if difficulty != 'hard' else 20)
    tri_h = random.randint(3, 10 if difficulty != 'hard' else 15)
    length = random.randint(4, 15 if difficulty != 'hard' else 25)
    cross_section = base * tri_h / 2
    vol = cross_section * length
    return {
        'question': (f'A triangular prism has a triangular face with base {base} cm and height {tri_h} cm. '
                     f'The length of the prism is {length} cm. Find its volume.'),
        'answer': f'{vol} cm³',
        'explanation': (f'Cross-sectional area = ½ × {base} × {tri_h} = {cross_section} cm². '
                        f'Volume = {cross_section} × {length} = {vol} cm³')
    }


# ---------------------------------------------------------------------------
# Verbal Reasoning
# ---------------------------------------------------------------------------
def _verbal_reasoning(difficulty: str) -> dict:
    kind = random.choice(['letter_after', 'position', 'sequence', 'opposite'])

    if kind == 'letter_after':
        step = random.randint(1, 3 if difficulty == 'easy' else 5 if difficulty == 'medium' else 8)
        start_idx = random.randint(0, 25)
        answer_idx = (start_idx + step) % 26
        start = chr(ord('A') + start_idx)
        answer = chr(ord('A') + answer_idx)
        return {
            'question': f'In the alphabet, which letter is {step} letter(s) after {start}?',
            'answer': answer,
            'explanation': f'{start} is position {start_idx + 1}. Move forward {step} to position {answer_idx + 1}, which is {answer}.'
        }

    if kind == 'position':
        word_bank = ['CAT', 'DOG', 'BOOK', 'READ', 'CODE', 'LOGIC', 'SMART', 'BRAIN']
        word = random.choice(word_bank if difficulty != 'hard' else word_bank + ['PATTERN', 'REASON'])
        total = sum((ord(ch) - ord('A') + 1) for ch in word)
        return {
            'question': f'Using A=1, B=2, ..., Z=26, find the total for the word "{word}".',
            'answer': str(total),
            'explanation': f'Sum the letter positions in {word} to get {total}.'
        }

    if kind == 'sequence':
        start = random.randint(1, 8 if difficulty == 'easy' else 12)
        step1 = random.randint(1, 3 if difficulty == 'easy' else 4)
        step2 = step1 + random.randint(1, 2 if difficulty != 'easy' else 1)
        p1 = start
        p2 = p1 + step1
        p3 = p2 + step2
        p4 = p3 + step1
        p5 = p4 + step2
        answer = chr(ord('A') + (p5 - 1) % 26)
        s1 = chr(ord('A') + (p1 - 1) % 26)
        s2 = chr(ord('A') + (p2 - 1) % 26)
        s3 = chr(ord('A') + (p3 - 1) % 26)
        s4 = chr(ord('A') + (p4 - 1) % 26)
        return {
            'question': f'Find the next letter in the sequence: {s1}, {s2}, {s3}, {s4}, ?',
            'answer': answer,
            'explanation': f'Positions follow +{step1}, +{step2}, +{step1}, +{step2}. Next letter is {answer}.'
        }

    letter_idx = random.randint(0, 25)
    opposite_idx = 25 - letter_idx
    letter = chr(ord('A') + letter_idx)
    opposite = chr(ord('A') + opposite_idx)
    return {
        'question': f'What is the opposite letter pair of {letter} in the alphabet mirror (A↔Z, B↔Y, ...)?',
        'answer': opposite,
        'explanation': f'{letter} is position {letter_idx + 1}; mirrored position is {26 - letter_idx}, which is {opposite}.'
    }


# ---------------------------------------------------------------------------
# Non-Verbal Reasoning (CEM-style fundamentals)
# ---------------------------------------------------------------------------
def _non_verbal_item_for_kinds(kinds: list[str], difficulty: str) -> dict:
    kind = random.choice(kinds)

    matrix_bank = [
        (
            'In a 3x3 shape matrix, the number of sides increases by 1 across each row (triangle, square, pentagon). '
            'If the third row starts with a hexagon then a heptagon, what should the missing third shape be?',
            ['Triangle', 'Pentagon', 'Octagon', 'Nonagon'],
            'Octagon'
        ),
        (
            'In each row, shading follows: white -> half-shaded -> fully shaded. '
            'What should the missing third shape be in that row?',
            ['White shape', 'Half-shaded shape', 'Fully shaded shape', 'Striped shape'],
            'Fully shaded shape'
        ),
    ]

    rotation_bank = [
        (
            'A right-pointing arrow is rotated 90 degrees clockwise. Which direction does it point now?',
            ['Up', 'Down', 'Left', 'Right'],
            'Down'
        ),
        (
            'A shape is reflected in a vertical mirror line. What changes?',
            ['Top and bottom swap', 'Left and right swap', 'Only size changes', 'Nothing changes'],
            'Left and right swap'
        ),
    ]

    odd_one_out_bank = [
        (
            'Which is the odd one out?',
            ['Square (4 lines of symmetry)', 'Rectangle (2 lines of symmetry)', 'Circle (many lines of symmetry)', 'Scalene triangle (0 lines of symmetry)'],
            'Scalene triangle (0 lines of symmetry)'
        ),
        (
            'Which shape does not belong with the others?',
            ['Cube net', 'Cuboid net', 'Pyramid net', 'Circle'],
            'Circle'
        ),
    ]

    spatial_bank = [
        (
            'Which pair of faces are opposite on a standard cube?',
            ['Adjacent faces sharing an edge', 'Faces that never touch', 'Any two top faces', 'Faces with matching colours only'],
            'Faces that never touch'
        ),
        (
            'When a cube net folds, which relationship stays true?',
            ['All faces touch all others', 'Only edge-sharing faces become adjacent', 'Corners become edges', 'Opposite faces share an edge'],
            'Only edge-sharing faces become adjacent'
        ),
    ]

    if kind == 'matrix':
        question, options, answer = random.choice(matrix_bank)
    elif kind == 'rotation':
        question, options, answer = random.choice(rotation_bank)
    elif kind == 'odd-one-out':
        question, options, answer = random.choice(odd_one_out_bank)
    else:
        question, options, answer = random.choice(spatial_bank)

    if difficulty == 'easy':
        explanation = f'The correct pattern rule gives "{answer}".'
    elif difficulty == 'hard':
        explanation = f'"{answer}" is the only option consistent with the full visual rule and transformation.'
    else:
        explanation = f'"{answer}" matches the non-verbal pattern rule.'

    return {
        'question': question,
        'answer': answer,
        'mcq_options': options,
        'explanation': explanation,
    }


def _non_verbal_reasoning(difficulty: str) -> dict:
    return _non_verbal_item_for_kinds(['matrix', 'rotation', 'odd-one-out', 'spatial'], difficulty)


def _nvr_cem_pattern_matrices(difficulty: str) -> dict:
    return _non_verbal_item_for_kinds(['matrix'], difficulty)


def _nvr_cem_rotations_reflections(difficulty: str) -> dict:
    return _non_verbal_item_for_kinds(['rotation'], difficulty)


def _nvr_cem_odd_one_out(difficulty: str) -> dict:
    return _non_verbal_item_for_kinds(['odd-one-out'], difficulty)


def _nvr_cem_3d_nets(difficulty: str) -> dict:
    return _non_verbal_item_for_kinds(['spatial'], difficulty)


# ---------------------------------------------------------------------------
# English (CEM-style fundamentals)
# ---------------------------------------------------------------------------
def _english_item_for_kinds(kinds: list[str], difficulty: str) -> dict:
    """
    Build a single English MCQ from a constrained set of question kinds.
    """
    kind = random.choice(kinds)

    synonym_bank = [
        ('rapid', ['fast', 'slow', 'late', 'quiet'], 'fast'),
        ('enormous', ['tiny', 'small', 'huge', 'dull'], 'huge'),
        ('ancient', ['modern', 'old', 'future', 'fresh'], 'old'),
        ('fragile', ['strong', 'careful', 'breakable', 'thick'], 'breakable'),
        ('generous', ['kind', 'selfish', 'angry', 'nervous'], 'kind'),
    ]
    antonym_bank = [
        ('expand', ['grow', 'stretch', 'shrink', 'build'], 'shrink'),
        ('scarce', ['rare', 'plentiful', 'small', 'thin'], 'plentiful'),
        ('victory', ['defeat', 'win', 'prize', 'success'], 'defeat'),
        ('include', ['add', 'contain', 'exclude', 'keep'], 'exclude'),
        ('polite', ['rude', 'formal', 'calm', 'kind'], 'rude'),
    ]
    grammar_bank = [
        ('The kitten curled up and fell ____ on the rug.', ['sleep', 'asleep', 'sleeping', 'sleeps'], 'asleep'),
        ('Although it was raining, the match continued ____ planned.', ['as', 'like', 'than', 'for'], 'as'),
        ('Neither Sam nor his friends ____ late for the rehearsal.', ['was', 'were', 'be', 'is'], 'were'),
        ('She completed the puzzle ____ than her brother.', ['quick', 'quickly', 'quicker', 'quickest'], 'quicker'),
        ('In the sentence "They carefully crossed the road", what type of word is "carefully"?',
         ['noun', 'adverb', 'adjective', 'pronoun'], 'adverb'),
    ]
    spelling_bank = [
        ('Choose the correctly spelt word.', ['definately', 'definitely', 'definetly', 'definatly'], 'definitely'),
        ('Choose the correctly spelt word.', ['seperate', 'separat', 'separate', 'seperete'], 'separate'),
        ('Choose the correctly spelt word.', ['occured', 'occurred', 'ocurred', 'occurd'], 'occurred'),
        ('Choose the correctly spelt word.', ['necessary', 'neccessary', 'necessery', 'necesary'], 'necessary'),
    ]
    punctuation_bank = [
        ('Which sentence is punctuated correctly?', [
            'After lunch we went to the park and played football',
            'After lunch, we went to the park and played football.',
            'After lunch we went, to the park and played football.',
            'After lunch we, went to the park and played football.'
        ], 'After lunch, we went to the park and played football.'),
        ('Which sentence is punctuated correctly?', [
            'Its raining so take your coat.',
            "It's raining so take your coat.",
            "It's raining, so take you're coat.",
            'Its raining, so take your coat'
        ], "It's raining so take your coat."),
    ]
    comprehension_bank = [
        (
            'Read the passage: "Maya packed her bag the night before the trip. In the morning, she checked the weather and added a raincoat." Why did Maya add a raincoat?',
            ['She wanted to carry extra weight.', 'She checked the weather first.', 'She forgot her bag.', 'She was going swimming.'],
            'She checked the weather first.'
        ),
        (
            'Read the passage: "The library was silent except for pages turning. Arun whispered because he did not want to disturb anyone." What does this tell us about the library?',
            ['It was noisy and crowded.', 'People were expected to be quiet.', 'It was closed for the day.', 'No one was inside.'],
            'People were expected to be quiet.'
        ),
    ]
    creative_writing_bank = [
        (
            'Which opening sentence is most engaging for a creative story?',
            ['I woke up and had breakfast.', 'The wind howled as the old gate creaked open.', 'It was Monday and I went to school.', 'We had maths first lesson.'],
            'The wind howled as the old gate creaked open.'
        ),
        (
            'Which sentence adds the best descriptive detail?',
            ['The dog ran.', 'The dog moved.', 'The dog dashed across the muddy field, splashing puddles.', 'The dog was there.'],
            'The dog dashed across the muddy field, splashing puddles.'
        ),
    ]
    narrative_writing_bank = [
        (
            'Choose the best sentence to continue the narrative logically: "Tom heard a loud crash in the kitchen. He ran downstairs and..."',
            ['he wondered what happened next week.', 'he saw the broken vase on the floor.', 'he eats dinner quietly.', 'the sun is bright tomorrow.'],
            'he saw the broken vase on the floor.'
        ),
        (
            'Which option gives a clear ending to a narrative?',
            ['Then it started.', 'Everyone shouted because.', 'At last, Sara found her brother and they walked home safely.', 'The end of maybe.'],
            'At last, Sara found her brother and they walked home safely.'
        ),
    ]
    report_bank = [
        (
            'Which heading best suits a non-chronological report about owls?',
            ['Once Upon a Time', 'What Owls Eat', 'My Best Day Ever', 'A Funny Story'],
            'What Owls Eat'
        ),
        (
            'Which sentence is most suitable for a non-chronological report?',
            ['I think foxes are cute and funny.', 'Foxes are mammals that live in many habitats across the UK.', 'Yesterday I saw a fox near my house.', 'Foxes are my favourite because they are cool.'],
            'Foxes are mammals that live in many habitats across the UK.'
        ),
    ]

    if kind == 'synonym':
        base, options, answer = random.choice(synonym_bank)
        question = f'Choose the word closest in meaning to "{base}".'
    elif kind == 'antonym':
        base, options, answer = random.choice(antonym_bank)
        question = f'Choose the word opposite in meaning to "{base}".'
    elif kind == 'grammar':
        question, options, answer = random.choice(grammar_bank)
    elif kind == 'spelling':
        question, options, answer = random.choice(spelling_bank)
    elif kind == 'punctuation':
        question, options, answer = random.choice(punctuation_bank)
    elif kind == 'comprehension':
        question, options, answer = random.choice(comprehension_bank)
    elif kind == 'creative-writing':
        question, options, answer = random.choice(creative_writing_bank)
    elif kind == 'narrative-writing':
        question, options, answer = random.choice(narrative_writing_bank)
    else:
        question, options, answer = random.choice(report_bank)

    if difficulty == 'easy':
        explanation = f'The best fit is "{answer}" in this context.'
    elif difficulty == 'hard':
        explanation = f'"{answer}" is the only option that best matches the expected 11+ English standard for this question.'
    else:
        explanation = f'"{answer}" is the correct choice based on meaning, grammar, and exam-style expectations.'

    return {
        'question': question,
        'answer': answer,
        'mcq_options': options,
        'explanation': explanation,
    }


def _english_cem(difficulty: str) -> dict:
    """
    Mixed UK-style entrance English practice items.
    """
    return _english_item_for_kinds(
        ['synonym', 'antonym', 'grammar', 'spelling', 'punctuation', 'comprehension'],
        difficulty
    )


def _english_grammar(difficulty: str) -> dict:
    return _english_item_for_kinds(['grammar'], difficulty)


def _english_punctuation(difficulty: str) -> dict:
    return _english_item_for_kinds(['punctuation', 'spelling'], difficulty)


def _english_synonyms(difficulty: str) -> dict:
    return _english_item_for_kinds(['synonym'], difficulty)


def _english_antonyms(difficulty: str) -> dict:
    return _english_item_for_kinds(['antonym'], difficulty)


def _english_comprehension(difficulty: str) -> dict:
    return _english_item_for_kinds(['comprehension'], difficulty)


def _english_creative_writing(difficulty: str) -> dict:
    return _english_item_for_kinds(['creative-writing'], difficulty)


def _english_narrative_writing(difficulty: str) -> dict:
    return _english_item_for_kinds(['narrative-writing'], difficulty)


def _english_non_chronological_report(difficulty: str) -> dict:
    return _english_item_for_kinds(['non-chronological-report'], difficulty)


# ---------------------------------------------------------------------------
# Computers (subtopic-specific generators)
# ---------------------------------------------------------------------------
def _computer_item(module_id: str, difficulty: str) -> dict:
    banks = {
        'intro-it-safety': [
            ('Which is the safest password?', ['password123', 'Mia2024', 'Blue!Tiger92', '12345678'], 'Blue!Tiger92'),
            ('What should you do if a message asks for your home address online?', ['Share it if they seem friendly', 'Ignore/report and tell a trusted adult', 'Post only part of it', 'Send it privately'], 'Ignore/report and tell a trusted adult'),
        ],
        'spreadsheets-basics': [
            ('Which formula correctly adds cells A1 to A5?', ['=ADD(A1:A5)', '=SUM(A1:A5)', '=TOTAL(A1-A5)', '=PLUS(A1:A5)'], '=SUM(A1:A5)'),
            ('What does an absolute reference look like?', ['A1', '$A$1', 'A$1$', '1A$'], '$A$1'),
        ],
        'scratch-programming': [
            ('Which structure repeats instructions until a condition is met?', ['Sequence', 'Loop', 'Variable', 'Broadcast'], 'Loop'),
            ('In Scratch, what is a variable usually used for?', ['Changing sprite costume', 'Storing values like score', 'Drawing shapes', 'Stopping all scripts'], 'Storing values like score'),
        ],
        'block-programming': [
            ('Why create a custom block/function?', ['To make scripts run slower', 'To reuse code and reduce repetition', 'To remove variables', 'To avoid testing'], 'To reuse code and reduce repetition'),
            ('Which is best debugging practice?', ['Change many things at once', 'Test after each small change', 'Skip failed tests', 'Delete all scripts and restart'], 'Test after each small change'),
        ],
        'binary-systems': [
            ('What is denary 10 in binary?', ['1010', '1110', '1001', '1100'], '1010'),
            ('Which hexadecimal digit equals binary 1111?', ['A', 'C', 'F', '9'], 'F'),
        ],
        'binary-shifts': [
            ('What is the result of left shifting 0011 by 1?', ['0001', '0110', '0010', '1110'], '0110'),
            ('In two\'s complement (8-bit), what is the sign bit for negative numbers?', ['Least significant bit', 'Most significant bit', 'Middle bit', 'Parity bit'], 'Most significant bit'),
        ],
        'logic-gates': [
            ('What is the output of AND when inputs are 1 and 0?', ['0', '1', 'Depends on NOT', 'Undefined'], '0'),
            ('Which gate outputs 1 when inputs are different?', ['AND', 'OR', 'XOR', 'NOT'], 'XOR'),
        ],
        'circuit-design': [
            ('Why simplify a logic circuit?', ['To use more gates', 'To reduce complexity and cost', 'To remove inputs', 'To avoid truth tables'], 'To reduce complexity and cost'),
            ('What should you do before finalizing a logic circuit?', ['Skip testing', 'Create and test a truth table', 'Rename all wires only', 'Add random NOT gates'], 'Create and test a truth table'),
        ],
        'python-with-karel': [
            ('Which command moves Karel forward one square?', ['turn_left()', 'move()', 'put_beeper()', 'turn_right()'], 'move()'),
            ('How many turn_left() calls does Karel need to turn right?', ['1', '2', '3', '4'], '3'),
            ('What does put_beeper() do in Karel?', ['Moves Karel forward', 'Places a ball on Karel\'s square', 'Turns Karel left', 'Stops the program'], 'Places a ball on Karel\'s square'),
            ('What does pick_beeper() do?', ['Puts a ball down', 'Picks up a ball from Karel\'s square', 'Moves backward', 'Turns right'], 'Picks up a ball from Karel\'s square'),
            ('Which direction does Karel face at the start by default?', ['North', 'South', 'East', 'West'], 'East'),
            ('What brackets must follow a Karel command like move?', ['Square brackets []', 'Curly brackets {}', 'Round brackets ()', 'No brackets needed'], 'Round brackets ()'),
            ('What is Karel the Robot used for?', ['Playing games', 'Learning basic programming commands', 'Drawing pictures', 'Browsing the internet'], 'Learning basic programming commands'),
            ('How do you turn Karel to face the opposite direction?', ['One turn_left()', 'Two turn_left() calls', 'One move()', 'One put_beeper()'], 'Two turn_left() calls'),
            ('What happens if you call move() when there is a wall in front of Karel?', ['Karel flies over', 'Karel turns around', 'An error occurs', 'Karel places a beeper'], 'An error occurs'),
            ('What type of language is Karel?', ['A natural language', 'A simple programming language for beginners', 'A database language', 'A machine language'], 'A simple programming language for beginners'),
        ],
        'python-basics': [
            ('Which is a valid Python variable name?', ['2score', 'my-score', 'my_score', 'class'], 'my_score'),
            ('What does int("7") return?', ['"7"', '7', '7.0', 'Error always'], '7'),
        ],
        'python-control': [
            ('Which keyword starts a loop over a range in Python?', ['if', 'for', 'def', 'print'], 'for'),
            ('What is a common cause of infinite loops?', ['Clear stop condition', 'Wrong indentation', 'Missing update to loop variable', 'Using comments'], 'Missing update to loop variable'),
        ],
        'python-functions': [
            ('What does a function return statement do?', ['Repeats loop', 'Sends value back to caller', 'Prints only', 'Creates variable scope error'], 'Sends value back to caller'),
            ('Why use functions?', ['To duplicate code', 'To improve reuse and readability', 'To remove all parameters', 'To avoid testing'], 'To improve reuse and readability'),
        ],
        'python-data-structures': [
            ('Which data structure stores key-value pairs?', ['List', 'Tuple', 'Dictionary', 'String'], 'Dictionary'),
            ('What does list.append(x) do?', ['Removes x', 'Sorts list', 'Adds x to end of list', 'Replaces list with x'], 'Adds x to end of list'),
        ],
        'computer-architecture': [
            ('Which sequence is correct for CPU cycle?', ['Decode-Fetch-Execute', 'Fetch-Execute-Decode', 'Fetch-Decode-Execute', 'Execute-Fetch-Decode'], 'Fetch-Decode-Execute'),
            ('Which CPU part performs calculations?', ['Control Unit', 'ALU', 'RAM', 'Cache'], 'ALU'),
        ],
        'memory-storage': [
            ('Which storage is non-volatile?', ['RAM', 'Cache', 'SSD', 'Registers'], 'SSD'),
            ('How many MB are in 1 GB (binary approx in school context)?', ['100', '512', '1024', '2048'], '1024'),
        ],
        'data-representation': [
            ('What does higher image resolution usually mean?', ['Fewer pixels', 'More pixels', 'Smaller file always', 'No quality change'], 'More pixels'),
            ('ASCII/Unicode are used to represent what?', ['Sound', 'Text characters', 'Video frames', 'Network packets'], 'Text characters'),
        ],
        'input-output': [
            ('Which is an input device?', ['Monitor', 'Printer', 'Keyboard', 'Speaker'], 'Keyboard'),
            ('Which device is most suitable for accessibility text-to-speech output?', ['Microphone', 'Speaker/headphones', 'Scanner', 'Webcam'], 'Speaker/headphones'),
        ],
        'db-basics': [
            ('Which field should usually be unique for each record?', ['Name', 'Primary key', 'Address', 'Age'], 'Primary key'),
            ('A row in a database table is called what?', ['Field', 'Record', 'Schema', 'Query'], 'Record'),
        ],
        'db-sql-queries': [
            ('Which SQL command retrieves data from a table?', ['SELECT', 'INSERT', 'UPDATE', 'DELETE'], 'SELECT'),
            ('Which clause filters rows by condition?', ['ORDER BY', 'FROM', 'WHERE', 'GROUP'], 'WHERE'),
        ],
        'os-basics': [
            ('What is a core job of an operating system?', ['Design websites', 'Manage hardware and software resources', 'Write games automatically', 'Store only photos'], 'Manage hardware and software resources'),
            ('Which is most likely managed by the OS?', ['CPU scheduling', 'Essay writing', 'Drawing graphics manually', 'Math homework marking'], 'CPU scheduling'),
        ],
        'network-basics': [
            ('What does LAN stand for?', ['Large Access Network', 'Local Area Network', 'Linked Area Node', 'Long Address Number'], 'Local Area Network'),
            ('Which device routes traffic between networks?', ['Keyboard', 'Router', 'Monitor', 'Microphone'], 'Router'),
        ],
        'internet-protocols': [
            ('What does DNS mainly do?', ['Encrypt all internet traffic', 'Translate domain names to IP addresses', 'Store passwords', 'Block all ads'], 'Translate domain names to IP addresses'),
            ('An IP address is used to:', ['Name a folder', 'Identify a device on a network', 'Format text', 'Create a database key'], 'Identify a device on a network'),
        ],
        'web-basics': [
            ('HTTPS is mainly used for:', ['Faster graphics', 'Secure communication', 'Larger fonts', 'Offline browsing'], 'Secure communication'),
            ('The World Wide Web is best described as:', ['The same as electricity', 'A service running on the internet', 'A computer part', 'A type of keyboard'], 'A service running on the internet'),
        ],
        'ds-arrays-lists': [
            ('In most languages, the first index of an array/list is:', ['1', '0', '-1', '2'], '0'),
            ('Which operation adds an item to end of a list in Python?', ['append()', 'remove()', 'sort()', 'pop()'], 'append()'),
        ],
        'ds-stack-queue': [
            ('A stack follows which order?', ['FIFO', 'LIFO', 'Random', 'Alphabetic'], 'LIFO'),
            ('A queue follows which order?', ['LIFO', 'FIFO', 'Reverse only', 'Sorted only'], 'FIFO'),
        ],
        'algo-searching': [
            ('Binary search requires the list to be:', ['Random', 'Sorted', 'Duplicated', 'Encrypted'], 'Sorted'),
            ('Which search checks items one by one from start?', ['Binary search', 'Linear search', 'Hash search', 'Tree search'], 'Linear search'),
        ],
        'algo-sorting': [
            ('In bubble sort, what happens in each pass?', ['Only first item moves', 'Adjacent items are compared and swapped if needed', 'List is reversed fully', 'Items are encrypted'], 'Adjacent items are compared and swapped if needed'),
            ('Why sort data before some searches?', ['To use more memory', 'To improve search efficiency', 'To remove all duplicates automatically', 'To change data type'], 'To improve search efficiency'),
        ],
    }

    question, options, answer = random.choice(banks.get(module_id, banks['python-basics']))
    if difficulty == 'hard':
        explanation = f'"{answer}" is correct because it matches the key computing concept tested in this topic.'
    elif difficulty == 'easy':
        explanation = f'The correct choice is "{answer}".'
    else:
        explanation = f'"{answer}" is the correct option for this computing question.'
    return {
        'question': question,
        'answer': answer,
        'mcq_options': options,
        'explanation': explanation,
    }


def _intro_it_safety(difficulty: str) -> dict: return _computer_item('intro-it-safety', difficulty)
def _spreadsheets_basics(difficulty: str) -> dict: return _computer_item('spreadsheets-basics', difficulty)
def _scratch_programming(difficulty: str) -> dict: return _computer_item('scratch-programming', difficulty)
def _block_programming(difficulty: str) -> dict: return _computer_item('block-programming', difficulty)
def _binary_systems(difficulty: str) -> dict: return _computer_item('binary-systems', difficulty)
def _binary_shifts(difficulty: str) -> dict: return _computer_item('binary-shifts', difficulty)
def _logic_gates(difficulty: str) -> dict: return _computer_item('logic-gates', difficulty)
def _circuit_design(difficulty: str) -> dict: return _computer_item('circuit-design', difficulty)
def _python_with_karel(difficulty: str) -> dict: return _computer_item('python-with-karel', difficulty)
def _python_basics(difficulty: str) -> dict: return _computer_item('python-basics', difficulty)
def _python_control(difficulty: str) -> dict: return _computer_item('python-control', difficulty)
def _python_functions(difficulty: str) -> dict: return _computer_item('python-functions', difficulty)
def _python_data_structures(difficulty: str) -> dict: return _computer_item('python-data-structures', difficulty)
def _computer_architecture(difficulty: str) -> dict: return _computer_item('computer-architecture', difficulty)
def _memory_storage(difficulty: str) -> dict: return _computer_item('memory-storage', difficulty)
def _data_representation(difficulty: str) -> dict: return _computer_item('data-representation', difficulty)
def _input_output(difficulty: str) -> dict: return _computer_item('input-output', difficulty)
def _db_basics(difficulty: str) -> dict: return _computer_item('db-basics', difficulty)
def _db_sql_queries(difficulty: str) -> dict: return _computer_item('db-sql-queries', difficulty)
def _os_basics(difficulty: str) -> dict: return _computer_item('os-basics', difficulty)
def _network_basics(difficulty: str) -> dict: return _computer_item('network-basics', difficulty)
def _internet_protocols(difficulty: str) -> dict: return _computer_item('internet-protocols', difficulty)
def _web_basics(difficulty: str) -> dict: return _computer_item('web-basics', difficulty)
def _ds_arrays_lists(difficulty: str) -> dict: return _computer_item('ds-arrays-lists', difficulty)
def _ds_stack_queue(difficulty: str) -> dict: return _computer_item('ds-stack-queue', difficulty)
def _algo_searching(difficulty: str) -> dict: return _computer_item('algo-searching', difficulty)
def _algo_sorting(difficulty: str) -> dict: return _computer_item('algo-sorting', difficulty)


# ---------------------------------------------------------------------------
# Dispatcher
# ---------------------------------------------------------------------------
MODULE_GENERATORS = {
    'four-operations':          _four_operations,
    'fractions-decimals':       _fractions_decimals,
    'ratios':                   _ratios,
    'percentages':              _percentages,
    'multi-step-word-problems': _multi_step_word_problems,
    'mental-arithmetic':        _mental_arithmetic,
    'speed-based-calculation':  _speed_based_calculation,
    'logical-number-puzzles':   _logical_number_puzzles,
    'probability':              _probability,
    'algebra':                  _algebra,
    'perimeter-area':           _perimeter_area,
    'angles':                   _angles,
    'coordinate-geometry':      _coordinate_geometry,
    'volumes':                  _volumes,
    'verbal-reasoning':         _verbal_reasoning,
    'verbal-reasoning-level-1': _verbal_reasoning,
    'verbal-reasoning-level-2': _verbal_reasoning,
    'verbal-reasoning-cem-vocab-codes': _verbal_reasoning,
    'verbal-reasoning-cem-sequences-analogies': _verbal_reasoning,
    'non-verbal-reasoning':     _non_verbal_reasoning,
    'nvr-cem-pattern-matrices': _nvr_cem_pattern_matrices,
    'nvr-cem-rotations-reflections': _nvr_cem_rotations_reflections,
    'nvr-cem-odd-one-out':      _nvr_cem_odd_one_out,
    'nvr-cem-3d-nets':          _nvr_cem_3d_nets,
    'english-cem':              _english_cem,
    'grammar':                  _english_grammar,
    'punctuation':              _english_punctuation,
    'synonyms':                 _english_synonyms,
    'antonyms':                 _english_antonyms,
    'comprehension':            _english_comprehension,
    'creative-writing':         _english_creative_writing,
    'narrative-writing':        _english_narrative_writing,
    'non-chronological-report': _english_non_chronological_report,
    'intro-it-safety':          _intro_it_safety,
    'spreadsheets-basics':      _spreadsheets_basics,
    'scratch-programming':      _scratch_programming,
    'block-programming':        _block_programming,
    'binary-systems':           _binary_systems,
    'binary-shifts':            _binary_shifts,
    'logic-gates':              _logic_gates,
    'circuit-design':           _circuit_design,
    'python-with-karel':        _python_with_karel,
    'python-basics':            _python_basics,
    'python-control':           _python_control,
    'python-functions':         _python_functions,
    'python-data-structures':   _python_data_structures,
    'computer-architecture':    _computer_architecture,
    'memory-storage':           _memory_storage,
    'data-representation':      _data_representation,
    'input-output':             _input_output,
    'db-basics':                _db_basics,
    'db-sql-queries':           _db_sql_queries,
    'os-basics':                _os_basics,
    'network-basics':           _network_basics,
    'internet-protocols':       _internet_protocols,
    'web-basics':               _web_basics,
    'ds-arrays-lists':          _ds_arrays_lists,
    'ds-stack-queue':           _ds_stack_queue,
    'algo-searching':           _algo_searching,
    'algo-sorting':             _algo_sorting,
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
