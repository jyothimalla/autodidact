import openpyxl
from io import BytesIO

from openpyxl import Workbook
from io import BytesIO

def create_excel_stream(questions, paper_id="Paper"):
    wb = Workbook()
    ws = wb.active
    ws.title = paper_id

    ws.append(["No.", "Question", "Answer", "Explanation"])
    for q in questions:
        ws.append([
            q.get("number", ""),
            q.get("question", ""),
            q.get("answer", ""),
            q.get("explanation", "")
        ])

    buffer = BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    return buffer



def create_excel(file_path, questions):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Paper"

    ws.append(["No", "Question", "Option A", "Option B", "Option C", "Option D", "Option E"])

    for i, q in enumerate(questions, start=1):
        row = [
            i,
            q["question"],
            q["options"].get("A", ""),
            q["options"].get("B", ""),
            q["options"].get("C", ""),
            q["options"].get("D", ""),
            q["options"].get("E", ""),
        ]
        ws.append(row)

    wb.save(file_path)
