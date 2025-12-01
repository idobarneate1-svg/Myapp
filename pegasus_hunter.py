from flask import Flask, request, render_template, redirect, url_for, jsonify, send_from_directory
import os
import shutil
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploaded_files'
app.config['ALLOWED_EXTENSIONS'] = {'*'}  # קבל כל סוג של קובץ

# סוגי קבצים נתמכים לתמונות וסרטונים
IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp', 'svg'}
VIDEO_EXTENSIONS = {'mp4', 'webm', 'ogg', 'mov', 'avi', 'mkv'}

# וודא שתיקיית ההעלאות קיימת
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return True  # מאפשר כל סוג קובץ

def get_file_type(filename):
    """מזהה את סוג הקובץ (תמונה, סרטון או אחר)"""
    if '.' in filename:
        ext = filename.rsplit('.', 1)[1].lower()
        if ext in IMAGE_EXTENSIONS:
            return 'image'
        elif ext in VIDEO_EXTENSIONS:
            return 'video'
    return 'other'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'אין קובץ בבקשה'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'לא נבחר קובץ'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return jsonify({'success': 'הקובץ הועלה בהצלחה', 'filename': filename})
    
    return jsonify({'error': 'סוג קובץ לא מורשה'}), 400

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/list_uploads')
def list_uploads():
    upload_folder = app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_folder):
        return jsonify({'files': []})
    
    files = os.listdir(upload_folder)
    files_with_types = []
    for f in files:
        file_type = get_file_type(f)
        files_with_types.append({
            'name': f,
            'type': file_type,
            'url': url_for('uploaded_file', filename=f)
        })
    return jsonify({'files': files_with_types})

@app.route('/scan_system', methods=['POST'])
def scan_system():
    # כאן נסרק את קבצי המערכת, בגרסה פשוטה נחזיר רק הודעה
    return jsonify({'status': 'סריקת קבצי מערכת החלה', 'path': '/system'})

@app.route('/scan_vendor', methods=['POST'])
def scan_vendor():
    return jsonify({'status': 'סריקת תיקיית vendor החלה', 'path': '/vendor'})

@app.route('/scan_data', methods=['POST'])
def scan_data():
    return jsonify({'status': 'סריקת תיקיית data החלה', 'path': '/data'})

@app.route('/scan_product', methods=['POST'])
def scan_product():
    return jsonify({'status': 'סריקת תיקיית product החלה', 'path': '/product'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
