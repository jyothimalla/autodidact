from sqlalchemy.orm import Session
from model import FMCQuestionSave

def save_answer(db, user_id, username, student_name, operation, level, sublevel, question_number, answer):
    db_answer = FMCQuestionSave(
        user_id=user_id,
        username=username,
        student_name=student_name,
        operation=operation,
        level=level,
        sublevel=sublevel,
        question_number=question_number,
        answer=answer
    )
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
