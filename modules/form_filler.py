from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER
import io

def generate_1040_pdf_bytes(name, filing_status, summary):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=LETTER)

    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, 750, "Simplified IRS Form 1040 - 2024")
    c.setFont("Helvetica", 12)
    c.drawString(50, 710, f"Name: {name}")
    c.drawString(50, 690, f"Filing Status: {filing_status.replace('_', ' ').title()}")
    c.drawString(50, 660, f"Total Income: ${summary['total_income']}")
    c.drawString(50, 640, f"Standard Deduction: ${summary['standard_deduction']}")
    c.drawString(50, 620, f"Taxable Income: ${summary['taxable_income']}")
    c.drawString(50, 600, f"Tax Due: ${summary['tax_due']}")
    c.drawString(50, 580, f"Total Withheld: ${summary['withheld']}")
    c.drawString(50, 560, f"Refund or Amount Owed: ${summary['refund_or_owe']}")

    c.setFont("Helvetica-Oblique", 10)
    c.drawString(50, 520, "This is a simplified demo version. Not for actual filing.")

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer
