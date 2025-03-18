from src.helper import load_pdf_file, text_splitter, hugging_face_embeddings
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
from langchain_pinecone import PineconeVectorStore
import os
from dotenv import load_dotenv

load_dotenv()

# loading the data
extracted_data = load_pdf_file("data/")

# Splitting into chunks
text_chunks = text_splitter(extracted_data)
print("length of text chunks:", len(text_chunks))

# Creating embeddings
embeddings = hugging_face_embeddings()

# Creating Pinecone index
index_name = "medical-chatbot"


pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
pc.create_index(
    name=index_name,
    dimension=768,
    metric="cosine",
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1"
    )
)


index_name = "medical-chatbot"

index = pc.Index(index_name)

# Correctly initialize PineconeVectorStore
vector_store = PineconeVectorStore(index_name=index_name, embedding=embeddings)

vector_store.add_documents(documents=text_chunks)