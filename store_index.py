from src.helper import load_pdf_file, text_splitter, hugging_face_embeddings
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
from langchain_pinecone import PineconeVectorStore
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Pinecone configuration
INDEX_NAME = "medical-chatbot"
DIMENSION = 768  # Matches your embedding model (e.g., Hugging Face default)
METRIC = "cosine"
CLOUD = "aws"
REGION = "us-east-1"

def initialize_vectorstore():
    """Initialize and return the Pinecone vector store."""
    # Initialize Pinecone client
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

    # Check if index exists, create if not
    existing_indexes = pc.list_indexes().names()
    if INDEX_NAME not in existing_indexes:
        print(f"Creating new index: {INDEX_NAME}")
        pc.create_index(
            name=INDEX_NAME,
            dimension=DIMENSION,
            metric=METRIC,
            spec=ServerlessSpec(cloud=CLOUD, region=REGION)
        )
    else:
        print(f"Index {INDEX_NAME} already exists.")

    # Connect to the index
    index = pc.Index(INDEX_NAME)
    embeddings = hugging_face_embeddings()

    # Check if index has data
    stats = index.describe_index_stats()
    if stats["total_vector_count"] == 0:
        print("Index is empty. Loading PDF, creating chunks, and uploading...")
        extracted_data = load_pdf_file("data/")
        if not extracted_data:
            raise ValueError("No data extracted from PDF files.")
        text_chunks = text_splitter(extracted_data)
        print("Length of text chunks:", len(text_chunks))
        vector_store = PineconeVectorStore.from_documents(
            documents=text_chunks,
            index_name=INDEX_NAME,
            embedding=embeddings
        )
    else:
        print("Index already contains data, just loading vector store...")
        vector_store = PineconeVectorStore(index_name=INDEX_NAME, embedding=embeddings)

    return vector_store

# Export the vector store (initialized once at module load)
try:
    vectorstore_from_docs = initialize_vectorstore()
except Exception as e:
    print(f"Error during initialization: {str(e)}")
    vectorstore_from_docs = None

if __name__ == "__main__":
    # For testing purposes
    if vectorstore_from_docs:
        print("Vector store initialized successfully.")
    else:
        print("Vector store initialization failed.")