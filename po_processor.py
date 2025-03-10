import os
import json
from werkzeug.utils import secure_filename
from pdf_processing import extract_text_from_pdf, split_text
from llm_processing import embed_and_store, retrieve_most_relevant_chunk_with_confidence, extract_information_with_llm, refine_extracted_information
from utils import post_process_extracted_info

def process_purchase_order_file(file, customer_module, upload_folder):
    """
    Process a purchase order PDF file and extract information.
    
    Args:
        file: The uploaded file object
        customer_module: The customer module to use for processing
        upload_folder: The folder to save the uploaded file
        
    Returns:
        dict: The extracted and processed information
    """
    filename = secure_filename(file.filename)
    filepath = os.path.join(upload_folder, filename)
    
    try:
        # Save the file temporarily
        file.save(filepath)
        
        # Get the prompts from the customer module
        extract_prompt = customer_module.extract_prompt
        refine_prompt = customer_module.refine_prompt
        
        # Step 1: Process the PDF
        raw_text = extract_text_from_pdf(filepath, customer_module.__name__.split('_')[-1])
        text_chunks = split_text(raw_text)
        vectorstore = embed_and_store(text_chunks)
        
        query = "Purchase Order Number, Quantity in kg, Required Delivery Date, Material Number, deliver to"
        relevant_text = retrieve_most_relevant_chunk_with_confidence(vectorstore, query, threshold=0.80)
        
        # Step 2: Initial Extraction
        initial_extracted_info = extract_information_with_llm(relevant_text, extract_prompt)
        print(f"\n--- Initial Extracted Information for {filename} (Step 1) ---")
        
        # Step 3: Refinement
        refined_info = refine_extracted_information(initial_extracted_info, refine_prompt)
        print(f"\n--- Refined Information for {filename} (Step 2) ---")
        print(refined_info)
        
        # Process the refined information
        refined_info_dict = json.loads(refined_info)
        
        # Step 4: Post-process the extracted information
        final_info = post_process_extracted_info(refined_info_dict, customer_module)
        
        # Step 5: Final Output Logging
        print(f"\n===== FINAL OUTPUT for {filename} (Step 3) =====")
        print(json.dumps(final_info, indent=4))
        print("=================================")
        
        return final_info
        
    finally:
        # Clean up the temporary file
        if os.path.exists(filepath):
            os.remove(filepath)
