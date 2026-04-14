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
    try:
        data = request.form.to_dict()
        pdf_path = "FEMILY MEDICARE PRPOSAL-1.pdf"
        
        if not os.path.exists(pdf_path):
            return f"Error: {pdf_path} not found in the server!"

        reader = PdfReader(pdf_path)
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)

        # Section VI: Medical Information & Insured Persons Mapping [cite: 104, 122, 168-194]
        # PDF-ல் உள்ள கட்டங்களின் பெயர்களுடன் உங்கள் படிவத் தரவை இணைக்கிறோம்
        field_mapping = {
            # PAGE 1 & 2: Proposer & Persons
            "Name": data.get('name', ''),
            "Date of Birth": data.get('dob', ''),
            "Mobile": data.get('mobile', ''),
            "Aadhaar No.": data.get('aadhaar', ''),
            "Present Address": data.get('address', ''),
            "Nominee Name": data.get('nominee_name', ''),
            "Sum Insured Options": data.get('sum_insured', '500000'),
            "INTERMEDIARY CODE": "AGN0004206", #

            # Member 1 to 6 Details
            "m1_name": data.get('m1_name', ''), "m1_dob": data.get('m1_dob', ''),
            "m2_name": data.get('m2_name', ''), "m2_dob": data.get('m2_dob', ''),
            "m3_name": data.get('m3_name', ''), "m3_dob": data.get('m3_dob', ''),
            "m4_name": data.get('m4_name', ''), "m4_dob": data.get('m4_dob', ''),
            "m5_name": data.get('m5_name', ''), "m5_dob": data.get('m5_dob', ''),
            "m6_name": data.get('m6_name', ''), "m6_dob": data.get('m6_dob', ''),

            # Section VI: Lifestyle & Chronic Illness (All 6 Persons) [cite: 122-194]
            "m1_lic": data.get('m1_lic', 'N'), "m2_lic": data.get('m2_lic', 'N'),
            "m3_lic": data.get('m3_lic', 'N'), "m4_lic": data.get('m4_lic', 'N'),
            "m5_lic": data.get('m5_lic', 'N'), "m6_lic": data.get('m6_lic', 'N'),
            
            "m1_hrt": data.get('m1_hrt', 'N'), "m2_hrt": data.get('m2_hrt', 'N'),
            "m3_hrt": data.get('m3_hrt', 'N'), "m4_hrt": data.get('m4_hrt', 'N'),
            "m5_hrt": data.get('m5_hrt', 'N'), "m6_hrt": data.get('m6_hrt', 'N'),
            
            "m1_dia": data.get('m1_dia', 'N'), "m2_dia": data.get('m2_dia', 'N'),
            "m3_dia": data.get('m3_dia', 'N'), "m4_dia": data.get('m4_dia', 'N'),
            "m5_dia": data.get('m5_dia', 'N'), "m6_dia": data.get('m6_dia', 'N'),
            
            "m1_res": data.get('m1_res', 'N'), "m2_res": data.get('m2_res', 'N'),
            "m3_res": data.get('m3_res', 'N'), "m4_res": data.get('m4_res', 'N'),
            "m5_res": data.get('m5_res', 'N'), "m6_res": data.get('m6_res', 'N'),
            
            "m1_dig": data.get('m1_dig', 'N'), "m2_dig": data.get('m2_dig', 'N'),
            "m3_dig": data.get('m3_dig', 'N'), "m4_dig": data.get('m4_dig', 'N'),
            "m5_dig": data.get('m5_dig', 'N'), "m6_dig": data.get('m6_dig', 'N'),
            
            "med_details": data.get('med_details', ''),

            # Bank Details [cite: 205-209]
            "Bank Name": data.get('bank_name', ''),
            "Bank Account No": data.get('bank_acc', ''),
            "IFS Code": data.get('bank_ifsc', '')
        }
        
        # 6 பக்கங்களிலும் தரவுகளைப் பதித்தல்
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
    except Exception as e:
        return f"Internal Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
