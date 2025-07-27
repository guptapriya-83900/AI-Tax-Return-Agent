from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
from werkzeug.utils import secure_filename
from modules.extractor import extract_data_from_pdf
from modules.tax_logic import calculate_tax
from flask import send_file
from modules.form_filler import generate_1040_pdf_bytes

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2 MB limit


# Utility function to check file type
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'files' not in request.files:
        return "No files uploaded", 400

    uploaded_files = request.files.getlist('files')
    personal_info = {
        'name': request.form.get('name'),
        'filing_status': request.form.get('filing_status'),
        'dependents': request.form.get('dependents')
    }

    saved_files = []
    for file in uploaded_files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            saved_files.append(filename)
        else:
            return "Only PDF files allowed", 400

    parsed_results = []
    for filename in saved_files:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        parsed = extract_data_from_pdf(filepath)
        parsed['filename'] = filename
        parsed_results.append(parsed)

    total_income = 0
    total_withheld = 0

    for parsed in parsed_results:
        if parsed.get('type') == 'W-2':
            total_income += float(parsed.get('wages', 0))
            total_withheld += float(parsed.get('withheld', 0))

    filing_status = personal_info['filing_status']
    tax_due, deduction_used, taxable_income = calculate_tax(total_income, filing_status)

    refund_or_owe = round(total_withheld - tax_due, 2)
    tax_summary = {
        'total_income': total_income,
        'standard_deduction': deduction_used,
        'taxable_income': taxable_income,
        'tax_due': tax_due,
        'withheld': total_withheld,
        'refund_or_owe': refund_or_owe
    }

    return render_template('result.html',
                           files=saved_files,
                           info=personal_info,
                           parsed_data=parsed_results,
                           tax_summary=tax_summary)


    # Step 3: return render_template('result.html',
    #                     files=saved_files,
    #                     info=personal_info,
    #                     parsed_data=parsed_results,
    #                     tax_summary=tax_summary)


# Pass to template
    # Step 2: return render_template('result.html', files=saved_files, info=personal_info, parsed_data=parsed_results)
    #Step 1: return render_template('result.html', files=saved_files, info=personal_info)

# Optional route to view uploaded file (for testing)
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route("/download_pdf", methods=["POST"])
def download_generated_pdf():
    name = request.form.get("name")
    filing_status = request.form.get("filing_status")

    summary = {
        "total_income": float(request.form.get("total_income")),
        "standard_deduction": float(request.form.get("standard_deduction")),
        "taxable_income": float(request.form.get("taxable_income")),
        "tax_due": float(request.form.get("tax_due")),
        "withheld": float(request.form.get("withheld")),
        "refund_or_owe": float(request.form.get("refund_or_owe"))
    }

    pdf_buffer = generate_1040_pdf_bytes(name, filing_status, summary)
    return send_file(pdf_buffer, mimetype="application/pdf", download_name="Form_1040.pdf", as_attachment=True)



if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
