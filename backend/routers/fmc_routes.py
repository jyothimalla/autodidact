from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from typing import List, Optional
import random
from model import GeneratedProblem, User, UserScore, FMCQuestionSave, Base, FMCPaperSet
from database import get_db
from sqlalchemy.orm import Session
from schemas import FMCQuestionCreate, FMCQuestionRead
from datetime import datetime

from fastapi.responses import FileResponse
from openpyxl import Workbook
from reportlab.pdfgen import canvas

import os, json

router = APIRouter()

class FMCQuestion(BaseModel):
    question: str
    answer: str
    explanation: str

class FMCQuestionSaveModel(BaseModel):
    user_id: int
    level: int
    score: int
    questions: List[FMCQuestion]
    timestamp: Optional[datetime] = None 

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
    5: ["addition", "subtraction", "evenorodd"],
    0: ["multiplication", "division", "logicpattern"],
    2: ["evenorodd", "time", "measurement"],
    3: ["fraction", "money", "probability", "geometry"],
    4: ["patterns", "codes", "guessing"],
    1: ["addition", "subtraction", "multiplication", "division", "evenorodd", "time", "measurement", "fraction", "money","codes", "realworld", "fmc", "optionalQuestions"],
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
        ## Real-World Word Problems
    elif op == "realworld":
        template = random.choice(["coins", "mileage", "treats", "direction", "speed", "legs", "collision", "advancedrealworld"])

        if template == "coins":
            target = 8
            num_2p = random.randint(0, target // 2)
            remaining = target - 2 * num_2p
            num_1p = remaining
            total_coins = num_1p + num_2p
            question = f"What is the smallest number of coins which will make {target}p?"
            answer = str(total_coins)
            explanation = f"Use {num_2p} × 2p and {num_1p} × 1p coins → Total: {total_coins} coins"

        elif template == "mileage":
            cost_per_unit = random.choice([10, 20, 25])
            distance_per_charge = random.choice([20, 25, 30])
            travel_distance = distance_per_charge * random.randint(2, 5)
            total_cost = int(travel_distance / distance_per_charge * cost_per_unit)
            question = (f"It costs {cost_per_unit}p to charge {name1}'s scooter which can then travel {distance_per_charge} miles.\n"
                        f"How much would it cost to travel {travel_distance} miles?")
            answer = f"{total_cost}p"
            explanation = f"{travel_distance // distance_per_charge} × {cost_per_unit}p = {total_cost}p"

        elif template == "treats":
            num_kittens = random.randint(2, 6)
            treats_per_cat = random.randint(2, 4)
            total_cats = 1 + num_kittens
            total_treats = total_cats * treats_per_cat
            question = (f"{name1} the cat and her {num_kittens} kittens each eat {treats_per_cat} cat treats every day.\n"
                        f"How many treats altogether do they eat in one day?")
            answer = str(total_treats)
            explanation = f"{total_cats} × {treats_per_cat} = {total_treats}"

        elif template == "direction":
            direction = random.choice(["North", "East", "South", "West"])
            angle = random.choice([90, 180, 270])
            if angle == 90:
                directions = {"North": "East", "East": "South", "South": "West", "West": "North"}
            elif angle == 180:
                directions = {"North": "South", "East": "West", "South": "North", "West": "East"}
            else:
                directions = {"North": "West", "West": "South", "South": "East", "East": "North"}

            new_direction = directions[direction]
            question = (f"{name1} was facing {direction}. A bird spins {name1} {angle}° clockwise.\n"
                        f"What direction is {name1} now facing?")
            answer = new_direction
            explanation = f"{angle}° clockwise from {direction} is {new_direction}"

        elif template == "speed":
            distance = 1  # in miles
            time_min = random.choice([15, 20, 30])
            speed = round(distance / (time_min / 60), 2)
            question = (f"{name1} takes {time_min} minutes to cycle to school, which is {distance} mile away.\n"
                        f"What is {name1}'s average speed?")
            answer = f"{speed} mph"
            explanation = f"Speed = Distance ÷ Time = {distance} ÷ {time_min/60} = {speed} mph"

        elif template == "legs":
            parrots = cats = dogs = random.randint(1, 4)
            total_legs = parrots * 2 + cats * 4 + dogs * 4
            question = (f"A pet home has {parrots} parrots, {cats} cats, and {dogs} dogs.\n"
                        f"How many legs can the owner see?")
            answer = str(total_legs)
            explanation = f"2×{parrots} + 4×{cats} + 4×{dogs} = {total_legs}"

        elif template == "collision":
            spider_speed = random.randint(6, 9)
            slug_speed = random.randint(3, 6)
            distance = random.choice([44, 55, 66])
            time = distance // (spider_speed + slug_speed)
            question = (f"The spider and the slug are {distance} cm apart. The spider runs at {spider_speed} cm/sec and the slug slides at {slug_speed} cm/sec.\n"
                        f"How long until they meet?")
            answer = str(time) + " sec"
            explanation = f"{spider_speed} + {slug_speed} = {spider_speed + slug_speed} cm/sec → {distance} ÷ {spider_speed + slug_speed} = {time} sec"
        
        elif template == "advancedrealworld":
            subtemplate = random.choice([
                "sock_days", "digit_sum_year", "sugar_limit", "train_time",
                "apple_bags", "breath_seconds", "netball_tennis", "padlock_code",
                "chocolate_fraction", "keypad_rules"
            ])

            if subtemplate == "sock_days":
                total_socks = 18
                pairs = total_socks // 2
                wear_every = 3
                days = pairs * wear_every
                question = f"My maths teacher {name1} has {total_socks} socks ({pairs} pairs). He puts on clean socks every {wear_every} days. How many days can he wear these socks before washing them all?"
                answer = str(days)
                explanation = f"{pairs} pairs × {wear_every} days = {days} days"

            elif subtemplate == "digit_sum_year":
                start_year = random.choice([2022, 2013, 2004])
                current_sum = sum(map(int, str(start_year)))
                next_year = start_year + 1
                while sum(map(int, str(next_year))) != current_sum:
                    next_year += 1
                diff = next_year - start_year
                question = f"The digits of the year {start_year} total {current_sum}. How many years will it be until this happens again?"
                answer = str(diff)
                explanation = f"Next year with same digit sum is {next_year}, so {diff} years later."

            elif subtemplate == "sugar_limit":
                per_bar = 7.5
                max_sugar = 24
                bars = int(max_sugar // per_bar)
                question = f"A snack bar contains {per_bar}g of sugar. It is recommended that children aged 10 have at most {max_sugar}g of sugar daily. How many snack bars could you eat and not exceed this limit?"
                answer = str(bars)
                explanation = f"{max_sugar} ÷ {per_bar} = {bars} bars (rounded down)"

            elif subtemplate == "train_time":
                normal_speed = 50
                time = 3
                distance = normal_speed * time
                fast_speed = 150
                fast_time = round(distance / fast_speed, 2)
                question = (f"Dr {name1} says a train travelling at {normal_speed} mph can complete a journey in {time} hours. "
                            f"How long will it take a high-speed train at {fast_speed} mph to complete the same journey?")
                answer = f"{fast_time} hours"
                explanation = f"Distance = {distance} miles. Time = {distance} ÷ {fast_speed} = {fast_time} hrs"

            elif subtemplate == "apple_bags":
                num = random.choice([20, 40, 60, 80, 100])
                question = (f"{name1} has an apple orchard. She can put all apples into bags of 4 or 5 with no apples left over.\n"
                            f"Which of the following could be the number of apples?\nOptions: 20, 25, 30, 35, 40")
                answer = str(num)
                explanation = f"{num} is divisible by both 4 and 5."

            elif subtemplate == "breath_seconds":
                mins = 24
                secs = 37.36
                total = int(mins * 60 + secs)
                rounded = round(total)
                question = (f"{name1} holds their breath for {mins} minutes and {secs} seconds. "
                            f"How long is this in seconds (rounded to nearest)?")
                answer = str(rounded)
                explanation = f"{mins}×60 + {secs} = {total} ≈ {rounded} sec"

            elif subtemplate == "netball_tennis":
                netball_pct = 75
                tennis_pct = 60
                combined = round(netball_pct * tennis_pct / 100)
                question = (f"In a class, {netball_pct}% of children like netball. "
                            f"{tennis_pct}% of those also like tennis. What percentage like both?")
                answer = f"{combined}%"
                explanation = f"{netball_pct}% × {tennis_pct}% = {combined}%"

            elif subtemplate == "padlock_code":
                digit1 = random.randint(1, 9)
                digit3 = random.choice([3, 6, 9])
                digit2 = random.randint(digit3 + 1, 9)
                digit4 = 10 - digit1
                code = f"{digit1}{digit2}{digit3}{digit4}"
                question = (f"{name1} needs to open a padlock. Clues:\n"
                            f"1. Sum of first and last digits is 10.\n"
                            f"2. Third digit is a multiple of 3.\n"
                            f"3. Second digit is greater than third.\n"
                            f"4. Most digits are odd.\nWhat is the code?")
                answer = code
                explanation = f"Code: {code} satisfies all conditions."

            elif subtemplate == "chocolate_fraction":
                uneaten = 24
                total = int(uneaten * 5 / 1)  # if 1/5 is 24g, full is 120g
                eaten = total - uneaten
                question = f"{name1} ate four-fifths of a chocolate bar. {uneaten}g was left. How much did {name1} eat?"
                answer = f"{eaten}g"
                explanation = f"1/5 = {uneaten}, so 5/5 = {total}, 4/5 = {eaten}"

            elif subtemplate == "keypad_rules":
                code = "1368"  # a valid hardcoded one that fits constraints
                question = (f"A four-digit code must follow all these rules:\n"
                            f"• Must be even\n• Includes digit from each row & column of the keypad\n"
                            f"• Digits sum to even\nWhat is a possible code?")
                answer = code
                explanation = f"1368 is even, spans all rows & columns, digits add to even"
    
    ##Logic Pattern
    elif op == "logicpattern":
        subtemplate = random.choice(["digit_sum_year", "digit_sum_diff", "sum_product", "coin_combo"])

        if subtemplate == "digit_sum_year":
            start_year = random.choice([2022, 2013, 2004])
            current_sum = sum(map(int, str(start_year)))
            next_year = start_year + 1
            while sum(map(int, str(next_year))) != current_sum:
                next_year += 1
            diff = next_year - start_year
            question = f"The digits of the year {start_year} total {current_sum}. How many years will it be until this happens again?"
            answer = str(diff)
            explanation = f"Next year with same digit sum is {next_year}, so {diff} years later."

        elif subtemplate == "digit_sum_diff":
            for tens in range(1, 10):
                for ones in range(0, 10):
                    num = 10 * tens + ones
                    if (tens + ones == 12) and (abs(tens - ones) == 4):
                        question = (
                            f"A two-digit number is less than 100. "
                            f"The sum of the digits is 12 and the difference between them is 4. What is the number?"
                        )
                        answer = str(num)
                        explanation = f"{tens} + {ones} = 12 and |{tens} - {ones}| = 4 → number = {num}"
                        break

        elif subtemplate == "sum_product":
            # Find number pair with known sum & product
            target_sum = 15
            target_product = 54
            for x in range(1, target_sum):
                y = target_sum - x
                if x * y == target_product:
                    question = f"Two numbers add together to give {target_sum} and multiply together to give {target_product}.\nThe larger of the two numbers is?"
                    answer = str(max(x, y))
                    explanation = f"{x} + {y} = {target_sum}, {x} * {y} = {target_product} → larger = {max(x, y)}"
                    break

        elif subtemplate == "coin_combo":
            total_coins = 10
            for num_5p in range(1, total_coins):
                num_2p = total_coins - num_5p
                if 5 * num_5p + 2 * num_2p == 32:
                    question = (
                        f"Amanda has {total_coins} coins in her purse. They are 2p and 5p coins. "
                        f"The coins make 32p in total. How many 5p coins are there in Amanda’s purse?"
                    )
                    answer = str(num_5p)
                    explanation = f"5p × {num_5p} + 2p × {num_2p} = 32p"
                    break

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
        a = random.randint(2, 10)
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

    ## FMC Questions
    elif op == "fmc":
        question = f"{name1} has a secret code. What is the code?"
        answer = str(random.randint(1000, 9999))
        explanation = "The code is a random number between 1000 and 9999."

    ## Optional Questions
    elif op == "optionalQuestions":
        question = f"{name1} has a secret code. What is the code?"
        answer = str(random.randint(1000, 9999))
        explanation = "The code is a random number between 1000 and 9999."
    else:
        question = "Invalid operation"
        answer = "N/A"
        explanation = "N/A"

    return FMCQuestion(question=question, answer=answer, explanation=explanation)


@router.get("/fmc/questions", response_model=List[FMCQuestion])
def get_fmc_questions(level: int = 0):
    questions = []
    seen = set()
    while len(questions) < 40:
        try:
            q = generate_fmc_problem(level)
            # ensure valid and unique question text
            if q.question and q.answer and q.explanation and q.question not in seen:
                questions.append(q)
                seen.add(q.question)
        except Exception as e:
            print(f"Error in generating FMC question: {e}")
    
    return questions

@router.get("/fmc/questions", response_model=List[FMCQuestion])
def generate_dynamic_fmc_questions(level: int = 0):
    """Generate 10 fresh FMC problems dynamically without saving."""
    return [generate_fmc_problem(level) for _ in range(10)]

@router.post("/fmc/save-questions")
def save_user_attempt(data: FMCQuestionSaveModel, db: Session = Depends(get_db)):
    """Save a user's solved questions and their score."""
    attempt = GeneratedProblem(
        user_id=data.user_id,
        level=data.level,
        score=data.score,
        questions=json.dumps([q.dict() for q in data.questions]),
        timestamp=data.timestamp or datetime.utcnow()
    )
    db.add(attempt)
    db.commit()
    return {"message": "User FMC Attempt saved successfully."}

@router.get("/fmc/history/{user_name}")
def get_user_fmc_history(user_name: str, db: Session = Depends(get_db)):
    """Fetch a user's previous solved FMC history."""
    return db.query(GeneratedProblem).filter_by(user_name=user_name).order_by(GeneratedProblem.created_at.desc()).all()


# ---------------------------
# Evaluation Route
# ---------------------------

@router.post("/fmc/evaluate")
def evaluate_fmc_submission(user_name: str, level: int, answers: List[str], db: Session = Depends(get_db)):
    """Evaluate submitted FMC answers."""
    generated_questions = [generate_fmc_problem(level) for _ in range(10)]
    correct_count = sum(1 for submitted, generated in zip(answers, generated_questions) if submitted.strip().lower() == generated.answer.strip().lower())

    # Save score to UserScore table
    score_record = UserScore(
        user_name=user_name,
        operation="fmc",
        level=level,
        score=correct_count,
        total_questions=10,
        is_completed=(correct_count == 10)
    )
    db.add(score_record)
    db.commit()

    if correct_count < 6:
        return {"score": correct_count, "message": f"Please review the topics before retrying."}
    return {"score": correct_count, "message": "Excellent! You may proceed to the next level."}
