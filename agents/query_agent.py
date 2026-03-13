import os
from dotenv import load_dotenv
from rag.rag_pipeline import create_vector_store

# Load environment variables
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

# Create vector database once
vectorstore = create_vector_store()

# Create retriever
retriever = vectorstore.as_retriever()

def handle_query(query):

    # Retrieve relevant documents
    docs = retriever.invoke(query)

    if not docs:
        return "Sorry, I couldn't find an answer."

    context = docs[0].page_content

    # Simple extraction logic for demo
    if "hackathon" in query.lower():
        if "Hackathon:" in context:
            parts = context.split("Hackathon:")[1].split()
            return parts[0] + " " + parts[1]

    return context