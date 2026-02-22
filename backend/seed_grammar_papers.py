"""
Seed 20 Grammar School Entrance Exam Papers
Each paper has 50 multiple-choice questions covering all subjects
"""

import sys
from database import SessionLocal, engine
from model import GrammarPaper, Base
from generators.mcq_generator import generate_exam
from datetime import datetime

# Ensure tables exist
Base.metadata.create_all(engine)

def seed_grammar_papers():
    """Create 20 grammar school entrance exam papers"""
    db = SessionLocal()

    try:
        # Check if papers already exist
        existing_count = db.query(GrammarPaper).count()
        if existing_count >= 20:
            print(f"✓ {existing_count} grammar papers already exist. Skipping seed.")
            return

        print("Generating 20 Grammar School Entrance Exam Papers...")
        print("This may take a few minutes...\n")

        for paper_num in range(1, 21):
            # Check if this specific paper already exists
            existing = db.query(GrammarPaper).filter(
                GrammarPaper.paper_number == paper_num
            ).first()

            if existing:
                print(f"Paper {paper_num} already exists, skipping...")
                continue

            # Generate 50 questions with mixed difficulty
            questions = generate_exam(num_questions=50, difficulty='mixed')

            # Create paper record
            paper = GrammarPaper(
                paper_number=paper_num,
                title=f"Grammar School Entrance Practice Paper {paper_num}",
                difficulty='mixed',
                questions_json=questions
            )

            db.add(paper)
            db.commit()

            print(f"✓ Created Paper {paper_num}: {len(questions)} questions")

        print(f"\n✅ Successfully created {20 - existing_count} grammar school papers!")
        print(f"Total papers in database: {db.query(GrammarPaper).count()}")

    except Exception as e:
        print(f"❌ Error seeding papers: {e}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    seed_grammar_papers()
