from fastapi import APIRouter, Query
from fastapi.responses import FileResponse
import os
import pandas as pd

router = APIRouter()

@router.get("/generate-paper-excel")
def generate_paper_excel(operation: str = Query(...), level: int = Query(...)):
    file_path = f"generated_papers/{operation}_level_{level}.xlsx"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Example questions (replace with your logic)
    data = {
        "Question Number": [1, 2, 3, 4, 5],
        "Question": [f"Sample {operation} question {i}" for i in range(1, 6)],
        "Answer": ["" for _ in range(5)]
    }

    df = pd.DataFrame(data)
    df.to_excel(file_path, index=False)

    return FileResponse(file_path, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", filename=os.path.basename(file_path))
