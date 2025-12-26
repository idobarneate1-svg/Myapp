from flask import Flask, request, render_template, redirect, url_for, jsonify, send_from_directory
import os
import shutil
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploaded_files'
app.config['ALLOWED_EXTENSIONS'] = {'*'}  # קבל כל סוג של קובץ

# וודא שתיקיית ההעלאות קיימת
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return True  # מאפשר כל סוג קובץ

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
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return jsonify({'files': files})

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

@app.route('/rejestracja/api/funds/quotes/chart/pricing', methods=['GET'])
def get_fund_pricing():
    """
    API endpoint to retrieve fund pricing data for chart visualization.
    
    Query Parameters:
        fundId (int): The fund identifier
        fromDate (str): Start date in format YYYY-MM-DD
        unitCategoryCode (str): Unit category code (e.g., 'A', 'B', etc.)
    
    Returns:
        JSON response with pricing data suitable for charting
    """
    # Get query parameters
    fund_id = request.args.get('fundId', type=int)
    from_date = request.args.get('fromDate')
    unit_category_code = request.args.get('unitCategoryCode', '')
    
    # Validate required parameters
    if not fund_id:
        return jsonify({'error': 'fundId parameter is required'}), 400
    
    if not from_date:
        return jsonify({'error': 'fromDate parameter is required'}), 400
    
    # Parse the from_date
    try:
        start_date = datetime.strptime(from_date, '%Y-%m-%d')
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    
    # Generate mock pricing data for the chart
    # In a real application, this would query a database
    pricing_data = []
    current_date = start_date
    base_price = 100.0 + (fund_id % 50)  # Different base price per fund
    
    # Generate data points from start date to today
    end_date = datetime.now()
    while current_date <= end_date:
        # Simulate price fluctuation
        day_offset = (current_date - start_date).days
        price = base_price + (day_offset * 0.1) + ((day_offset % 7) * 0.5)
        
        pricing_data.append({
            'date': current_date.strftime('%Y-%m-%d'),
            'price': round(price, 2),
            'unitCategoryCode': unit_category_code
        })
        
        current_date += timedelta(days=1)
    
    # Return the pricing data
    response = {
        'fundId': fund_id,
        'fromDate': from_date,
        'unitCategoryCode': unit_category_code,
        'data': pricing_data,
        'dataPoints': len(pricing_data)
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
