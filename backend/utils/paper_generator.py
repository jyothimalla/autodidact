import os
from fpdf import FPDF

def generate_paper_pdf(operation: str, level: int) -> str:
    file_path = f"generated_papers/{operation}_level_{level}.pdf"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Paper for {operation.title()} Level {level}", ln=True, align='C')

    # Example content
    for i in range(1, 6):
        pdf.cell(200, 10, txt=f"Q{i}: Sample question for {operation} Level {level}", ln=True)

    pdf.output(file_path)
    return file_path
