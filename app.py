import os
import io
from flask import Flask, request, render_template, send_file
from pypdf import PdfReader, PdfWriter

app = Flask(__name__, template_folder='templates')

@app.route('/')
def home():
    # 4-படிநிலை கொண்ட புதிய index.html-ஐக் காட்டும்
    return render_template('index.html')

@app.route('/process-pdf', methods=['POST'])
def process_pdf():
    # படிவத் தரவுகளைப் பெறுதல்
    data = request.form.to_dict()
    
    # PDF கோப்பு பெயர் (உங்கள் GitHub-ல் உள்ளவாறே)
    pdf_path = "FEMILY MEDICARE PRPOSAL-1.pdf"
    
    if not os.path.exists(pdf_path):
        return f"பிழை: {pdf_path} கோப்பு சர்வரில் இல்லை! தயவுசெய்து GitHub-ல் கோப்பு பெயரைச் சரிபார்க்கவும்."

    reader = PdfReader(pdf_path)
    writer = PdfWriter()
    
    # 6 பக்கங்களையும் காப்பி செய்தல்
    for page in reader.pages:
        writer.add_page(page)

    # PDF-ல் உள்ள கட்டங்களின் பெயர்களுக்குத் தரவுகளை மேப்பிங் செய்தல் [cite: 18-91]
    # குறிப்பு: PDF-ல் உள்ள கட்டங்களின் பெயர்கள் மாறினால் இதையும் மாற்ற வேண்டும்
    field_mapping = {
        "Name": data.get('name', ''),               # முன்மொழிபவர் பெயர் [cite: 18]
        "Date of Birth": data.get('dob', ''),       # பிறந்த தேதி [cite: 19]
        "Present Address": data.get('address', ''), # முகவரி [cite: 36]
        "Mobile": data.get('mobile', ''),           # மொபைல் எண் [cite: 46]
        "Nominee Name": data.get('nominee_name', ''), # வாரிசுதாரர் [cite: 50]
        "Sum Insured Options": data.get('sum_insured', '5 Lakhs'), # காப்பீட்டுத் தொகை [cite: 62]
        "Intermediary Code": "AGN0004206"           # உங்கள் நிரந்தர குறியீடு [cite: 5, 252]
    }
    
    # முதல் பக்கத்தில் தரவுகளைப் பதித்தல் [cite: 100]
    writer.update_page_form_field_values(writer.pages[0], field_mapping)

    # புதிய PDF-ஐ உருவாக்குதல்
    output_filename = f"Proposal_{data.get('name', 'Customer')}.pdf"
    output_stream = io.BytesIO()
    writer.write(output_stream)
    output_stream.seek(0)

    # முடிவாக அந்த PDF-ஐ வாடிக்கையாளர் டவுன்லோட் செய்ய அனுமதித்தல்
    return send_file(
        output_stream,
        as_attachment=True,
        download_name=output_filename,
        mimetype='application/pdf'
    )

if __name__ == '__main__':
    app.run(debug=True)
