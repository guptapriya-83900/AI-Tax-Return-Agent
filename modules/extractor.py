import pdfplumber
import os

def extract_data_from_pdf(filepath):
    extracted_data = {}

    if not os.path.exists(filepath):
        return {"error": "File does not exist"}

    try:
        with pdfplumber.open(filepath) as pdf:
            full_text = ""
            for page in pdf.pages:
                full_text += page.extract_text() + "\n"

        extracted_data['raw_text'] = full_text

        # Try to infer form type
        if "W-2" in full_text:
            extracted_data['type'] = "W-2"
            extracted_data.update(parse_w2(full_text))
        elif "1099-NEC" in full_text:
            extracted_data['type'] = "1099-NEC"
            extracted_data.update(parse_1099_nec(full_text))
        elif "1099-INT" in full_text:
            extracted_data['type'] = "1099-INT"
            extracted_data.update(parse_1099_int(full_text))
        else:
            extracted_data['type'] = "unknown"

    except Exception as e:
        extracted_data['error'] = str(e)

    return extracted_data


def parse_w2(text):
    data = {}
    lines = text.splitlines()

    for line in lines:
        # Look for the W-2 income and tax line pattern
        if "Wage and Tax Statement" in line and any(char.isdigit() for char in line):
            # Example line: "Form W-2 Wage and Tax Statement 2023 1829.01 185.60"
            parts = line.strip().split()
            # Try to extract numbers at the end
            numbers = [p for p in parts if p.replace('.', '', 1).isdigit()]
            if len(numbers) >= 2:
                data['wages'] = numbers[-2]  # second last
                data['withheld'] = numbers[-1]  # last

    return data

def clean_number(val):
    return val.replace("$", "").replace(",", "")


def parse_1099_nec(text):
    data = {}
    lines = text.splitlines()
    for line in lines:
        if "Nonemployee compensation" in line:
            data['nonemployee_comp'] = extract_amount(line)
    return data


def parse_1099_int(text):
    data = {}
    lines = text.splitlines()
    for line in lines:
        if "Interest income" in line:
            data['interest_income'] = extract_amount(line)
    return data


def extract_amount(line):
    # Extract the last amount in the line (e.g., $9,456.00 or 9456.00)
    import re
    match = re.findall(r"\$?\d[\d,]*\.?\d{0,2}", line)
    if match:
        return match[-1].replace("$", "").replace(",", "")
    return None
