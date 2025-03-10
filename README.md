# E-Commerce Web Application with PDF Processing

This repository contains a comprehensive solution for e-commerce operations with a focus on purchase order processing, featuring three main components:

1. A React-based web frontend
2. A Flask-based PDF processing API
3. A Streamlit-based testing application

## Default Configuration

**Note:** The default configuration utilizes OpenAI via API calls for the most accurate extraction results. This can be selected by choosing "DEFAULT" in the customer dropdown of the web application.

---

## Section 1: E-Commerce Web Application

A modern React-based web application for managing purchase orders, order tracking, and e-commerce operations with separate interfaces for administrators and regular users.

### 📸 Screenshots

#### Login Page
![image](https://github.com/user-attachments/assets/e544118b-42b8-4d09-94a5-259e4e9139c6)


#### Admin Dashboard
![image](https://github.com/user-attachments/assets/628d83f4-15a9-4372-a52a-860f3442ef90)


#### Admin Purchase Order Upload
![image](https://github.com/user-attachments/assets/ceb87eec-96b5-47da-9d22-27a56d14514e)


####  Admin Purchase Order Upload Process
![image](https://github.com/user-attachments/assets/d942b41a-ff8d-43bf-ad7c-f8b0dfc7f89d)

####  Non-Admin Order Upload
![image](https://github.com/user-attachments/assets/632afb73-7f80-485e-bf38-7e4c95b48010)


### 🚀 Features

#### User Authentication
- Secure login system with role-based access control
- Separate interfaces for administrators and regular users
- Session management for persistent login

#### Admin Features
- **Dashboard**: Overview of system activity and key metrics
- **Purchase Order Processing**: Upload, view, and process purchase orders
  - PDF file upload with multi-file support
  - Automatic extraction of order details
  - Manual editing capabilities for extracted data
  - Customer-specific processing rules
- **Order Entry**: Create and manage orders directly in the system
- **Order Tracking**: Monitor status of all orders in the system

#### User Features
- **Purchase Order Upload**: Submit purchase orders for processing
- **Order History**: View past and current orders
- **Order Status Tracking**: Monitor the progress of submitted orders

#### PDF Processing Integration
- Seamless integration with backend PDF processing API
- Support for various purchase order formats
- Real-time feedback on processing status

### 🛠️ Technology Stack

#### Frontend
- **React 19**: Latest version of the React library for building user interfaces
- **React Router 7**: For application routing and navigation
- **React Bootstrap**: UI component library based on Bootstrap
- **Axios**: HTTP client for API requests
- **XLSX**: For Excel file processing
- **React DnD**: For drag-and-drop functionality
- **Framer Motion**: For smooth animations and transitions

#### Backend Integration
- RESTful API integration with Flask backend
- PDF processing capabilities
- Customer data management

### 🏗️ Project Structure

```
ecom_web/
├── public/             # Static files
├── src/                # Source code
│   ├── apipost/        # API integration utilities
│   ├── components/     # Reusable UI components
│   │   ├── AlertMessage.js
│   │   ├── Footer.js
│   │   ├── Header.js
│   │   └── Product.js
│   ├── data/           # Static data and mock data
│   ├── pages/          # Application pages
│   │   ├── LoginPage.js
│   │   ├── MainExternal.js
│   │   ├── MainInternal.js
│   │   ├── adminview/  # Admin-specific pages
│   │   │   ├── AdminDashboard.js
│   │   │   ├── OrderEntryAdmin.js
│   │   │   ├── OrderRecords.js
│   │   │   └── POuploadAdmin.js
│   │   └── userview/   # User-specific pages
│   │       ├── HomePage.js
│   │       ├── OrderRecords.js
│   │       └── POupload.js
│   ├── App.js          # Main application component
│   ├── index.js        # Application entry point
│   └── users.js        # User management utilities
└── package.json        # Project dependencies and scripts
```

### 📋 Application Flow

1. **Authentication**: Users log in through the LoginPage component
2. **Role-Based Routing**: 
   - Administrators are directed to the admin interface
   - Regular users are directed to the user interface
3. **Purchase Order Processing**:
   - User uploads PDF purchase orders
   - System processes the PDFs and extracts relevant information
   - User reviews and can edit the extracted information
   - User submits the processed information to the system
4. **Order Tracking**:
   - Users can view the status of their orders
   - Administrators can view and manage all orders in the system

### 🔄 Purchase Order Processing Workflow

#### Admin Workflow
1. Select customer from dropdown
2. View customer-specific shipping information
3. Upload one or more PDF purchase orders
4. System processes the PDFs and extracts order details
5. Review extracted information in a tabular format
6. Edit information if necessary
7. View original PDF for verification
8. Submit processed orders to the system

#### User Workflow
1. Upload purchase order PDF(s)
2. System processes the PDFs
3. Review extracted information
4. Submit order for processing

### 📸 Key UI Components

#### Header Component
[Add screenshot of header component here]

The Header component provides navigation and user information across the application.

#### Purchase Order Upload
[Add screenshot of PO upload component here]

The PO upload component allows users to upload and process purchase order PDFs.

#### Order Records Table
[Add screenshot of order records table here]

The Order Records component displays order information in a sortable, filterable table.

### 🚀 Getting Started

#### Prerequisites
- Node.js 16.x or higher
- npm 8.x or higher

#### Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd ecom_web
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Start the development server:
   ```
   npm start
   ```

4. Open your browser and navigate to:
   ```
   http://localhost:3000
   ```

#### Building for Production

```
npm run build
```

This creates an optimized production build in the `build` folder.

### 🔌 Backend Integration

This frontend application integrates with a Flask backend API for PDF processing and data management. The backend provides the following endpoints:

- `/api/process-purchase-order`: Processes uploaded PDF purchase orders
- `/api/customers`: Retrieves the list of available customers
- `/api/customer-ship-to/:customer`: Retrieves shipping information for a specific customer

### 🧩 Extending the Application

#### Adding New Features
1. Create new components in the appropriate directories
2. Update routing in App.js
3. Integrate with backend API as needed

#### Adding New Customer Types
The system supports customer-specific processing rules. To add a new customer:

1. Update the backend API to support the new customer
2. The frontend will automatically include the new customer in the dropdown

### 📝 Development Notes

#### State Management
- Component-level state using React hooks
- Props for component communication
- Context API for global state (authentication, etc.)

#### API Integration
- Axios for HTTP requests
- Error handling with try/catch blocks
- Loading states for better user experience

#### Responsive Design
- Bootstrap Grid System
- Media queries for custom responsive behavior
- Mobile-first approach

### 🔒 Security Considerations

- Authentication token management
- Role-based access control
- Input validation
- Secure API communication

### 🔮 Future Enhancements

- Enhanced data visualization
- Batch processing improvements
- Integration with additional backend services
- Advanced search and filtering capabilities
- Export functionality for reports

---

## Section 2: PDF Purchase Order Processing API

A Flask-based API for extracting and processing purchase order information from PDF documents. This application uses Large Language Models (LLMs) and vector embeddings to intelligently extract key information from purchase order PDFs and return structured data.

### How It Works: LLM-Powered Extraction

This system leverages advanced LLM capabilities to extract relevant information from purchase order documents through a sophisticated multi-step process:

#### 1. Text Extraction and Chunking

```python
# Extract text from PDF
raw_text = extract_text_from_pdf(filepath, customer)
# Split into manageable chunks
text_chunks = split_text(raw_text)
```

- The system first extracts raw text from PDF documents using PyMuPDF (fitz)
- Customer-specific logic determines which pages to process (e.g., Customer BA only processes the first 2 pages)
- The extracted text is split into manageable chunks using RecursiveCharacterTextSplitter

#### 2. Vector Embedding and Semantic Search

```python
# Create vector embeddings
vectorstore = embed_and_store(text_chunks)
# Find relevant text through semantic search
query = "Purchase Order Number, Quantity in kg, Required Delivery Date, Material Number, deliver to"
relevant_text = retrieve_most_relevant_chunk_with_confidence(vectorstore, query, threshold=0.8)
```

- Text chunks are converted into numerical vector representations (embeddings) using Llama 3.1
- These embeddings capture the semantic meaning of the text
- A similarity search finds the most relevant text chunks based on a specific query
- Only chunks with a similarity score above the confidence threshold (0.8) are used

#### 3. Initial Information Extraction

```python
# Extract initial information using customer-specific prompts
initial_extracted_info = extract_information_with_llm(relevant_text, extract_prompt)
```

- The Llama 3.1 model processes the relevant text using customer-specific extraction prompts
- Each customer module defines custom prompts tailored to their purchase order format
- The extraction prompt guides the model to identify specific fields like PO number, quantities, dates, etc.

#### 4. Information Refinement

```python
# Refine the extracted information
refined_info = refine_extracted_information(initial_extracted_info, refine_prompt)
refined_info_dict = json.loads(refined_info)
```

- The initially extracted information undergoes refinement using customer-specific refinement prompts
- This step standardizes formats, corrects errors, and ensures consistency
- The refined information is converted to a structured JSON format

#### 5. Post-Processing

```python
# Apply post-processing
modify_quantity_and_unit(refined_info_dict)  # Fix Quantity & Unit
modify_delivery_date_format(refined_info_dict)  # Fix Date Format
refined_info_dict.update(module.sold_to_info)  # Add sold-to info
```

- Quantity values are standardized and converted to KG if necessary
- Dates are formatted to YYYY-MM-DD
- Customer-specific sold-to information is added
- Delivery addresses are matched to standardized shipping codes

### Processing Workflow

1. **PDF Upload**: The PDF file is uploaded and temporarily stored
2. **Customer Selection**: The appropriate customer module is selected based on the customer code
3. **Text Extraction**: Raw text is extracted from the PDF using PyMuPDF
4. **Text Chunking**: The text is split into manageable chunks
5. **Embedding**: Text chunks are embedded using Llama 3.1 and stored in a FAISS vector database
6. **Relevant Text Retrieval**: The most relevant text chunks are retrieved based on semantic search
7. **Initial Information Extraction**: LLM extracts initial information using customer-specific prompts
8. **Refinement**: The extracted information is refined using customer-specific prompts
9. **Post-processing**: 
   - Quantity and unit formatting
   - Date format standardization
   - Adding sold-to information
   - Processing deliver-to addresses
10. **Response**: The structured information is returned as JSON

### Dependency Files

| File | Description |
|------|-------------|
| **pdf.py** | Main Flask application that handles HTTP requests, routes, and orchestrates the PDF processing workflow |
| **pdf_processing.py** | Contains utilities for extracting and processing text from PDF files |
| **llm_processing.py** | Provides functions for language model processing, including embedding, retrieval, and information extraction |
| **utils.py** | Utility functions for post-processing extracted information |
| **customer_handler.py** | Manages customer-specific modules and user permissions |
| **Customer_X.py** (multiple files) | Customer-specific configuration and processing logic |
| **po_processor.py** | Orchestrates the purchase order processing workflow |

### Customer Modules

Each customer module (e.g., Customer_G.py, Customer_C.py) contains:
- `extract_prompt`: Initial extraction prompt tailored to the customer's PO format
- `refine_prompt`: Refinement prompt for standardizing extracted information
- `sold_to_info`: Dictionary with customer-specific sold-to information
- `ship_to_info`: Dictionary mapping delivery addresses to standardized codes

### Prerequisites

- Python 3.7+
- Flask
- Flask-CORS
- PyMuPDF (fitz)
- LangChain
- FAISS-CPU
- Ollama (for local LLM inference)

### Installation

#### Option 1: Using pip

1. Clone the repository:
   ```
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

#### Option 2: Using Conda

1. Clone the repository:
   ```
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Create and activate the Conda environment:
   ```
   conda env create -f environment.yml
   conda activate pdf-processor
   ```

#### Common Setup Steps

1. Ensure Ollama is installed and the Llama 3.1 model is available:
   ```
   ollama pull llama3.1
   ```

2. Create necessary directories:
   ```
   mkdir -p uploads uploaded_pdfs
   ```

### Usage

#### Starting the Server

Run the application:

```
python pdf.py
```

The server will start on http://localhost:5000 by default.

### API Endpoints

#### 1. Process Purchase Order

**Endpoint:** `/api/process-purchase-order`  
**Method:** POST  
**Content-Type:** multipart/form-data

**Parameters:**
- `file`: PDF file to process (required)
- `customer`: Customer code (e.g., 'BA', 'C', 'N', 'B', 'G')

**Response:**
```json
{
  "Purchase Order Number": "PO123456",
  "Quantity": "1000",
  "Unit": "KG",
  "Required Delivery Date": "2025-03-15",
  "Material Number": "MAT001",
  "Deliver to": "MAGA1",
  "sold_to_num": "gsp_123"
}
```

#### 2. Get Customers List

**Endpoint:** `/api/customers`  
**Method:** GET

**Response:**
```json
[
  {"value": "C", "label": "Customer C"},
  {"value": "N", "label": "Customer N"},
  {"value": "B", "label": "Customer B"},
  {"value": "G", "label": "Customer G"},
  {"value": "BA", "label": "Customer BA"}
]
```

### Error Handling

The API includes error handling for:
- Missing files: `{'error': 'No file provided'}`
- Empty filenames: `{'error': 'No file selected'}`
- Invalid file types: `{'error': 'Invalid file type'}`
- Invalid customer selections: `{'error': 'Invalid customer selection'}`
- Processing errors: `{'error': 'Error message'}`

### Extending for New Customers

To add support for a new customer:

1. Create a new customer module (e.g., `Customer_NEW.py`) with:
   - `extract_prompt`: Prompt for initial information extraction
   - `refine_prompt`: Prompt for refining extracted information
   - `sold_to_info`: Dictionary with sold-to information
   - `ship_to_info`: Dictionary mapping delivery addresses

2. Import the new module in `pdf.py` and `customer_handler.py`

3. Add the new customer to the `customer_modules` dictionary in the `process_purchase_order` function

4. Add the new customer to the list returned by the `/api/customers` endpoint

---

## Section 3: Streamlit PDF Purchase Order Extractor (app.py)

A Streamlit-based web application for testing purchase order extraction using OpenAI's GPT-4o model. This application provides a simple, user-friendly interface for extracting and processing purchase order information from PDF documents.

### Overview

This project consists of two main components:

1. **openAI_extraction.py**: A backend script that handles PDF text extraction and OpenAI API integration
2. **app.py**: A Streamlit frontend application that provides a user-friendly interface for the extraction process

### How It Works: OpenAI-Powered Extraction

This system leverages OpenAI's GPT-4o model to extract relevant information from purchase order documents through a streamlined process:

#### 1. Text Extraction

```python
def extract_text_from_pdf(pdf_file):
    text = ""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
    return text
```

- The system extracts raw text from PDF documents using PyPDF2
- All pages of the PDF are processed and combined into a single text string

#### 2. Text Preprocessing

```python
def fix_number_format(text):
    text = re.sub(r'(\d{1,3}),(\d{3}\.\d+)', r'\1\2', text)  # Convert "41,976.050" → "41976.050"
    return text
```

- The extracted text undergoes preprocessing to fix common formatting issues
- Number formats are standardized to ensure accurate extraction

#### 3. OpenAI API Integration

```python
response = client.chat.completions.create(
    model="gpt-4o",
    messages=prompts,
    temperature=0,
    top_p=0.1
)
```

- The preprocessed text is sent to OpenAI's GPT-4o model
- A carefully crafted system prompt guides the model to extract specific fields
- Temperature is set to 0 for deterministic outputs
- Low top_p value (0.1) ensures high-precision responses

#### 4. Information Extraction

The system prompt instructs the model to extract:
- Customer Name (from the 'SHIP TO' section)
- Purchase Order Number
- Required Delivery Date (converted to ISO format)
- Material Number
- Order Quantity in kg (standardized format)
- Delivery Address (only the 'SHIP TO' address)

#### 5. JSON Parsing and Validation

```python
try:
    extract_contents_json = json.loads(extract_contents)
except json.JSONDecodeError:
    st.error("⚠ OpenAI returned invalid JSON")
```

- The model's response is parsed as JSON
- Validation ensures the extracted information is properly structured
- Error handling manages cases where the model doesn't return valid JSON

### Streamlit Frontend (app.py)

The Streamlit application provides a user-friendly interface with the following features:

#### 1. API Key Management

- Secure input for OpenAI API key
- Validation to ensure the API key is valid
- Session state management to maintain the key during the session

#### 2. File Upload

- Support for multiple PDF uploads
- File validation to ensure only PDFs are processed
- Session state management to track uploaded files

#### 3. Processing Controls

- Process button to trigger extraction
- Reset button to clear uploaded files and results
- Visual feedback during processing

#### 4. Results Display

- Structured display of extracted information
- JSON formatting for clear presentation
- Error handling for invalid responses

### Differences from Backend-Only Approach

While openAI_extraction.py provides the core functionality, app.py enhances it with:

1. **Interactive UI**: User-friendly interface for uploading files and viewing results
2. **Multiple File Processing**: Support for batch processing multiple PDFs
3. **Real-time Feedback**: Visual indicators of processing status and results
4. **Error Handling**: Improved error messages and recovery options
5. **Session Management**: Persistence of uploads and results during the session

### Prerequisites

- Python 3.7+
- Streamlit
- PyPDF2
- OpenAI Python SDK
- python-dotenv (for openAI_extraction.py)
- Valid OpenAI API key with access to GPT-4o

### Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. For openAI_extraction.py, create a .env file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

### Usage

#### Running the Streamlit App

```
streamlit run app.py
```

The application will open in your default web browser, typically at http://localhost:8501.

#### Using the Application

1. Enter your OpenAI API key in the sidebar
2. Click "Validate API Key" to verify the key
3. Upload one or more PDF purchase orders
4. Click "Process Files" to extract information
5. View the structured results for each file
6. Use "Reset Files" to clear and start over

### System Prompt Details

The system uses a carefully crafted prompt to guide the OpenAI model:

```
You are an AI extracting relevant content from a purchase order.
Find the following details and return ONLY a valid JSON object with these fields:
- Customer Name (Extract from the 'SHIP TO' section only)
- Purchase Order Number
- Required Delivery Date (convert to ISO format YYYY-MM-DD)
- Material Number (Extract from the line item section)
- Order Quantity in kg (only the converted kg value)
- Delivery Address (extract ONLY the 'SHIP TO' address)

IMPORTANT:
- Return ONLY a valid JSON object
- Ensure 'Order Quantity in kg' is a clean number
- Ensure 'Required Delivery Date' follows ISO 8601 format
- Ensure 'Delivery Address' is the correct 'SHIP TO' address
- Ignore addresses related to 'Vendor', 'Invoice', 'Billing', etc.
```

This prompt ensures the model focuses on extracting the specific information needed in the correct format.

### Extending the Application

To enhance the application:

1. **Add Authentication**: Implement user authentication for secure access
2. **Database Integration**: Store extracted information in a database
3. **Custom Extraction Rules**: Add support for different purchase order formats
4. **Export Options**: Add functionality to export results as CSV, Excel, etc.
5. **Batch Processing Improvements**: Add progress tracking for large batches
