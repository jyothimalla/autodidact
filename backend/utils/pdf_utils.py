from reportlab.pdfgen import canvas
from io import BytesIO

def create_pdf_stream(questions, paper_id):
    buffer = BytesIO()
    c = canvas.Canvas(buffer)
    y = 800
    c.drawString(50, y, f"Paper ID: {paper_id}")
    y -= 40

    for q in questions:
        c.drawString(50, y, f"{q['number']}. {q['question']}")
        y -= 30

    c.save()
    buffer.seek(0)
    return buffer
