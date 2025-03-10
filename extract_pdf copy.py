from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
import sys
import json
from difflib import SequenceMatcher
from datetime import datetime
import Customer_G as Customer_G
import Customer_C as Customer_C
import Customer_N as Customer_N
import Customer_B as Customer_B
import Customer_BA as Customer_BA
from pdf_processing import extract_text_from_pdf, split_text
from llm_processing import embed_and_store, retrieve_most_relevant_chunk_with_confidence, extract_information_with_llm, refine_extracted_information

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def find_best_match(deliver_to, ship_info):
    best_match = None
    highest_ratio = 0.0
    for key, value in ship_info.items():
        ratio = SequenceMatcher(None, deliver_to, value).ratio()
        if ratio > highest_ratio:
            highest_ratio = ratio
            best_match = key
    return best_match

def modify_quantity_and_unit(info_dict):
    """Extract numeric value from Quantity and store Unit separately."""
    if "Quantity" in info_dict:
        quantity_value = info_dict["Quantity"]
        quantity_value = quantity_value.replace(",", "")  # Remove commas

        if "KG" in quantity_value.upper():
            numeric_value = quantity_value.split()[0]  # Extract numeric part
            info_dict["Quantity"] = numeric_value  # Store only the number
            info_dict["Unit"] = "KG"  # Store Unit separately
        elif "LB" in quantity_value.upper():
            numeric_value = float(quantity_value.split()[0]) / 2.2046  # Convert LB to KG
            info_dict["Quantity"] = f"{round(numeric_value, 3)}"
            info_dict["Unit"] = "KG"

def modify_delivery_date_format(info_dict):
    """Format Required Delivery Date to YYYY-MM-DD."""
    if "Required Delivery Date" in info_dict:
        try:
            original_date = info_dict["Required Delivery Date"]
            formatted_date = datetime.strptime(original_date, "%m/%d/%Y").strftime("%Y-%m-%d")
            info_dict["Required Delivery Date"] = formatted_date
        except ValueError:
            pass  # Keep the original format if parsing fails

@app.route('/api/process-purchase-order', methods=['POST'])
def process_purchase_order():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    customer = request.form.get('customer', 'BA')
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Get the appropriate customer module
            customer_modules = {
                'C': Customer_C,
                'N': Customer_N,
                'B': Customer_B,
                'G': Customer_G,
                'BA': Customer_BA,
            }
            
            module = customer_modules.get(customer.upper())
            if not module:
                return jsonify({'error': 'Invalid customer selection'}), 400
            
            extract_prompt = module.extract_prompt
            refine_prompt = module.refine_prompt
            
            # Process the PDF (Step 1)
            raw_text = extract_text_from_pdf(filepath, customer)
            text_chunks = split_text(raw_text)
            vectorstore = embed_and_store(text_chunks)
            
            query = "Purchase Order Number, Quantity in kg, Required Delivery Date, Material Number, deliver to"
            relevant_text = retrieve_most_relevant_chunk_with_confidence(vectorstore, query, threshold=0.8)
            
            # Step 2: Initial Extraction
            initial_extracted_info = extract_information_with_llm(relevant_text, extract_prompt)
            print(f"\n--- Initial Extracted Information for {filename} (Step 1) ---")
            print(initial_extracted_info)

            # Step 3: Refinement
            refined_info = refine_extracted_information(initial_extracted_info, refine_prompt)
            print(f"\n--- Refined Information for {filename} (Step 2) ---")
            print(refined_info)
            
            # Process the refined information
            refined_info_dict = json.loads(refined_info)

            # Step 4: Apply Fixes (Quantity & Unit)
            modify_quantity_and_unit(refined_info_dict)  # Fix Quantity & Unit
            modify_delivery_date_format(refined_info_dict)  # Fix Date Format
            
            # Step 5: Add sold-to info and process deliver-to address
            refined_info_dict.update(module.sold_to_info)
            deliver_to_address = refined_info_dict.get("Deliver to", "")
            ship_to_key = find_best_match(deliver_to_address, module.ship_to_info)
            
            if ship_to_key:
                refined_info_dict["Deliver to"] = ship_to_key
            
            # Step 6: Final Output Logging
            finaloutput = refined_info_dict
            print(f"\n===== FINAL OUTPUT for {filename} (Step 3) =====")
            print(json.dumps(finaloutput, indent=4))
            print("=================================")

            # Clean up the temporary file
            os.remove(filepath)
            
            return jsonify(finaloutput)
            
        except Exception as e:
            # Clean up the temporary file in case of error
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/api/customers', methods=['GET'])
def get_customers():
    customers = [
        {'value': 'C', 'label': 'Customer C'},
        {'value': 'N', 'label': 'Customer N'},
        {'value': 'B', 'label': 'Customer B'},
        {'value': 'G', 'label': 'Customer G'},
        {'value': 'BA', 'label': 'Customer BA'},
    ]
    return jsonify(customers)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
