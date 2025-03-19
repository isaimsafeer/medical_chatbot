from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
import os

# loading pdf file
def load_pdf_file(directory):
    documents = []
    # Loop through all files in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):  # Check if the file is a PDF
            file_path = os.path.join(directory, filename)
            loader = PyPDFLoader(file_path)
            documents.extend(loader.load())  # Add the loaded documents to the list
    return documents


def text_splitter(extracted_data):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)  # 'overlap' should be 'chunk_overlap'
    text_chunks = text_splitter.split_documents(extracted_data)
    return text_chunks



def hugging_face_embeddings():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    return embeddings

