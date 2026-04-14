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
            return f"Error: {pdf_path} not found!"

        reader = PdfReader(pdf_path)
        writer = PdfWriter()
        
        # அக்ரோஃபார்ம் சிக்கலைத் தவிர்க்க, பக்கங்களை அப்படியே காப்பி செய்கிறோம்
        for page in reader.pages:
            writer.add_page(page)

        # மருத்துவ விவரங்கள் மற்றும் உறுப்பினர்கள் விவரம் (Section VI முழுமையாக) [cite: 121-194]
        field_mapping = {
            "name": data.get('name', ''),
            "dob": data.get('dob', ''),
            "mobile": data.get('mobile', ''),
            "sum_insured": data.get('sum_insured', '500000'),
            "m1_lic": data.get('m1_lic', 'N'), "m2_lic": data.get('m2_lic', 'N'),
            "m1_hrt": data.get('m1_hrt', 'N'), "m2_hrt": data.get('m2_hrt', 'N'),
            "m1_dia": data.get('m1_dia', 'N'), "m2_dia": data.get('m2_dia', 'N'),
            "med_details": data.get('med_details', '')
        }

        # PDF-ல் AcroForm கட்டாயமில்லை என்பதை உறுதிப்படுத்துகிறோம்
        try:
            writer.update_page_form_field_values(writer.pages[0], field_mapping)
        except Exception:
            # ஒருவேளை AcroForm இல்லையென்றால், இந்த வரியைத் தவிர்த்து விடுகிறோம்
            pass

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
        return f"System Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
