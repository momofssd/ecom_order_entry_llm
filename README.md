# PDF Purchase Order Processing API

This Flask-based API service processes purchase orders in PDF format for multiple customers. It extracts relevant information using LLM (Language Learning Model) processing and returns structured data.

## Features

- PDF text extraction and processing
- Customer-specific information handling
- Automatic quantity unit conversion (LB to KG)
- Date format standardization
- Delivery address matching
- Multi-customer support (C, N, B, G, BA)

## Requirements

- Python 3.8+
- Dependencies listed in `requirements.txt`

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the server:
```bash
python pdf.py
```

The server will run on `http://localhost:5000`

### API Endpoints

#### 1. Process Purchase Order
- **Endpoint**: `/api/process-purchase-order`
- **Method**: POST
- **Content-Type**: multipart/form-data
- **Parameters**:
  - `file`: PDF file (required)
  - `customer`: Customer code (C, N, B, G, or BA)
- **Returns**: JSON with extracted PO information

#### 2. Get Customers List
- **Endpoint**: `/api/customers`
- **Method**: GET
- **Returns**: List of available customers

### Response Format

The API returns JSON containing:
- Purchase Order Number
- Quantity (in KG)
- Required Delivery Date (YYYY-MM-DD)
- Material Number
- Delivery Address
- Customer-specific information

## Error Handling

- Invalid file type
- Missing file
- Processing errors
- Invalid customer selection

## File Structure

- `pdf.py`: Main application file
- `Customer_*.py`: Customer-specific processing modules
- `pdf_processing.py`: PDF text extraction utilities
- `llm_processing.py`: Language model processing functions

## Notes

- Uploaded files are temporarily stored in the 'uploads' directory
- Files are automatically deleted after processing
- Supports PDF files only
- Automatically converts quantities from LB to KG
- Standardizes dates to YYYY-MM-DD format
