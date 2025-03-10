from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain.vectorstores import FAISS

def embed_and_store(chunks):
    embeddings = OllamaEmbeddings(model="llama3.1")
    vectorstore = FAISS.from_texts(chunks, embedding=embeddings)
    return vectorstore

def retrieve_most_relevant_chunk_with_confidence(vectorstore, query, threshold=0.8):
    retrieved_docs_with_scores = vectorstore.similarity_search_with_score(query, k=1)
    high_confidence_docs = [doc for doc, score in retrieved_docs_with_scores if score >= threshold]
    combined_text = "\n".join([doc.page_content for doc in high_confidence_docs])
    return combined_text

def extract_information_with_llm(retrieved_text, extract_prompt):
    llm = OllamaLLM(model="llama3.1", temperature=0)
    prompt = extract_prompt(retrieved_text)
    response = llm.invoke(prompt)
    return response

def refine_extracted_information(extracted_info, refine_prompt):
    llm = OllamaLLM(model="llama3.1", temperature=0)
    prompt = refine_prompt(extracted_info)
    refined_response = llm.invoke(prompt)
    return refined_response.strip()
