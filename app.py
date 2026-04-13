import os
import smtplib
from flask import Flask, request
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from email.message import EmailMessage
import io

app = Flask(__name__)

EMAIL_ADDRESS = "support@lic2.in"
EMAIL_PASSWORD = "lic123" # கவனிக்க: உங்கள் App Password-ஐ இங்கே இடவும்

@app.route('/process-pdf', methods=['POST'])
def process_pdf():
    data = request.form.to_dict()
    client_photo = request.files.get('client_photo')

    reader = PdfReader("FEMILY_MEDICARE_PRPOSAL-1.pdf")
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)

    field_values = {
        "ProposerName": data.get('proposer_name'),
        "IntermediaryCode": "AGN0004206",
        "SumInsured": data.get('sum_insured', "500000"),
        "PhysicalPolicy": "Yes",
        "Declaration": "Yes"
    }
    
    writer.update_page_form_field_values(writer.pages[0], field_values)

    output_filename = f"Proposal_{data.get('proposer_name')}.pdf"
    with open(output_filename, "wb") as f:
        writer.write(f)

    # மின்னஞ்சல் அனுப்பும் பகுதி
    msg = EmailMessage()
    msg['Subject'] = f"New Proposal: {data.get('proposer_name')}"
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS
    msg.set_content("New insurance proposal attached.")
    with open(output_filename, 'rb') as f:
        msg.add_attachment(f.read(), maintype='application', subtype='pdf', filename=output_filename)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

    return "மின்னஞ்சல் அனுப்பப்பட்டது!"