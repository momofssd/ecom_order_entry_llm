
sold_to_info = {
    "sold_to_num": "gsp_123"  
}


ship_to_info = {
    "gsh_1": "MAGA1",
    "gsh_2": "MAGA2",
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
    - **deliver to**: Ensure the address is correctly formatted and remove any duplicate information.

    **Return ONLY the refined information in JSON format. Do NOT add any extra explanations, titles, or text.**

    {{
        "Purchase Order Number": "",
        "Quantity": "",
        "Required Delivery Date": "",
        "Material Number": "",
        "Deliver to": ""
    }}
    """

