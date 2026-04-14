import os
import io
from flask import Flask, request, render_template, send_file
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

app = Flask(__name__, template_folder='templates')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process-pdf', methods=['POST'])
def process_pdf():
    try:
        data = request.form.to_dict()
        existing_pdf_path = "FEMILY MEDICARE PRPOSAL-1.pdf"
        
        if not os.path.exists(existing_pdf_path):
            return "பிழை: PDF கோப்பு சர்வரில் இல்லை!"

        # 1. வாடிக்கையாளர் தகவல்களை ஒரு தற்காலிக PDF-ல் எழுதுகிறோம்
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        
        # பக்கம் 1-ல் தகவல்களை எழுதுதல் (Coordinates: X, Y)
        can.setFont("Helvetica", 10)
        can.drawString(100, 645, data.get('name', ''))  # பெயர்
        can.drawString(100, 625, data.get('dob', ''))   # பிறந்த தேதி
        can.drawString(100, 580, data.get('address', '')) # முகவரி
        can.drawString(450, 520, data.get('mobile', ''))  # மொபைல்
        
        # மருத்துவ விவரங்கள் (Medical Info Section VI) [cite: 120-194]
        # உதாரணமாக P1-க்கான பதில்கள்
        can.drawString(100, 400, f"Heart: {data.get('m1_hrt', 'N')}  Sugar: {data.get('m1_dia', 'N')}")
        
        can.save()
        packet.seek(0)
        new_pdf = PdfReader(packet)

        # 2. அசல் PDF-உடன் தகவல்களை இணைக்கிறோம்
        existing_pdf = PdfReader(open(existing_pdf_path, "rb"))
        output = PdfWriter()

        for i in range(len(existing_pdf.pages)):
            page = existing_pdf.pages[i]
            if i == 0: # முதல் பக்கத்தில் மட்டும் தகவல்களை ஒட்டுகிறோம்
                page.merge_page(new_pdf.pages[0])
            output.add_page(page)

        output_stream = io.BytesIO()
        output.write(output_stream)
        output_stream.seek(0)

        return send_file(
            output_stream,
            as_attachment=True,
            download_name=f"Filled_Proposal_{data.get('name', 'Customer')}.pdf",
            mimetype='application/pdf'
        )
    except Exception as e:
        return f"System Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
