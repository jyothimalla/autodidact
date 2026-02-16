from openpyxl import Workbook
from io import BytesIO

def create_excel_stream(questions, paper_id):
    wb = Workbook()
    ws = wb.active
    ws.title = "Questions"

    ws.append(["No.", "Question", "Answer", "Explanation"])
    for q in questions:
        ws.append([q['number'], q['question'], q['answer'], q['explanation']])

    buffer = BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    return buffer
