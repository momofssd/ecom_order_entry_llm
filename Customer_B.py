sold_to_info = {
    "sold_to_num": "bsp_222"  
}


ship_to_info = {
    "bsh_1": "MAGA1",
    "bsh_2": "MAGA2",
}




def extract_prompt(retrieved_text):
    return f"""
    You are an expert at reading purchase orders. From the text below, extract **only the exact content** from the document without paraphrasing or summarizing.

    Return the following details exactly as they appear in the text in this format:

    {{
        "PO Number": "",
        "QUANTITY": "",
        "PROMISED  DELIVERY": "",
        "ITEM NUMBER": "",
        "SHIP TO": ""
    }}

    **Instructions:**
    - **PO Number**: A purely numeric **6-8 digit number** that follows **"PO Number"**.
    - ** PROMISED  DELIVERY**: Look for a delivery date in the format **MM/DD/YYYY**.
    - **ITEM NUMBER**:
      - It is a **numeric code** in a format like "182111 "**.
      - The item number **should not be mistaken for quantities or order numbers**.
      - Typically, it is a **longer numeric value** and appears in a dedicated field.
      - **IGNORE values that are followed by "LB", "KG", or other weight units.** 
        - **SHIP TO**: Extract the shipping address that starts with the facility name.It is not a POX BOX address. It should not includes "SABIC"

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

