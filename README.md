# AI Tax Return Agent Prototype

A simplified AI-based system for preparing individual tax returns by:
- Uploading tax forms (W-2, 1099-NEC, 1099-INT)
- Extracting data using PDF parsing
- Calculating tax due or refund using IRS 2024 brackets
- Generating a downloadable Form 1040 PDF

## Features
- File upload interface (W-2/1099s)
- Auto-parsing of wages and withholding
- Refund calculation with standard deductions
- PDF generation of simplified Form 1040

## Tech Stack
- Python, Flask
- PDFPlumber (for parsing)
- ReportLab (for PDF generation)

## How to Run
```bash
git clone <your-repo>
cd ai_tax_agent
pip install -r requirements.txt
python app.py
