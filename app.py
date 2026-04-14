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

        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        can.setFont("Helvetica", 10)

        # --- துல்லியமான இடங்கள் (Corrected Coordinates) ---
        
        # 1. பெயர் (Name) - கோட்டின் மேல் சரியாக அமர
        can.drawString(100, 683, data.get('name', '').upper())
        
        # 2. பிறந்த தேதி (DOB) 
        can.drawString(100, 665, data.get('dob', ''))
        
        # 3. முகவரி (Address) - பல வரிகளாகப் பிரித்தல்
        address = data.get('address', '')
        can.drawString(120, 520, address[:40]) # முதல் வரி
        if len(address) > 40:
            can.drawString(120, 505, address[40:80]) # இரண்டாம் வரி

        # 4. மொபைல் எண் (Mobile)
        can.drawString(450, 440, data.get('mobile', ''))

        # 5. மருத்துவ விவரங்கள் (Section VI - Page 2-ல் வரவேண்டியது)
        # இப்போது முதல் பக்கத்தில் தெரியாமல் இருக்க இதைப் பக்கம் 2-க்கு மாற்ற வேண்டும்
        
        can.save()
        packet.seek(0)
        new_pdf = PdfReader(packet)

        existing_pdf = PdfReader(open(existing_pdf_path, "rb"))
        output = PdfWriter()

        for i in range(len(existing_pdf.pages)):
            page = existing_pdf.pages[i]
            if i == 0: # முதல் பக்கம்
                page.merge_page(new_pdf.pages[0])
            output.add_page(page)

        output_stream = io.BytesIO()
        output.write(output_stream)
        output_stream.seek(0)

        return send_file(
            output_stream,
            as_attachment=True,
            download_name=f"Fixed_Proposal_{data.get('name', 'Customer')}.pdf",
            mimetype='application/pdf'
        )
    except Exception as e:
        return f"System Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
