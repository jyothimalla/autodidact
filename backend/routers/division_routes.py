from fastapi import APIRouter, Query
from typing import List
from pydantic import BaseModel
import random

router = APIRouter()

class Question(BaseModel):
    question: str
    answer: str
    explanation: str

names = ["Ava", "Lima", "Zoe", "Noah", "Emma", "Ethan", "Olivia", "Liam", "Sophia", "Mason", "Isabella", "Lucas", "Mia",
          "Aiden", "Charlotte", "Jackson", "Amelia", "Caden", "Harper", "Grayson", "Evelyn", "Elijah", "Abigail", "Oliver", "Ella", "James", "Scarlett", "Benjamin", "Avery", "Alexander",
            "Sofia", "Charlotte", "William", "Aria", "Daniel", "Chloe", "Matthew", "Layla", "Michael", "Luna", "Henry", "Nora",
            "Sebastian", "Zoey", "Jackson", "Mila", "Riley", "Joseph", "Aubrey", "Samuel", "Hannah", "Carter", "Lily", "John", "Addison", "Luke", "Grace",
            "Anthony", "Ellie", "Isaac", "Samantha", "Gabriel", "Aaliyah", "Christopher", "Natalie", "Andrew", "Zara", "Joshua", "Leah", "David", "Audrey",
            "Nathan", "Skylar", "Ryan", "Bella", "Isaiah", "Claire", "Dylan", "Savannah", "Wyatt", "Anna", "Caleb", "Stella",   "Jack", "Sophie", "Owen", 
            "Ariana", "Lucy", "Aaron", "Maya", "Charles", "Nina",
            "Thomas", "Lila", "Adam", "Mackenzie", "Eli", "Kinsley", "Jonathan", "Peyton", "Christian", "Arianna", "Hunter",  
           "Jaxon", "Autumn", "Levi", "Kaylee", "Asher", "Piper", "Landon", "Sadie", "Ezekiel", "Maddison", "Colton", "Alyssa",    
            "Jeremiah", "Lydia", "Evan", "Madelyn", "Gavin", "Adeline", "Chase", "Aubree", "Jace", "Kylie", "Jason", "Rylee",
            "Luca", "Ainsley", "Nolan", "Emery", "Zachary", "Katherine", "Brayden", "Sienna", "Silas", "Molly", "Sawyer", "Emilia",
            "Axel", "Ayla", "Lola", "Bentley", "Mckenzie", "Ryder", "Kaitlyn", "Luis", "Elena", "Diego", "Gianna",
            "Jasper", "Aubrielle", "Ember", "Brandon", "Lia", "Zane", "Miriam", "Bryson", "Sage", "Cameron", "Liana",
            "Jax", "Mya", "Kaden", "Lennon", "Riley", "Emberly", "Gage", "Sierra", "Kendall", "Tessa", "Dante", "Alina",
            "Kieran", "Mira", "Rocco","Finn", "Mabel", "Jett", "Alayna", "Koa", "Sabrina", "Troy", "Livia"]
items = ["Apples", "Books", "Coins", "Stickers", "Pencils", "Choclates", "Marbles", "Toys", "Cards", "Balloons", "Stamps", "Rocks", "Shells", "Buttons", "Leaves", "Flowers", "Crayons",
         "Stones", "Bottles", "Cups", "Plates", "Blocks", "Dolls", "Cars", "Trains", "Kites", "Bikes", "Balls", "Teddies",
         "Bubbles", "Paints", "Brushes", "Glasses", "Masks", "Hats", "Scarves", "Gloves", "Socks", "Shoes", "Belts", "Watches",
         "Necklaces", "Bracelets", "Earrings", "Rings", "Pins", "Brooches", "Keychains", "Magnets", "Cars", "Pens", "Markers",
         "Erasers", "Notebooks", "Folders", "Binders", "Paperclips", "Staplers", "Tape", "Glue", "Scissors", "Rulers", "Calculators",
         "Highlighters", "Sticky Notes", "Index Cards", "Thumbtacks", "Push Pins", "Rubber Bands", "Envelopes", "Mailers", "Labels",
         "Stickers", "Postcards", "Greeting Cards", "Calendars", "Planners", "Journals", "Sketchbooks"]
children = random.randint(5, 35)
stickers_per_sheet = random.choice([10, 12, 15])

@router.get("/division/questions", response_model=List[Question])
def get_division_questions(level: int = Query(0, ge=0, le=10)):
    questions = []
    for _ in range(10):
        if level == 0:
            # Single-digit ÷ single-digit
            divisor = random.randint(1, 9)
            dividend = random.randint(1, 9) * divisor
        elif level == 1:
            # Two-digit ÷ single-digit
            divisor = random.randint(2, 9)
            dividend = random.randint(10, 99) * divisor
        elif level == 2:
            # Three-digit ÷ two-digit
            divisor = random.randint(10, 99)
            dividend = random.randint(100, 999) * divisor
        elif level == 3:
            # Simple word problems
            item = random.choice(items)
            name = random.choice(names)

            people = random.randint(2, 9)
            total = people * random.randint(5, 20)
            question = f"{total} {items} are divided equally among {people} children. How many does each child get?"
            answer = str(total // people)
            explanation = f"{total} ÷ {people} = {total // people} {items} per child"
            questions.append(Question(question=question, answer=answer, explanation=explanation))
            continue
        elif level == 4:
            # Four-digit ÷ two-digit
            divisor = random.randint(10, 99)
            dividend = random.randint(1000, 9999) * divisor
        elif level == 5:
            # Five-/Six-digit ÷ two-digit, ask for remainder
            divisor = random.randint(10, 99)
            dividend = random.randint(10000, 999999)
            quotient = dividend // divisor
            remainder = dividend % divisor
            question = f"What is the remainder when {dividend} is divided by {divisor}?"
            answer = f"Remainder: {remainder}"
            explanation = f"{dividend} ÷ {divisor} = {quotient} remainder {remainder}"
            questions.append(Question(question=question, answer=answer, explanation=explanation))
            continue
        
        elif level == 6:
            # Harder word problems
            dividend = random.randint(1000, 3000)
            divisor = random.randint(20, 60)
            quotient = dividend // divisor
            remainder = dividend % divisor
            question = f"A company makes {dividend} {item}s and packs them in boxes of {divisor}. How many full boxes? How many {item}/s are left?"
            answer = f"Full boxes: {quotient}, Leftover: {remainder}"
            explanation = f"{dividend} ÷ {divisor} = {quotient} R {remainder}"
            questions.append(Question(question=question, answer=answer, explanation=explanation))
            continue
        elif level == 7:
            # Division-multiplication inverse
            product = random.randint(50, 200)
            divisor = random.randint(2, 10)
            dividend = product * divisor
            question = f"What number multiplied by {divisor} gives {dividend}?"
            answer = str(product)
            explanation = f"{dividend} ÷ {divisor} = {product}"
            questions.append(Question(question=question, answer=answer, explanation=explanation))
            continue
        elif level == 8:
            # Estimation
            dividend = random.randint(500, 1000)
            divisor = random.randint(7, 15)
            est_dividend = round(dividend, -1)
            est_divisor = round(divisor)
            question = f"Estimate: {dividend} ÷ {divisor} (round to nearest ten)"
            est_answer = round(est_dividend / est_divisor)
            answer = str(est_answer)
            explanation = f"Rounded: {est_dividend} ÷ {est_divisor} ≈ {est_answer}"
            questions.append(Question(question=question, answer=answer, explanation=explanation))
            continue
        elif level == 9:
            # Logic puzzle
            base = random.randint(3, 9)
            name1, name2, name3 = random.sample(["Ali", "Ben", "Chloe", "Diya", "Evan"], 3)
            total = base * 6
            question = (f"{name1}, {name2}, and {name3} have {total} sweets together.\n"
                        f"{name1} has double of what {name2} has. {name3} has the same as {name2}.\n"
                        f"How many sweets does {name1} have?")
            name2_share = total // 4
            name1_share = name2_share * 2
            answer = str(name1_share)
            explanation = f"Shares: {name2}: {name2_share}, {name3}: {name2_share}, {name1}: {name1_share}"
            questions.append(Question(question=question, answer=answer, explanation=explanation))
            continue
        elif level == 10:
            # Real-world scenario
            amount = random.randint(10000, 50000)
            workers = random.choice([8, 10, 12])
            share = amount // workers
            question = f"₹{amount} is shared equally among {workers} workers. How much does each worker get?"
            answer = f"₹{share}"
            explanation = f"{amount} ÷ {workers} = ₹{share}"
            questions.append(Question(question=question, answer=answer, explanation=explanation))
            continue

        # Default case for levels 0–3:
        quotient = dividend // divisor
        question = f"{dividend} ÷ {divisor} = "
        answer = str(quotient)
        explanation = f"Divide {dividend} by {divisor} to get {quotient}"
        questions.append(Question(question=question, answer=answer, explanation=explanation))

    return questions
