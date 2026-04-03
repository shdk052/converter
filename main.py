from flask import Flask, render_template, request, send_file
import os
from pathlib import Path
import datetime
from PIL import Image
#
# img = Image.open("input.png")
# img.save("output.jpg")
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/con', methods=['POST'])
def convert():
    file = request.files.get('image')
    if not file:
        return "לא נבחר קובץ", 400

    os.makedirs("uploads", exist_ok=True)

    input_path = os.path.join("uploads", file.filename)
    file.save(input_path)

    img = Image.open(input_path)
    base_name = os.path.splitext(file.filename)[0]

    selected_format = request.form.get('format', 'png').lower()

    # המרת שם פורמט ל־Pillow
    pillow_format = selected_format.upper()
    if pillow_format == 'JPG':
        pillow_format = 'JPEG'

    # שם קובץ פלט
    output_filename = f"{base_name}.{selected_format}"
    output_path = os.path.join("uploads", output_filename)

    # המרה ל‑RGB אם JPEG
    if pillow_format == 'JPEG':
        img = img.convert('RGB')

    # שמירה בפורמט החדש
    img.save(output_path, format=pillow_format)

    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3000, debug=True)
