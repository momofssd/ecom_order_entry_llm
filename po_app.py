from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json

# Import modularized components
from utils import allowed_file
from customer_handler import get_customer_module, get_all_customers, validate_user_permission
from po_processor import process_purchase_order_file

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/api/process-purchase-order', methods=['POST'])
def process_purchase_order():
    """API endpoint to process a purchase order PDF file."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    customer_code = request.form.get('customer', 'BA')
    user_data = request.form.get('user', None)
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not file or not allowed_file(file.filename, ALLOWED_EXTENSIONS):
        return jsonify({'error': 'Invalid file type'}), 400
    
    # Validate user permissions
    if not validate_user_permission(user_data, customer_code):
        return jsonify({'error': 'You do not have permission to access this customer'}), 403
    
    # Get the appropriate customer module
    customer_module = get_customer_module(customer_code)
    if not customer_module:
        return jsonify({'error': 'Invalid customer selection'}), 400
    
    try:
        # Process the purchase order
        result = process_purchase_order_file(file, customer_module, app.config['UPLOAD_FOLDER'])
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ===== DEFAULT CUSTOMER HANDLING =====
# This endpoint is specifically for the DEFAULT customer option
# It bypasses the regular processing flow (utils.py, po_process.py, llm_process.py)
# and uses standard_via_openai.py directly
@app.route('/api/process-default-purchase-order', methods=['POST'])
def process_default_purchase_order():
    """API endpoint to process a purchase order PDF file using standard_via_openai directly."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    user_data = request.form.get('user', None)
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not file or not allowed_file(file.filename, ALLOWED_EXTENSIONS):
        return jsonify({'error': 'Invalid file type'}), 400
    
    # Validate user permissions for DEFAULT customer
    if not validate_user_permission(user_data, 'DEFAULT'):
        return jsonify({'error': 'You do not have permission to access this customer'}), 403
    
    try:
        # Save the file temporarily
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        
        # Use standard_via_openai's extract_po_data function directly
        # This is where we directly use the output from standard_via_openai.py (imported as Customer_Default)
        # instead of going through the regular flow with po_processor.py
        import standard_via_openai
        result = standard_via_openai.extract_po_data(filename)
        
        # Clean up the temporary file
        if os.path.exists(filename):
            os.remove(filename)
            
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/customers', methods=['GET'])
def get_customers():
    """API endpoint to get a list of all available customers."""
    return jsonify(get_all_customers())

@app.route('/api/customer-ship-to/<customer>', methods=['GET'])
def get_customer_ship_to(customer):
    """API endpoint to get ship-to information for a specific customer."""
    # Get the appropriate customer module
    customer_module = get_customer_module(customer)
    if not customer_module:
        return jsonify({'error': 'Invalid customer selection'}), 400
    
    # Return the ship_to_info dictionary from the customer module
    return jsonify(customer_module.ship_to_info)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
