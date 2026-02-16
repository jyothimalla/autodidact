from model import FMCQuestionSave, UserAnswer

from sqlalchemy.orm import Session

def save_answer(
    db: Session,
    user_id: int,
    username: str,
    operation: str,
    level: int,
    sublevel: str,
    question_number: int,
    answer: str,
):
    # TODO: replace AnswerModel with your actual table/model name
    record = UserAnswer(
        user_id=user_id,
        username=username,
        operation=operation,
        level=level,
        sublevel=sublevel,
        question_number=question_number,
        answer=answer,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record
