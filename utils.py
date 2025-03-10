from difflib import SequenceMatcher
from datetime import datetime
import json

def allowed_file(filename, allowed_extensions={'pdf'}):
    """Check if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def find_best_match(deliver_to, ship_info, threshold=0.3):
    """Find the best matching ship-to code for a delivery address."""
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
            info_dict["Quantity"] = f"{round(numeric_value)}"  # Round to nearest integer
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

def post_process_extracted_info(refined_info_dict, customer_module):
    """Apply post-processing to the extracted information."""
    # Apply fixes to quantity, unit, and date format
    modify_quantity_and_unit(refined_info_dict)
    modify_delivery_date_format(refined_info_dict)
    
    # Add sold-to info and process deliver-to address
    refined_info_dict.update(customer_module.sold_to_info)
    deliver_to_address = refined_info_dict.get("Deliver to", "")
    ship_to_key = find_best_match(deliver_to_address, customer_module.ship_to_info)
    
    if ship_to_key:
        refined_info_dict["Deliver to"] = ship_to_key
    
    return refined_info_dict
