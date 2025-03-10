from dotenv import dotenv_values
from openai import OpenAI
import PyPDF2
import re
import json
import os

# Add ship_to_info dictionary required by the frontend
ship_to_info = {
    "default_1": "Default Shipping Address 1",
    "default_2": "Default Shipping Address 2",
    "default_3": "Default Shipping Address 3"
}

def extract_text_from_pdf(pdf_filename):
    """Extract text content from a PDF file"""
    try:
        with open(pdf_filename, "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""

def fix_number_format(text):
    """Convert numbers formatted as 'xxx,xxx.xxx' to 'xxxxxx.xxx'"""
    return re.sub(r'(\d{1,3}),(\d{3}\.\d+)', r'\1\2', text)

def format_results_for_frontend(extracted_data):
    """Format the extracted data to match the expected frontend format"""
    # If the data is a dictionary with a nested array (like purchaseOrderLines or Order Lines)
    if isinstance(extracted_data, dict):
        # Check if there are any array fields
        array_fields = [k for k, v in extracted_data.items() if isinstance(v, list)]
        
        if array_fields:
            # Get the first array field
            array_field = array_fields[0]
            lines = extracted_data[array_field]
            
            # Get common fields from the top level
            common_fields = {
                "Customer Name": extracted_data.get("Customer Name", ""),
                "Purchase Order Number": extracted_data.get("Purchase Order Number", ""),
                "Required Delivery Date": extracted_data.get("Required Delivery Date", ""),
                "Delivery Address": extracted_data.get("Delivery Address", "")
            }
            
            # Process each line item
            results = []
            for line_item in lines:
                # If the line item has all fields, use those directly
                if all(field in line_item for field in ["Customer Name", "Purchase Order Number", "Required Delivery Date", "Delivery Address"]):
                    # Just use the line item directly
                    results.append(line_item)
                else:
                    # Combine common fields with line-specific fields
                    combined_item = common_fields.copy()
                    combined_item.update(line_item)
                    results.append(combined_item)
            
            return results
    
    # If the data is already an array, return it directly
    if isinstance(extracted_data, list):
        return extracted_data
    
    # If the data is a single object, return it as a single-item array
    return [extracted_data]

def extract_po_data(pdf_filename):
    """Extract purchase order data from a PDF file using OpenAI"""
    print(f"\n===== PROCESSING PDF: {pdf_filename} =====")
    # Load environment variables
    env_vars = dotenv_values(".env")
    api_key = env_vars.get("OPENAI_API_KEY")
    
    if not api_key:
        print("Error: OPENAI_API_KEY not found in .env file")
        return []
    
    # Initialize OpenAI client
    try:
        openai_client = OpenAI(api_key=api_key)
    except Exception as e:
        print(f"Error initializing OpenAI client: {e}")
        return []
    
    # Extract and process PDF text
    pdf_text = extract_text_from_pdf(pdf_filename)
    if not pdf_text:
        return []
    
    pdf_text = fix_number_format(pdf_text)
    
    # Define the system message
    system_message = (
        "You are an AI extracting relevant content from a purchase order. "
        "Find the following details and return ONLY a valid JSON object with these fields:"
        "\n- Customer Name (Look for terms and condition and header section)"
        "\n- Purchase Order Number"
        "\n- Required Delivery Date (convert to ISO format YYYY-MM-DD)" 
        "\n- Material Number (Extract from the line item section, ignore `material description`,usually in the same row as 'Order Qty' and 'UOM')"
        "\n- Order Quantity in kg (only the converted kg value, do not include pounds or extra text, round to the nearest integer)"
        "\n- Delivery Address (extract ONLY the 'SHIP TO' address, includes distribution name if it is there, ignore all other addresses including 'Vendor', 'Invoice', 'Billing', and any address containing 'PO Box')"
        "\n\nIMPORTANT: "
        "- Return ONLY a valid JSON object. Do NOT include explanations, introductions, or Markdown formatting."
        "- Ensure 'Order Quantity in kg' is a clean number without thousand separators or extra text."
        "- Ensure 'Required Delivery Date' follows ISO 8601 format (YYYY-MM-DD)."
        "- Ensure 'Delivery Address' is the correct 'SHIP TO' address."
        "- Ignore addresses related to 'Vendor', 'Invoice', 'Billing', 'Remit To', 'PO Box', or 'Mailing Address'."
        "- Ignore Material Number related to 'Vendor', 'Invoice', 'Billing', 'Remit To', 'PO Box', or 'Mailing "
        "- Ignore **Price per unit** label."
    )
    
    # Create the prompts for the API call
    user_prompt = f"Extract relevant details from the following purchase order:\n{pdf_text}"
    prompts = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_prompt},
    ]
    
    # Add the multiple line detection prompt
    prompts.append({
        "role": "system",
        "content": (
            "Analyze the purchase order details provided. If the item section contains more than one item number, this indicates there are multiple purchase order lines. "
            "In that case, extract and output each line separately as a JSON array, where each element represents a single purchase order line with all its details. "
            "If there's only one line, output it as a single JSON object. Ensure that no line is omitted."
        )
    })

    try:
        # Make the API call
        response = openai_client.chat.completions.create(
            model='gpt-4o',
            messages=prompts,
            temperature=0,
            top_p=0.1,
            response_format={"type": "json_object"}
        )
        
        # Parse the response
        raw_response = response.choices[0].message.content
        
        try:
            extracted_data = json.loads(raw_response)
        except json.JSONDecodeError:
            print("Received invalid JSON response. Attempting to fix...")
            
            # Try to extract JSON if it's wrapped in markdown code blocks
            if "```json" in raw_response:
                match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', raw_response)
                if match:
                    try:
                        extracted_data = json.loads(match.group(1))
                    except:
                        print("Failed to extract JSON from code block")
                        return []
            else:
                print("Could not parse JSON response")
                return []
        
        # Print the raw extracted data for debugging
        print("\n===== RAW EXTRACTED DATA =====")
        print(json.dumps(extracted_data, indent=2))
        
        # Format the results for the frontend
        results = format_results_for_frontend(extracted_data)
        
        # Print the formatted results
        print("\n===== FORMATTED RESULTS FOR FRONTEND =====")
        print(json.dumps(results, indent=2))
        
        return results
        
    except Exception as e:
        print(f"Error in PO extraction: {e}")
        return []

# Save extraction results to a JSON file and display them
def save_and_display_results(pdf_filename, results):
    """Save extraction results to a JSON file and display them"""
    if not results:
        print("Extraction failed - no data to save")
        return
        
    # Create output filename
    output_filename = f"{os.path.splitext(pdf_filename)[0]}_extraction.json"
    
    # Save results to JSON file
    with open(output_filename, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to {output_filename}")
    print("\nIndividual Line Items:")
    for i, line in enumerate(results):
        print(f"\nLine {i+1}:")
        print(json.dumps(line, indent=2))

# Main block for direct execution
if __name__ == '__main__':
    import sys
    
    # Use command line argument if provided, otherwise use default
    if len(sys.argv) > 1:
        pdf_filename = sys.argv[1]
    else:
        # Default PDF file to process
        pdf_filename = ""
        print(f"No PDF file specified. Using default: {pdf_filename}")
    
    print("\n===== STANDARD VIA OPENAI EXTRACTION =====")
    print(f"Processing file: {pdf_filename}")
    
    # Extract data from PDF
    result = extract_po_data(pdf_filename)
    
    # Save and display results
    save_and_display_results(pdf_filename, result)
