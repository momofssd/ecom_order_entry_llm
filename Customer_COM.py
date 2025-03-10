sold_to_info = {
    "sold_to_num": "cosp_222"  
}


ship_to_info = {
    "comsh_1": "MAGA1",
    "comsh_2": "MAGA2",
}


def extract_prompt(retrieved_text):
    return f"""
    You are an expert at reading purchase orders. From the text below, extract **only the exact content** from the document without paraphrasing or summarizing.

    Return the following details exactly as they appear in the text in this format:

    {{
        "Purchase Order:": "",
        "Order Qty": "",
        "Delivery date": "",
        "Material: "",
        "Ship To": ""
    }}

    **Instructions:**
    - **Purchase Order**: A purely numeric that follows **"PO Date"**.It is a number starts with "8"
    --**Order Qty**: Order qty format is like **1000.000***. The order qty could have  unit of measure in "KG" or "Pound(s)". You need to keep the unit of measure. if identified unit of measure is "Pound(s)" use  "LB" as unit of measure. ignore **Price per unit** label
    - **Delivery date**: Look for a delivery date in the format **DD/MONTH/YYYY** that follows  "**Delivery date**"
    - **Material**: Material format is like **723495-1**, **5105304**,**1574555-1**,**45838-1**
    - **SHIP TO**: Extract the shipping address that starts with the facility name.Look for contents after "SHIP TO"

    **Important Extraction Rules:**
    - **DO NOT modify or summarize the content**—only extract exact values from the document.
    - **Ensure that the ITEM NUMBER is not confused with a quantity or unit of measure.**

    Here is the relevant purchase order text:

    {retrieved_text}
    """


def refine_prompt(extracted_info):
    return f"""
    You are an expert at processing purchase orders. Refine the following extracted information to match the specified format.

    Original extracted information:
    {extracted_info}

    **Instructions:**
    - **Quantity**: do not remove unit of measure
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
