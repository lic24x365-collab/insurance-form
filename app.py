import os
import io
from flask import Flask, request, render_template, send_file
from pypdf import PdfReader, PdfWriter

app = Flask(__name__, template_folder='templates')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process-pdf', methods=['POST'])
def process_pdf():
    data = request.form.to_dict()
    pdf_path = "FEMILY MEDICARE PRPOSAL-1.pdf"
    
    if not os.path.exists(pdf_path):
        return f"பிழை: {pdf_path} கோப்பு சர்வரில் இல்லை!"

    reader = PdfReader(pdf_path)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)

    # பக்கம் 1 முதல் 6 வரை உள்ள அனைத்து கட்டங்களையும் இணைக்கும் மேப்பிங் [cite: 18-264]
    field_mapping = {
        # PAGE 1: Proposer & Coverage [cite: 18-91]
        "Name": data.get('name', ''),
        "Date of Birth": data.get('dob', ''),
        "Gender": data.get('gender', ''),
        "PAN": data.get('pan', ''),
        "Mobile": data.get('mobile', ''),
        "Present Address": data.get('address', ''),
        "Nominee Name": data.get('nominee_name', ''),
        "Nominee Relationship with the Proposer": data.get('nominee_rel', ''),
        "Sum Insured Options": data.get('sum_insured', '500000'),
        "INTERMEDIARY CODE": "AGN0004206", # உங்கள் முகவர் குறியீடு

        # PAGE 2: Insured Person 1 Details [cite: 104]
        "Name_1": data.get('m1_name', ''),
        "DOB_1": data.get('m1_dob', ''),
        "ABHA ID_1": data.get('m1_abha', ''),
        "Height_1": data.get('m1_ht', ''),
        "Weight_1": data.get('m1_wt', ''),
        "Blood Group_1": data.get('m1_bg', ''),

        # PAGE 2 & 5: Existing Insurance & Bank [cite: 117, 205]
        "Company": data.get('prev_co', ''),
        "Sum Insured_Prev": data.get('prev_sum', ''),
        "Bank Name": data.get('bank_name', ''),
        "Bank Account No": data.get('bank_acc', ''),
        "IFS Code": data.get('bank_ifsc', ''),

        # PAGE 3 & 4: Medical Questionnaire [cite: 168, 174]
        "Heart Diseases": data.get('med_heart', 'N'),
        "Diabetes": data.get('med_sugar', 'N'),
        "Blood Pressure": data.get('med_bp', 'N'),
        "Cancer": data.get('med_cancer', 'N')
    }
    
    # தரவுகளை PDF-ல் பதித்தல்
    for i in range(len(writer.pages)):
        writer.update_page_form_field_values(writer.pages[i], field_mapping)

    output_stream = io.BytesIO()
    writer.write(output_stream)
    output_stream.seek(0)

    return send_file(
        output_stream,
        as_attachment=True,
        download_name=f"Proposal_{data.get('name', 'Customer')}.pdf",
        mimetype='application/pdf'
    )

if __name__ == '__main__':
    app.run(debug=True)
