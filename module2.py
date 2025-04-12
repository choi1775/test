
from flask import Flask, request, jsonify
import pdfplumber
import re

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze_pdf():
    file = request.files['file']
    keywords = request.form.getlist('keywords')
    results = {keyword: [] for keyword in keywords}
    with pdfplumber.open(file) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if text:
                lines = text.split('\n')
                for line_num, line in enumerate(lines, start=1):
                    for keyword in keywords:
                        if re.search(rf'\b{re.escape(keyword)}\b', line):
                            results[keyword].append({
                                'page': page_num,
                                'line': line_num,
                                'text': line.strip()
                            })
    return jsonify(results)
