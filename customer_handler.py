import json
import Customer_G as Customer_G
import Customer_C as Customer_C
import Customer_N as Customer_N
import Customer_B as Customer_B
import Customer_BA as Customer_BA
import Customer_COM as Customer_COM
# ===== DEFAULT CUSTOMER HANDLING =====
# Import standard_via_openai.py as the DEFAULT customer module (Customer_Default)
# This allows direct use of standard_via_openai.py's functions when DEFAULT is selected
# Note: There is no actual Customer_Default.py file - we're using standard_via_openai.py instead
import standard_via_openai as Customer_Default  # This is where standard_via_openai.py is imported as Customer_Default

# Dictionary mapping customer codes to their respective modules
CUSTOMER_MODULES = {
    'C': Customer_C,
    'N': Customer_N,
    'B': Customer_B,
    'G': Customer_G,
    'BA': Customer_BA,
    'COM': Customer_COM,
    'DEFAULT': Customer_Default
}

def get_customer_module(customer_code):
    """Get the appropriate customer module based on the customer code."""
    return CUSTOMER_MODULES.get(customer_code.upper())

def get_all_customers():
    """Get a list of all available customers."""
    customers = [
        {'value': 'C', 'label': 'Customer C'},
        {'value': 'N', 'label': 'Customer N'},
        {'value': 'B', 'label': 'Customer B'},
        {'value': 'G', 'label': 'Customer G'},
        {'value': 'BA', 'label': 'Customer BA'},
        {'value': 'COM', 'label': 'Customer COM'},
        {'value': 'DEFAULT', 'label': 'Customer Default'},
    ]
    return customers

def validate_user_permission(user_data, customer_code):
    """Validate if a user has permission to access a specific customer."""
    if not user_data:
        return True  # No user data provided, assume permission granted
    
    try:
        user = json.loads(user_data)
        # If user is not admin and trying to access a customer other than their assigned one
        if not user.get('isAdmin', False) and user.get('customerCode') != customer_code:
            return False
        return True
    except json.JSONDecodeError:
        return True  # Invalid user data, assume permission granted
