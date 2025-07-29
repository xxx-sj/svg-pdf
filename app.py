import os
import tempfile
from flask import Flask, request, send_file, jsonify
import cairosvg
from pypdf import PdfWriter
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>SVG to PDF Converter</title>
        <style>
            body { font-family: sans-serif; max-width: 800px; margin: auto; padding: 20px; text-align: center; }
            .upload-container { border: 2px dashed #ccc; padding: 20px; border-radius: 10px; margin: 20px 0; }
            #file-count { margin-top: 10px; color: #555; }
            .upload-btn { background-color: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin-top: 10px; }
            .upload-btn:hover { background-color: #45a049; }
        </style>
    </head>
    <body>
        <h1>SVG to PDF Converter</h1>
        <div class="upload-container">
            <form action="/convert" method="post" enctype="multipart/form-data">
                <h3>Upload your SVG files</h3>
                <input type="file" name="files" accept=".svg" required multiple onchange="updateFileCount(this)">
                <br>
                <p id="file-count">No files selected</p>
                <button type="submit" class="upload-btn">Convert to PDF</button>
            </form>
        </div>
        <script>
            function updateFileCount(input) {
                const fileCountEl = document.getElementById('file-count');
                if (input.files.length === 1) { fileCountEl.textContent = '1 file selected'; }
                else if (input.files.length > 1) { fileCountEl.textContent = `${input.files.length} files selected`; }
                else { fileCountEl.textContent = 'No files selected'; }
            }
        </script>
    </body>
    </html>
    '''

@app.route('/convert', methods=['POST'])
def convert_svg_to_pdf():
    # 'files' 라는 이름으로 여러 파일을 받습니다.
    files = request.files.getlist('files')

    if not files or files[0].filename == '':
        return jsonify({"error": "No files selected"}), 400

    merger = PdfWriter()
    temp_pdf_paths = []

    try:
        for file in files:
            if file and file.filename.endswith('.svg'):
                svg_content = file.read()
                
                # 각 SVG를 임시 PDF 파일로 변환합니다.
                temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
                temp_pdf_paths.append(temp_pdf.name)
                
                cairosvg.svg2pdf(bytestring=svg_content, write_to=temp_pdf.name)
                merger.append(temp_pdf.name)
                temp_pdf.close()

        if not temp_pdf_paths:
            return jsonify({"error": "No valid SVG files were found to convert."}), 400

        # 병합된 PDF를 메모리에 생성합니다.
        output_stream = BytesIO()
        merger.write(output_stream)
        merger.close()
        output_stream.seek(0)
        
        return send_file(
            output_stream,
            as_attachment=True,
            download_name='merged_output.pdf',
            mimetype='application/pdf'
        )

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": f"An error occurred during conversion: {str(e)}"}), 500
    finally:
        # 생성된 모든 임시 PDF 파일들을 삭제합니다.
        for path in temp_pdf_paths:
            if os.path.exists(path):
                os.remove(path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 