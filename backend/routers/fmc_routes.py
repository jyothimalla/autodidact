from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List, Optional
import random
from database import GeneratedProblem
from fastapi import Depends
from database import get_db
from sqlalchemy.orm import Session
from database import UserScore 
from database import Base
from database import FMCQuestionBank
from schemas import FMCQuestionCreate, FMCQuestionRead

router = APIRouter()

class FMCQuestion(BaseModel):
    question: str
    answer: str
    explanation: str

names = ["Ava", "Lima", "Zoe", "Noah", "Emma", "Ethan", "Olivia", "Liam", "Sophia", "Mason", "Isabella", "Lucas", "Mia",
          "Aiden", "Charlotte", "Jackson", "Amelia", "Caden", "Harper", "Grayson", "Evelyn", "Elijah", "Abigail", "Oliver", "Ella", "James", "Scarlett", "Benjamin", "Avery", "Alexander",
            "Sofia", "Charlotte", "William", "Aria", "Daniel", "Chloe", "Matthew", "Layla", "Michael", "Luna", "Henry", "Nora",
            "Sebastian", "Zoey", "Jackson", "Mila", "David", "Riley", "Joseph", "Aubrey", "Samuel", "Hannah", "Carter", "Lily", "John", "Addison", "Luke", "Grace",
            "Anthony", "Ellie", "Isaac", "Samantha", "Gabriel", "Aaliyah", "Christopher", "Natalie", "Andrew", "Zara", "Joshua", "Leah", "David", "Audrey",
            "Nathan", "Skylar", "Ryan", "Bella", "Isaiah", "Claire", "Dylan", "Savannah", "Wyatt", "Anna", "Caleb", "Stella",   "Jack", "Sophie", "Owen", "Ariana", "Luke", "Lucy", "Aaron", "Maya", "Charles", "Nina",
            "Thomas", "Lila", "Adam", "Mackenzie", "Eli", "Kinsley", "Jonathan", "Peyton", "Christian", "Arianna", "Hunter", "Serenity",    "Jaxon", "Autumn", "Levi", "Kaylee", "Asher", "Piper", "Landon", "Sadie", "Ezekiel", "Maddison", "Colton", "Alyssa",    
            "Jeremiah", "Lydia", "Evan", "Madelyn", "Gavin", "Adeline", "Chase", "Aubree", "Jace", "Kylie", "Jason", "Rylee",
            "Luca", "Ainsley", "Nolan", "Emery", "Zachary", "Katherine", "Brayden", "Sienna", "Silas", "Molly", "Sawyer", "Emilia",
            "Axel", "Ayla", "Jaxon", "Lola", "Bentley", "Mckenzie", "Ryder", "Kaitlyn", "Luis", "Elena", "Diego", "Gianna",
            "Jasper", "Aubrielle", "Kaden", "Ember", "Brandon", "Lia", "Zane", "Miriam", "Bryson", "Sage", "Cameron", "Liana",
            "Jax", "Mya", "Kaden", "Lennon", "Riley", "Emberly", "Gage", "Sierra", "Kendall", "Tessa", "Dante", "Alina",
            "Kieran", "Mira", "Rocco", "Liana", "Finn", "Mabel", "Jett", "Alayna", "Koa", "Sabrina", "Troy", "Livia",
            "Koa", "Mira", "Rocco", "Liana", "Finn", "Mabel", "Jett", "Alayna", "Koa", "Sabrina", "Troy", "Livia",]
items = ["Apples", "Books", "Coins", "Stickers", "Pencils", "Choclates", "Marbles", "Toys", "Cards", "Balloons", "Stamps", "Rocks", "Shells", "Buttons", "Leaves", "Flowers", "Crayons",
         "Stones", "Bottles", "Cups", "Plates", "Blocks", "Dolls", "Cars", "Trains", "Kites", "Bikes", "Balls", "Teddies",
         "Bubbles", "Paints", "Brushes", "Glasses", "Masks", "Hats", "Scarves", "Gloves", "Socks", "Shoes", "Belts", "Watches",
         "Necklaces", "Bracelets", "Earrings", "Rings", "Pins", "Brooches", "Keychains", "Magnets", "Cars", "Pens", "Markers",
         "Erasers", "Notebooks", "Folders", "Binders", "Paperclips", "Staplers", "Tape", "Glue", "Scissors", "Rulers", "Calculators",
         "Highlighters", "Sticky Notes", "Index Cards", "Thumbtacks", "Push Pins", "Rubber Bands", "Envelopes", "Mailers", "Labels",
         "Stickers", "Postcards", "Greeting Cards", "Calendars", "Planners", "Journals", "Sketchbooks", "Art Supplies", "Craft Kits",
         "Sewing Kits", "Knitting Kits", "Crochet Kits", "Embroidery Kits", "Beading Kits", "Jewelry Making Kits", "Model Kits", "Puzzle Kits",
         "Science Kits", "Experiment Kits", "Robotics Kits", "Coding Kits", "Electronics Kits", "Building Kits", "Construction Kits",
         "Gardening Kits", "Cooking Kits", "Baking Kits", "Art Kits", "Music Kits", "Dance Kits", "Sports Kits", "Fitness Kits"]
level_topics = {
    0: ["addition", "subtraction", "evenorodd"],
    1: ["multiplication", "division"],
    2: ["evenorodd", "time", "measurement"],
    3: ["fraction", "money", "probability", "geometry"],
    4: ["patterns", "codes", "guessing"],
    5: ["addition", "subtraction", "multiplication", "division", "evenorodd", "time", "measurement"],
    6: ["fraction", "money", "probability", "geometry", "images", "codes"],
    7: ["optionalQuestions"],
    8: ["optionalQuestions"],
    9: ["optionalQuestions"],
    10: ["optionalQuestions"]
}

def generate_fmc_problem(level: int):
    
    op = random.choice(level_topics.get(level, level_topics[0]))
    # op = random.choice(["addition", "subtraction", "multiplication", "division", "time", "fraction", 'evenorodd', "money", "probability", 'guessing', "measurement", "codes", "patterns", "geometry"])
    name1, name2, name3 = random.sample(names, 3)
    item = random.choice(items)
    
    ## Addition
    if op == "addition":
        if level == 0:

            a, b = random.randint(5, 10 + level), random.randint(1, 5 + level)
            question = (f"{name1} had {a} {item}. \n "
                        f"{name2} gave {name1} {b} more. \n"
                        f" How many does {name1} have now?")
            answer = str(a + b)
            explanation = f"{a} + {b} = {a + b}"
        elif level == 1:
            a, b = random.randint(5 + level, 10 + level * 2), random.randint(1, 5 + level)
            question = (f"{name1} had {a} {item}. \n "
                        f"{name2} gave {name1} {b} more. \n"
                        f" How many does {name1} have now?")
            answer = str(a + b)
            explanation = f"{a} + {b} = {a + b}"
        elif level == 2:    
            a, b, c = random.randint(5 + level, 10 + level * 2), random.randint(1, 5 + level), random.randint(1, 5 + level)
            question = (f"{name1} , {name2} and {name3} have {a+b+c} {items} between them. \n "
                        f"{name1} has the half the number of {items} that {name3} has. \n"
                        f"{name2} has {b} more than {name1}. \n"
                        f" How many {items} does {name1} have?")
            answer = str((a - b) // 3)
            explanation = f"{name1} has {(a - b) // 3} {items}, {name2} has {(a - b) // 3 + b} {items}, and {name3} has {(a - b) // 3 * 2} {items}."
        elif level == 3:
            a, b, c = random.randint(5 + level, 10 + level * 2), random.randint(1, 5 + level), random.randint(1, 5 + level)
            question = (f"{name1} , {name2} and {name3} have {a} {items} between them. \n "
                        f"{name1} has the half the number of {items} that {name3} has. \n"
                        f"{name2} has {b} more than {name1}. \n"
                        f" How many {items} does {name1} have?")
            answer = str((a - b) // 3)
            explanation = f"{name1} has {(a - b) // 3} {items}, {name2} has {(a - b) // 3 + b} {items}, and {name3} has {(a - b) // 3 * 2} {items}."

    ## Subtraction
    elif op == "subtraction":
        total = random.randint(10 + level, 20 + level * 2)
        taken = random.randint(1, total - 1)
        question = f"{name1} had {total} {item}. \n{name1} gave away {taken}. \n How many are left?"
        answer = str(total - taken)
        explanation = f"{total} - {taken} = {total - taken}"

    ## Multiplication
    elif op == "multiplication":
        count = random.randint(2, 4 + level)
        times = random.randint(2, 3 + level)
        question = f"{name1} has {count} boxes of {item}, each with {times} items. \n How many in total?"
        answer = str(count * times)
        explanation = f"{count} × {times} = {count * times}"

    ## Division
    elif op == "division":
        a = random.randint(2, 9)
        b = random.randint(20, 50)
        result = random.randint(2 + level, 10 + level)
        divisor = random.randint(1 + level, 5 + level)
        dividend = result * divisor
        if level == 0:
            question = f"{name1} has {dividend} {item}. \n {name1} wants to share them with {divisor} friends. \n How many does each friend get?"
        elif level == 1:
            question = f"{name1} has {dividend} {item}, shared equally among {divisor} friends. \n How many each?"
        elif level == 2:
            question = (f"{items} can be bought in packs of {a}.\n"
                       f"There are {b} pupils in class.\n"
                       f"How many packs must the teacher buy to be sure that everyone gets a {item} of their own?")
            answer = str((b + a - 1) // a)
            explanation = f"Total packs needed = {b} / {a} = {answer} (rounded up)"
       
    ## Time
    elif op == "time":
        hour1 = random.randint(1, 12)
        minute1 = random.randint(0, 59)
        hour2 = random.randint(1, 12)
        minute2 = random.randint(0, 59)
        question =( f"{name1} has a meeting at {hour1}:{minute1:02d}. \n"
                   f"It lasts {hour2} hours and {minute2} minutes. \n"
                    f" What time does it end? (Give your answer in HH:MM format)" )
        total_minutes = (hour1 * 60 + minute1 + hour2 * 60 + minute2) % 1440
        answer = f"{total_minutes // 60}:{total_minutes % 60:02d}"
        explanation = f"Start: {hour1}:{minute1:02d}, Duration: {hour2}h {minute2}m, End: {answer}"
   
    ## Fraction
    elif op == "fraction":
        name1, name2 = random.sample(names, 2)
        item = random.choice(["apples", "books", "blocks", "sweets"])
        total = random.randint(2, 10)
        part = random.randint(1, total - 1)
        fullCapacity = random.choice([100, 120, 160, 180, 150, 200, 250, 300])

        if level == 0:
            # Basic part of a whole
            question = (
                f"{name1} has {total} {item}.\n"
                f"{name2} took {part}/{total} of them.\n"
                f"How many did {name2} take?"
            )
            answer = str(part)
            explanation = f"{part}/{total} of {total} = {part}"

        elif level == 1:
            # One quarter from 3/4 bottle volume
            question = (
                f"{name1}'s water bottle holds {fullCapacity}ml when it is three quarters full.\n"
                f"How much does it hold when it is one quarter full?"
            )
            answer = str(fullCapacity // 3)
            explanation = f"If 3/4 = {fullCapacity}ml, then 1/4 = {fullCapacity // 3}ml"

        elif level == 2:
            # Improper to proper fraction
            a = random.randint(5, 10)
            b = random.randint(2, 5)
            improper = a * b + random.randint(1, b - 1)
            whole = improper // b
            remainder = improper % b
            question = (
                f"{name1} ate {improper}/{b} of a cake.\n"
                f"How many full cakes and parts did they eat?"
            )
            answer = f"{whole} and {remainder}/{b}"
            explanation = f"{improper}/{b} = {whole} + {remainder}/{b}"

        elif level == 3:
            # Image logic (assume frontend shows pie or image hint)
            question = (
                f"An image shows a circle divided into 8 equal parts.\n"
                f"{name1} shaded 3 parts.\n"
                f"What fraction of the shape is shaded?"
            )
            answer = "3/8"
            explanation = f"{name1} shaded 3 out of 8 = 3/8"

        elif level == 4:
            # Apply fraction to actual quantity
            quantity = random.choice([30, 45, 60, 90])
            numerator = random.choice([1, 2, 3])
            denominator = random.choice([3, 4, 5, 6])
            while quantity % denominator != 0:
                quantity = random.choice([30, 45, 60, 90])
            fraction_value = numerator * quantity // denominator
            question = (
                f"{name1} scored {numerator}/{denominator} of {quantity} marks in a test.\n"
                f"How many marks did {name1} score?"
            )
            answer = str(fraction_value)
            explanation = f"{numerator}/{denominator} of {quantity} = {fraction_value}"

    ## Even or Odd
    elif op == "evenorodd":
        number1 = random.randint(20, 50)
        number2 = random.randint(51, 99)
        type = ["even", "odd"]
        
        question = f"How many {type[random.randint(0,1)]} numbers are there between {number1} and {number2} ?"
        if type == "even":
            count = (number2 - number1) // 2 + 1
        else:
            count = (number2 - number1 + 1) // 2
        answer = str(count)
        explanation = f"There are {count} {type} numbers between {number1} and {number2}."

    ## Money  
    elif op == "money":
        total = random.randint(1, 100)
        spent = random.randint(1, total - 1)
        if level == 0:

            question = f"{name1} has ${total}. After spending ${spent}, how much is left?"
            answer = str(total - spent)
            explanation = f"${total} - ${spent} = ${total - spent}"
        elif level == 1:
            question = f"{name1} has ${total}. After spending ${spent}, how much is left?"
            answer = str(total - spent)
            explanation = f"${total} - ${spent} = ${total - spent}"
        elif level == 2:
            question = f"{name1} has ${total}. After spending ${spent}, how much is left?"
            answer = str(total - spent)
            explanation = f"${total} - ${spent} = ${total - spent}"
        elif level == 3:
            
            question = f"{name1} has ${total}. After spending ${spent}, how much is left?"
            answer = str(total - spent)
            explanation = f"${total} - ${spent} = ${total - spent}"
        elif level == 4:
            total_coins = random.randint(6, 15)
            while True:
                num_5p = random.randint(0, total_coins)
                num_2p = total_coins - num_5p
                total_value = 5 * num_5p + 2 * num_2p
                if total_value < 100 and total_value % 1 == 0:
                    break

            name1 = random.choice(names)
            question = (
                f"{name1} has {total_coins} coins in total.\n"
                f"They are only 2p and 5p coins.\n"
                f"The total value is {total_value}p.\n"
                f"How many 5p coins does {name1} have?"
            )
            answer = str(num_5p)
            explanation = (
                f"Let x be number of 5p coins.\n"
                f"Then {total_coins} - x are 2p coins.\n"
                f"5x + 2({total_coins - num_5p}) = {total_value}\n"
                f"So x = {num_5p}"
            )

    ## Probability
    elif op == "probability":
        total = random.randint(1, 100)
        favorable = random.randint(1, total - 1)
        question = f"The chance of {name1} winning a game is {favorable}/{total}. What is the probability?"
        answer = f"{favorable}/{total}"
        explanation = f"Probability = Favorable outcomes / Total outcomes = {favorable}/{total}"
   
   ## Guessing
    elif op == "guessing":
        number = random.randint(1, 100)
        question = f"{name1} is thinking of a number between 1 and 100. What is the chance of guessing it right?"
        answer = "1/100"
        explanation = "Only one number is correct out of 100."
    
    ## Measurement
    elif op == "measurement":
        length1 = random.randint(11, 100)
        a = random.randint(1, 10)
        length2 = random.randint(1, 10)
        name1 = random.choice(names)
        name2 = random.choice(names)
        if level == 0:
            question = (f"{name1} has a rope of {length1} cm. {name2} has a rope of {length2} cm. How long are they together?")
            answer = str(length1 + length2)
            explanation = f"{length1} cm + {length2} cm = {length1 + length2} cm"
        elif level == 1:
            question = (f"{name1} is knitting a scarf in a week.\n"
                        f"At the end of Monday his scarf measures {length1}cm.\n"
                            f"He knits another {a} cm every day."
                            f" How long is it at the end of Friday?")
            length2 = length1 + a * 5
            answer = str(length2)
            explanation = f"{length1} cm + {a} cm * 5 days = {length2} cm"

    ## Codes   
    elif op == "codes":
        code = random.randint(1000, 9999)
        question = f"{name1} has a secret code: {code}. What is the code?"
        answer = str(code)
        explanation = f"The code is {code}."
    
    ## Patterns
    elif op == "patterns":
        pattern = [random.randint(1, 10) for _ in range(5)]
        next_number = pattern[-1] + random.randint(1, 5)
        question = f"What comes next in the pattern: {', '.join(map(str, pattern))}?"
        answer = str(next_number)
        explanation = f"The next number is {next_number}."
    
    ## Geometry
    elif op == "geometry":
        shape = random.choice(["circle", "square", "rectangle"])
        if shape == "circle":
            radius = random.randint(1, 10)
            area = 3.14 * radius ** 2
            question = f"What is the area of a circle with radius {radius}?"
            answer = str(area)
            explanation = f"Area = π * r^2 = 3.14 * {radius}^2 = {area}"
        elif shape == "square":
            side = random.randint(1, 10)
            area = side ** 2
            question = f"What is the area of a square with side {side}?"
            answer = str(area)
            explanation = f"Area = side^2 = {side}^2 = {area}"
        else:
            length = random.randint(1, 10)
            width = random.randint(1, 10)
            area = length * width
            question = f"What is the area of a rectangle with length {length} and width {width}?"
            answer = str(area)
            explanation = f"Area = length * width = {length} * {width} = {area}"
    else:
        question = "Invalid operation"
        answer = "N/A"
        explanation = "N/A"

    return FMCQuestion(question=question, answer=answer, explanation=explanation)


@router.get("/fmc/questions", response_model=List[FMCQuestion])
def get_fmc_questions(level: int = 0):
    questions = []
    for _ in range(10):
        try:
            q = generate_fmc_problem(level)
            if q.question and q.answer and q.explanation:
                questions.append(q)
        except Exception as e:
            print(f"Error in generating FMC question: {e}")
    return questions

@router.get("/fmc/all")
def get_all_generated(db: Session = Depends(get_db)):
    return db.query(GeneratedProblem).order_by(GeneratedProblem.id.desc()).limit(10).all()

@router.get("/fmc/history")
def get_user_history(user_name: str, db: Session = Depends(get_db)):
    return db.query(GeneratedProblem).filter_by(user_name=user_name).order_by(GeneratedProblem.created_at.desc()).all()

@router.post("/fmc/evaluate")
def evaluate_fmc_submission(user_name: str, level: int, answers: List[str], db: Session = Depends(get_db)):
    questions = [generate_fmc_problem(level) for _ in range(10)]
    correct = sum(1 for a, q in zip(answers, questions) if a.strip().lower() == q.answer.strip().lower())
    
    db_score = UserScore(
        user_name=user_name,
        operation="fmc",
        level=level,
        score=correct,
        total_questions=10,
        is_completed=(correct == 10)
    )
    db.add(db_score)
    db.commit()

    if correct < 6:
        topic_list = ", ".join(level_topics[level])
        return {"score": correct, "message": f"Please review: {topic_list} before retrying this level."}
    else:
        return {"score": correct, "message": "Well done! You can move to the next level."}


@router.post("/fmc/admin/add")
def add_fmc_questions(questions: List[FMCQuestion], level: int, question_type: str, db: Session = Depends(get_db)):
    for q in questions:
        db_question = FMCQuestionBank(
            level=level,
            question_type=question_type,
            question=q.question,
            answer=q.answer,
            explanation=q.explanation
        )
        db.add(db_question)
    db.commit()
    return {"message": f"{len(questions)} questions added to database for level {level}."}

@router.get("/fmc/admin/questions", response_model=List[FMCQuestion])
def get_admin_questions(level: int = 0, db: Session = Depends(get_db)):
    return db.query(FMCQuestionBank).filter_by(level=level).all()

@router.get("/fmc/admin/export")
def export_questions(level: int = 0, db: Session = Depends(get_db)):
    questions = db.query(FMCQuestionBank).filter_by(level=level).all()
    return [q.__dict__ for q in questions if hasattr(q, "__dict__")]


# Admin: Add curated questions
@router.post("/fmc/admin/add", response_model=FMCQuestionRead)
def add_fmc_question(q: FMCQuestionCreate, db: Session = Depends(get_db)):
    db_q = FMCQuestionBank(**q.dict())
    db.add(db_q)
    db.commit()
    db.refresh(db_q)
    return db_q

# Admin: View all or filter by level/type
@router.get("/fmc/admin/questions", response_model=List[FMCQuestionRead])
def get_admin_questions(level: Optional[int] = None, qtype: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(FMCQuestionBank)
    if level is not None:
        query = query.filter(FMCQuestionBank.level == level)
    if qtype:
        query = query.filter(FMCQuestionBank.question_type == qtype)
    return query.all()

# Admin: Export for download
@router.get("/fmc/admin/export", response_model=List[FMCQuestionRead])
def export_all_fmc_questions(db: Session = Depends(get_db)):
    return db.query(FMCQuestionBank).all()