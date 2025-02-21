
sold_to_info = {
    "sold_to_num": "gsp_123"  
}


ship_to_info = {
    "gsh_1": "GALATA CHEMICALS, LLC 471 HIGHWAY 3142 HAHNVILLE LA 70057 US",
    "gsh_2": "GALATA CHEMICALS LLC RT 68 SOUTH; 465 HARTLEY DR RAVENSWOOD WV 26164 US HARTLEY OIL CO 126 SENECA DRIVE RIPLEY WV RIPLEY 25271 US",
}


def extract_prompt(retrieved_text):
    return f"""
    You are an expert at reading purchase orders. From the text below, extract **only the exact content** from the document without paraphrasing or summarizing.

    Return the following details exactly as they appear in the text in this format:

    {{
        "Document Number": "",
        "Quantity": "",
        "Delivery Date": "",
        "Material/Description": "",
        "Shipping Address": ""
    }}

    **Instructions:**
    - **Document Number**: it is a numbers followed to "Document Number".
    - **Delivery Date**: Look for a delivery date in the format **MM/DD/YYYY**.
    - **Material/Description**: it is a number following "Description"  not a description. it is not sabic number either
    - **Shipping Address**: Extract the shipping address that starts with the facility name.
    - **Quantity**: the unit of measure is KG
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
    - **Quantity**: the unit of measure is KG
    - **Required Delivery Date**: Remove any additional text and retain only the date in **MM/DD/YYYY** format.
    - **Please deliver to**: Ensure the address is correctly formatted and remove any duplicate information.

    **Return ONLY the refined information in JSON format. Do NOT add any extra explanations, titles, or text.**

    {{
        "Purchase Order Number": "",
        "Quantity": "",
        "Required Delivery Date": "",
        "Material Number": "",
        "Deliver to": ""
    }}
    """

