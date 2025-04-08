from fastapi import APIRouter, UploadFile, Form
from PIL import Image
import pytesseract
from database import SessionLocal, UserScore
from io import BytesIO

router = APIRouter()

@router.post("/upload-answersheet")
async def upload_answersheet(file: UploadFile, student_name: str = Form(...), operation: str = Form(...), level: int = Form(...)):
    image = Image.open(BytesIO(await file.read()))
    extracted_text = pytesseract.image_to_string(image)

    # Simple example logic (replace with actual mapping logic)
    correct_answers = ['A', 'C', 'B', 'D']  # Pull from DB
    student_answers = extracted_text.strip().split("\n")[:len(correct_answers)]

    score = sum(1 for s, c in zip(student_answers, correct_answers) if s.strip().upper() == c)
    
    db = SessionLocal()
    record = UserScore(
        user_name=student_name,
        operation=operation,
        level=level,
        score=score,
        total_questions=len(correct_answers),
        is_completed=(score == len(correct_answers))
    )
    db.add(record)
    db.commit()
    db.close()

    return {"message": "Answer sheet processed", "score": score}
