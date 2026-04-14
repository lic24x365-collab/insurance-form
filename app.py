import os
import smtplib
import io
from flask import Flask, request, render_template
from pypdf import PdfReader, PdfWriter

app = Flask(__name__, template_folder='templates')

@app.route('/')
def home():
    # இதுதான் உங்கள் முதல் பக்கத்தைக் காட்டும்
    return render_template('index.html')

@app.route('/process-pdf', methods=['POST'])
def process_pdf():
    data = request.form.to_dict()
    # உங்கள் GitHub-ல் உள்ள அதே கோப்பு பெயர்
    pdf_path = "FEMILY MEDICARE PRPOSAL-1.pdf"
    
    if not os.path.exists(pdf_path):
        return f"பிழை: {pdf_path} கோப்பு சர்வரில் இல்லை!"

    reader = PdfReader(pdf_path)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)

    # படிவத் தரவுகள்
    field_values = {
        "ProposerName": data.get('proposer_name'),
        "IntermediaryCode": "AGN0004206",
        "SumInsured": data.get('sum_insured', "500000")
    }
    
    writer.update_page_form_field_values(writer.pages[0], field_values)
    return "படிவம் தயார்! (மின்னஞ்சல் வசதி இன்னும் இணைக்கப்படவில்லை)"

if __name__ == '__main__':
    app.run(debug=True)
