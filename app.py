import sys
import json
from difflib import SequenceMatcher
from datetime import datetime
import streamlit as st
import concurrent.futures
import Customer_G as Customer_G
import Customer_C as Customer_C
import Customer_N as Customer_N
import Customer_B as Customer_B
import Customer_BA as Customer_BA
from pdf_processing import extract_text_from_pdf, split_text
from llm_processing import embed_and_store, retrieve_most_relevant_chunk_with_confidence, extract_information_with_llm, refine_extracted_information

# Function to process and refine purchase order
def process_and_refine_purchase_order(file_obj, extract_prompt, refine_prompt, module, customer):
    raw_text = extract_text_from_pdf(file_obj, customer)
    text_chunks = split_text(raw_text)
    vectorstore = embed_and_store(text_chunks)

    query = "Purchase Order Number, Quantity in kg, Required Delivery Date, Material Number, deliver to"
    relevant_text = retrieve_most_relevant_chunk_with_confidence(vectorstore, query, threshold=0.8)

    initial_extracted_info = extract_information_with_llm(relevant_text, extract_prompt)
    refined_info = refine_extracted_information(initial_extracted_info, refine_prompt)

    try:
        refined_info_dict = json.loads(refined_info)

        for key, value in refined_info_dict.items():
            if key == "Quantity" and "LB" in value.upper():
                value_numeric = float(value.replace(",", "").split()[0])
                value_kg = round(value_numeric / 2.2046, 3)
                refined_info_dict[key] = f"{value_kg:,} kg"

        refined_info_dict.update(module.sold_to_info)

        deliver_to_address = refined_info_dict.get("Deliver to", "")
        ship_to_key = find_best_match(deliver_to_address, module.ship_to_info)

        if ship_to_key:
            refined_info_dict["Deliver to"] = ship_to_key

        modify_quantity_and_unit(refined_info_dict)
        modify_delivery_date_format(refined_info_dict)

        return refined_info_dict

    except json.JSONDecodeError:
        return {"error": "Error decoding JSON response."}

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
            pass

# Function to find the best match for the "Deliver to" address
def find_best_match(deliver_to, ship_info):
    best_match = None
    highest_ratio = 0.0
    for key, value in ship_info.items():
        ratio = SequenceMatcher(None, deliver_to, value).ratio()
        if ratio > highest_ratio:
            highest_ratio = ratio
            best_match = key
    return best_match

# Streamlit App
st.title("Purchase Order Information Extractor")

# Sidebar for input options
with st.sidebar:
    st.header("Upload & Settings")
    uploaded_files = st.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=True)
    customer = st.selectbox("Select Customer", ['G', 'C', 'N', 'B', 'BA'])
    process_button = st.button("Process Purchase Orders")

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
    st.error("Not able to respond. Please select customer first.")
    st.stop()

if uploaded_files and process_button:
    all_results = {}

    # Process files in parallel to speed up processing
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_file = {
            executor.submit(
                process_and_refine_purchase_order,
                uploaded_file,
                extract_prompt,
                refine_prompt,
                module,
                customer
            ): uploaded_file
            for idx, uploaded_file in enumerate(uploaded_files, start=1)
        }

        for idx, (future, uploaded_file) in enumerate(future_to_file.items(), start=1):
            file_id = f"id{idx}"

            try:
                final_info = future.result()
                if "error" in final_info:
                    st.error(f"Error processing {uploaded_file.name}: {final_info['error']}")
                else:
                    all_results[file_id] = final_info
            except Exception as e:
                st.error(f"Error processing {uploaded_file.name}: {str(e)}")

    js_payload = json.dumps(all_results, indent=4)
    st.text(js_payload)

else:
    st.info("Please upload one or more PDF files to start processing.")
