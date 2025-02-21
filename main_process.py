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
from llm_processing import (
    embed_and_store,
    retrieve_most_relevant_chunk_with_confidence,
    extract_information_with_llm,
    refine_extracted_information
)


# Function to process and refine purchase order
def process_and_refine_purchase_order(pdf_path):
    # Extract text from PDF using customer-specific parameters
    raw_text = extract_text_from_pdf(pdf_path, customer)
    text_chunks = split_text(raw_text)
    
    # Reinitialize the vectorstore for each file to ensure no residual state is kept.
    vectorstore = embed_and_store(text_chunks)
    
    query = "Purchase Order Number, Quantity in weight, Required Delivery Date, Material Number, deliver to"
    relevant_text = retrieve_most_relevant_chunk_with_confidence(vectorstore, query, threshold=0.9)

    # Optionally log the relevant text:
    # print("\n--- Retrieved Relevant Text Chunk ---")
    # print(relevant_text)

    # Extract and then refine information with a fresh LLM instance each time.
    initial_extracted_info = extract_information_with_llm(relevant_text, extract_prompt)
    print("\n--- Initial Extracted Information (Step 1) ---")
    print(initial_extracted_info)

    refined_info = refine_extracted_information(initial_extracted_info, refine_prompt)
    print("\n--- Refined Information (Step 2) ---")
    print(refined_info)
    
    try:
        refined_info_dict = json.loads(refined_info)
        print("\n--- Output Objects ---")
        for key, value in refined_info_dict.items():
            if key == "Quantity":
                if "LB" in value.upper():
                    value_numeric = float(value.replace(",", "").split()[0])
                    value_kg = round(value_numeric / 2.2046)
                    refined_info_dict[key] = f"{value_kg:,} kg"
            print(key, ":", refined_info_dict[key])

        refined_info_dict.update(module.sold_to_info)
        
        deliver_to_address = refined_info_dict.get("Deliver to", "")
        ship_to_key = find_best_match(deliver_to_address, module.ship_to_info)
        
        if ship_to_key:
            refined_info_dict["Deliver to"] = ship_to_key
        
        print_final_info(refined_info_dict)
        return refined_info_dict

    except json.JSONDecodeError:
        print("Error decoding JSON response.")
        return None


# Function to modify quantity and extract unit
def modify_quantity_and_unit(info_dict):
    if "Quantity" in info_dict:
        quantity_value = info_dict["Quantity"]
        if "KG" in quantity_value.upper():
            numeric_value = quantity_value.replace(",", "").split()[0]
            info_dict["Quantity"] = numeric_value
            info_dict["Unit"] = "KG"

# Function to modify delivery date format to YYYY-MM-DD
def modify_delivery_date_format(info_dict):
    if "Required Delivery Date" in info_dict:
        try:
            original_date = info_dict["Required Delivery Date"]
            formatted_date = datetime.strptime(original_date, "%m/%d/%Y").strftime("%Y-%m-%d")
            info_dict["Required Delivery Date"] = formatted_date
        except ValueError:
            pass  # Keep the original format if parsing fails

# Function to find the best match for the "Deliver to" address
def find_best_match(deliver_to, ship_info, threshold=0.2):
    best_match = None
    highest_ratio = 0.0
    for key, value in ship_info.items():
        ratio = SequenceMatcher(None, deliver_to, value).ratio()
        if ratio > highest_ratio:
            highest_ratio = ratio
            best_match = key

    # Return None if the best match's ratio is below the threshold
    if highest_ratio < threshold:
        return "N/A"

    return best_match

# Function to print final refined information
def print_final_info(info_dict):
    print("\n--- Final Processed Information ---")
    for key, value in info_dict.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    customer = 'b'
    customer_modules = {
        'C': Customer_C,
        'N': Customer_N,
        'B': Customer_B,
        'G': Customer_G,
        'BA': Customer_BA,
    }
    
    module = customer_modules.get(customer.upper())
    if module:
        extract_prompt = module.extract_prompt
        refine_prompt = module.refine_prompt
    else:
        print("Not able to respond. Please select customer first.")
        sys.exit()

    pdf_path = 'BERRY_PO_4290665.pdf'
    final_info = process_and_refine_purchase_order(pdf_path)

    # Modify final_info after JSON payload creation
    modify_quantity_and_unit(final_info)
    modify_delivery_date_format(final_info)

    # Convert the final_info to JSON payload
    js_payload = json.dumps(final_info, indent=4)
    print(js_payload)
