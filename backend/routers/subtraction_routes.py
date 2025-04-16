from typing import List, Dict
import random
import pandas as pd
from fastapi import APIRouter, Query

router = APIRouter()

# Generate flow chain problems
def generate_flow_chain_problem() -> List[Dict]:
    questions = []
    for _ in range(10):
        start = random.randint(1, 9)
        multiplier = 0
        subtractor = random.randint(1, 5)
        final = random.randint(1, 10)
        temp = start * multiplier
        missing = final + subtractor - temp

        question = f"{start} → × {multiplier} → + ? → - {subtractor} = {final}"
        answer = str(missing)
        explanation = f"{start} × {multiplier} = {temp}, then ? = {final} + {subtractor} - {temp}"

        questions.append({
            "Type": "Flow Chain",
            "Question": question,
            "Answer": answer,
            "Explanation": explanation
        })
    return questions

# Generate symbolic shape problems
def generate_symbolic_shapes_problem() -> List[Dict]:
    questions = []
    for _ in range(5):
        triangle = random.randint(1, 9)
        pentagon = random.randint(1, triangle)
        hexagon = random.randint(1, 9)
        trapezium = 4

        question = (
            f"🟥 - 🟩 = {triangle - pentagon}\n"
            f"🟨 ÷ 2 = {trapezium // 2}\n"
            f"🟩 + 🟦 = {pentagon + hexagon}\n"
            f"What is the value of 🟥?"
        )

        answer = str(triangle)
        explanation = (
            f"🟩 = {pentagon}, 🟦 = {hexagon}, 🟥 = 🟩 + ({triangle - pentagon}) = {triangle}"
        )

        questions.append({
            "Type": "Symbolic Shapes",
            "Question": question,
            "Answer": answer,
            "Explanation": explanation
        })
    return questions

# Generate max option problems
def generate_max_option_problem() -> List[Dict]:
    questions = []
    for _ in range(5):
        a, b, c = random.sample(range(1, 5), 3)
        options = {
            "A": a + b - c,
            "B": b - a + c,
            "C": a + c - b,
            "D": c - b + a,
            "E": c - b - a
        }
        correct_option = max(options, key=options.get)

        question = (
            f"Which of the following gives the highest value?\n"
            f"A. {a} + {b} - {c}\n"
            f"B. {b} - {a} + {c}\n"
            f"C. {a} + {c} - {b}\n"
            f"D. {c} - {b} + {a}\n"
            f"E. {c} - {b} - {a}"
        )

        questions.append({
            "Type": "Max Option",
            "Question": question,
            "Answer": correct_option,
            "Explanation": f"Option {correct_option} gives the maximum value: {options[correct_option]}"
        })
    return questions

# Combine and show in DataFrame
df = pd.DataFrame(
    generate_flow_chain_problem() +
    generate_symbolic_shapes_problem() +
    generate_max_option_problem()
)

# 
# import ace_tools as tools; 
# tools.display_dataframe_to_user(name="Level 6–7 Questions", dataframe=df)
