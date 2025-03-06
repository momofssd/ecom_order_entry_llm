# PDF Purchase Order Processing API

A Flask-based API for extracting and processing purchase order information from PDF documents. This application uses natural language processing and machine learning techniques to automatically extract key information from purchase order PDFs and return structured data.

## Features

- PDF document upload and processing
- Customer-specific extraction logic
- Text extraction from PDFs
- LLM-based information extraction with confidence scoring
- Data refinement and formatting
- RESTful API endpoints
- Cross-Origin Resource Sharing (CORS) support



### Module Descriptions

- **pdf.py**: Main Flask application that handles HTTP requests, routes, and orchestrates the PDF processing workflow
- **pdf_processing.py**: Contains utilities for extracting and processing text from PDF files
  - `extract_text_from_pdf`: Extracts raw text from PDF documents
  - `split_text`: Divides extracted text into manageable chunks
- **llm_processing.py**: Provides functions for language model processing
  - `embed_and_store`: Converts text chunks into embeddings and stores them
  - `retrieve_most_relevant_chunk_with_confidence`: Finds the most relevant text based on a query
  - `extract_information_with_llm`: Uses LLM to extract structured information
  - `refine_extracted_information`: Refines the extracted information using prompts
- **Customer Modules**: Customer-specific configuration and processing logic
  - Each customer module contains:
    - `extract_prompt`: Initial extraction prompt
    - `refine_prompt`: Refinement prompt
    - `sold_to_info`: Customer sold-to information
    - `ship_to_info`: Customer shipping location mappings

## Prerequisites

- Python 3.7+
- Flask
- Flask-CORS
- Werkzeug
- Various NLP/ML libraries (for embedding and LLM processing)
- Customer-specific processing modules

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Ensure all customer modules are available in the project directory:
   - Customer_G.py
   - Customer_C.py
   - Customer_N.py
   - Customer_B.py
   - Customer_BA.py
   - Customer_COM.py

## Usage

### Starting the Server

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
- `customer`: Customer code (e.g., 'BA', 'C', 'N', 'B', 'G', 'COM')

**Response:**
```json
{
  "Purchase Order Number": "PO123456",
  "Quantity": "1000",
  "Unit": "KG",
  "Required Delivery Date": "2025-03-15",
  "Material Number": "MAT001",
  "Deliver to": "Warehouse A"
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
  {"value": "BA", "label": "Customer BA"},
  {"value": "COM", "label": "Customer COM"}
]
```

## Processing Flow

1. **PDF Upload**: The PDF file is uploaded and temporarily stored
2. **Text Extraction**: Raw text is extracted from the PDF
3. **Text Chunking**: The text is split into manageable chunks
4. **Embedding**: Text chunks are embedded and stored in a vector database
5. **Relevant Text Retrieval**: The most relevant text chunks are retrieved based on the query
6. **Initial Information Extraction**: LLM extracts initial information from relevant text
7. **Refinement**: The extracted information is refined using customer-specific prompts
8. **Post-processing**: 
   - Quantity and unit formatting
   - Date format standardization
   - Adding sold-to information
   - Processing deliver-to addresses
9. **Response**: The structured information is returned as JSON

## LLM Processing Details

The application leverages Large Language Models (LLMs) and vector embeddings to intelligently extract information from purchase order documents. Here's a detailed explanation of how the LLM processing works:

### Technology Stack

- **Model**: Llama 3.1 (via Ollama)
- **Vector Database**: FAISS (Facebook AI Similarity Search)
- **Framework**: LangChain for orchestrating the LLM workflow

### Embedding and Storage

```python
def embed_and_store(chunks):
    embeddings = OllamaEmbeddings(model="llama3.1")
    vectorstore = FAISS.from_texts(chunks, embedding=embeddings)
    return vectorstore
```

1. Text chunks from the PDF are converted into numerical vector representations (embeddings) using the Llama 3.1 model
2. These embeddings capture the semantic meaning of the text
3. The embeddings are stored in a FAISS vector database, which enables efficient similarity searches

### Relevant Text Retrieval

```python
def retrieve_most_relevant_chunk_with_confidence(vectorstore, query, threshold=0.8):
    retrieved_docs_with_scores = vectorstore.similarity_search_with_score(query, k=5)
    high_confidence_docs = [doc for doc, score in retrieved_docs_with_scores if score >= threshold]
    combined_text = "\n".join([doc.page_content for doc in high_confidence_docs])
    return combined_text
```

1. The system performs a similarity search against the vector database to find the most relevant text chunks
2. It retrieves the top 5 most similar chunks along with their similarity scores
3. Only chunks with a similarity score above the confidence threshold (default: 0.8) are kept
4. The high-confidence chunks are combined into a single text block for processing

### Information Extraction

```python
def extract_information_with_llm(retrieved_text, extract_prompt):
    llm = OllamaLLM(model="llama3.1", temperature=0)
    prompt = extract_prompt(retrieved_text)
    response = llm.invoke(prompt)
    return response
```

1. The Llama 3.1 model is initialized with temperature=0 for deterministic outputs
2. The customer-specific extraction prompt is applied to the retrieved text
3. The LLM processes the text and extracts the relevant purchase order information
4. The extraction prompt guides the model to identify specific fields like PO number, quantities, dates, etc.

### Information Refinement

```python
def refine_extracted_information(extracted_info, refine_prompt):
    llm = OllamaLLM(model="llama3.1", temperature=0)
    prompt = refine_prompt(extracted_info)
    refined_response = llm.invoke(prompt)
    return refined_response.strip()
```

1. The initially extracted information is passed through a refinement step
2. A customer-specific refinement prompt is used to improve the extraction results
3. This step helps standardize formats, correct errors, and ensure consistency
4. The refined information is then returned for further processing

### Confidence Scoring

The system incorporates confidence scoring to ensure reliable information extraction:

1. Vector similarity scores determine which text chunks are most relevant to the query
2. Only chunks above the confidence threshold are used for information extraction
3. This approach helps filter out irrelevant sections of the document
4. The threshold can be adjusted based on the desired balance between precision and recall

## Extending for New Customers

To add support for a new customer:

1. Create a new customer module (e.g., `Customer_NEW.py`) with:
   - `extract_prompt`: Prompt for initial information extraction
   - `refine_prompt`: Prompt for refining extracted information
   - `sold_to_info`: Dictionary with sold-to information
   - `ship_to_info`: Dictionary mapping delivery addresses

2. Import the new module in `pdf.py`

3. Add the new customer to the `customer_modules` dictionary in the `process_purchase_order` function

4. Add the new customer to the list returned by the `/api/customers` endpoint

## Error Handling

The API includes error handling for:
- Missing files
- Invalid file types
- Processing errors
- Invalid customer selections


