import fitz
from langchain.text_splitter import RecursiveCharacterTextSplitter

def extract_text_from_pdf(pdf_path, customer=None):
    document = fitz.open(pdf_path)
    text = ""
    total_pages = len(document)
    
    if customer and customer.upper() == "BA":
        # Only keep the first 2 pages for customer BA
        pages_to_extract = min(2, total_pages)
    else:
        # Default behavior: all pages except the last one if more than one
        pages_to_extract = total_pages - 1 if total_pages > 1 else 1

    for page_num in range(pages_to_extract):
        page = document[page_num]
        text += page.get_text()
    
    return text

def split_text(text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=100)
    return splitter.split_text(text)
