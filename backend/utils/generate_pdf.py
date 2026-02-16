from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO

def create_pdf_stream(questions, paper_id="Paper"):
    buffer = BytesIO()
    c = canvas.Canvas(buffer)
    y = 800
    c.drawString(50, y, f"Paper ID: {paper_id}")
    y -= 30

    for q in questions:
        c.drawString(50, y, f"{q['number']}. {q['question']}")
        y -= 30

    c.save()
    buffer.seek(0)
    return buffer



def create_pdf(file_path, questions):
    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4
    y = height - 50
    for i, q in enumerate(questions, start=1):
        c.drawString(50, y, f"{i}. {q['question']}")
        for opt_key, opt_text in q["options"].items():
            y -= 15
            c.drawString(70, y, f"   {opt_key}) {opt_text}")
        y -= 30
        if y < 100:
            c.showPage()
            y = height - 50
    c.save()
