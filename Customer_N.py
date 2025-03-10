sold_to_info = {
    "sold_to_num": "nsp_35499"  
}




ship_to_info = {
    "csh_1": "MAGA1",
    "csh_2": "MAGA2",
}



def extract_prompt(retrieved_text):
    return f"""
    You are an expert at reading purchase orders. From the text below, extract **only the exact content** from the document without paraphrasing or summarizing.

    Return the following details exactly as they appear in the text in this format:

    {{
        "Purchase Order Number": "",
        "Quantity": "",
        "Required Delivery Date": "",
        "Material Number": "",
        "Deliver to": ""
    }}

    **Instructions:**
    - **Required Delivery Date**: Look for a delivery date in the format **MM/DD/YYYY**.
    - **Deliver to**: Extract the shipping address that starts with the facility name.
    - **Do not include** contact details like phone numbers, emails, or names of people.
      - Include the company name, street address, city, state, and zip code.

    **Do not modify or summarize the content. Only retrieve exact text from the document.**

    Here is the relevant purchase order text:

    {retrieved_text}
    """

def refine_prompt(extracted_info):
    return f"""
    You are an expert at processing purchase orders. Refine the following extracted information to match the specified format.

    Original extracted information:
    {extracted_info}

    **Instructions:**
    - **Quantity**: if the unit of measure is lb keep the unit of measure as lb and ensure the number is formatted with commas as thousands separators and periods as decimal separators
    - **Required Delivery Date**: Remove any additional text and retain only the date in **MM/DD/YYYY** format.
    - **Deliver to**: Ensure the address is correctly formatted and remove any duplicate information.

    **Return ONLY the refined information in JSON format. Do NOT add any extra explanations, titles, or text.**

    {{
        "Purchase Order Number": "",
        "Quantity": "",
        "Required Delivery Date": "",
        "Material Number": "",
        "Deliver to": ""
    }}
    """




