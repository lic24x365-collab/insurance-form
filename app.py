import os
import smtplib
import io
import sqlite3
from datetime import datetime
from flask import Flask, request, render_template, make_response, session, redirect, url_for
from pypdf import PdfReader, PdfWriter
from xhtml2pdf import pisa

app = Flask(__name__, template_folder='templates')
app.secret_key = 'msrk_farm_2026_safe'

# Database Path
DB_PATH = 'flower_mandi.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# --- ROUTES ---

@app.route('/')
def home():
    # இன்சூரன்ஸ் படிவம் முகப்பு
    return render_template('index.html')

@app.route('/msrk')
def msrk_index():
    # மார்க்கெட் பில் முகப்பு
    return "MSRK FARM Dashboard - (Add your HTML logic here)"

@app.route('/download_pdf')
def download_pdf():
    # நீங்கள் கேட்ட அந்த 6 COLUMN PDF LOGIC
    # (குறிப்பு: இங்கு தேவையான டேட்டாவை get_audit_data மூலம் எடுக்க வேண்டும்)
    
    html = f"""
    <html>
    <head>
        <style>
            @page {{ size: A4; margin: 1cm; }}
            body {{ font-family: Helvetica; font-size: 9pt; }}
            table {{ width: 100%; border-collapse: collapse; }}
            th, td {{ border: 0.5pt solid black; padding: 5px; text-align: center; }}
            th {{ background-color: #f2f2f2; font-weight: bold; }}
        </style>
    </head>
    <body>
        <h2 style="text-align:center;">MSRK FARM - AUDIT STATEMENT</h2>
        <table>
            <thead>
                <tr>
                    <th width="15%">DATE</th>
                    <th width="25%">PARTICULARS</th>
                    <th width="15%">SALE VAL</th>
                    <th width="15%">NET VAL</th>
                    <th width="15%">ADVANCE</th>
                    <th width="15%">AGRI EXP</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>14-04-2026</td>
                    <td>Jasmine 10kg x 200</td>
                    <td>2000.0</td>
                    <td>1800.0</td>
                    <td>0.0</td>
                    <td>50.0</td>
                </tr>
            </tbody>
        </table>
    </body>
    </html>"""
    
    result = io.BytesIO()
    pisa.CreatePDF(io.BytesIO(html.encode("UTF-8")), dest=result)
    resp = make_response(result.getvalue())
    resp.headers['Content-Type'] = 'application/pdf'
    return resp

# இன்சூரன்ஸ் PDF ப்ராசஸ்
@app.route('/process-pdf', methods=['POST'])
def process_pdf():
    # நாம் ஏற்கனவே செய்த இன்சூரன்ஸ் லாஜிக்
    return "Insurance PDF Processed Successfully"

if __name__ == '__main__':
    app.run(debug=True)
