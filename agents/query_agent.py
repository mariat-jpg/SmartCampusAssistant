import os
import requests
from dotenv import load_dotenv
from rag.rag_pipeline import create_vector_store
from langchain_core.runnables import RunnablePassthrough

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

vectorstore = create_vector_store()
retriever = vectorstore.as_retriever()

def format_docs(docs):
    return "\n".join(doc.page_content for doc in docs)

def call_llm(context, question):
    prompt = f"""You are a helpful campus assistant. Answer the question using only the context below. Be concise. If the answer is in the context, state it directly. Do not say there is no information if the context contains relevant details. Return ONLY the answer, nothing else.

Context: {context}

Question: {question}

Answer:"""

    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "meta-llama/Llama-3.1-8B-Instruct",
        "provider": "cerebras",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 100,
        "temperature": 0.3,
    }

    response = requests.post(
        "https://router.huggingface.co/v1/chat/completions",
        headers=headers,
        json=payload
    )

    result = response.json()

    try:
        return result["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError):
        return str(result)

def handle_query(query):
    docs = retriever.invoke(query)
    context = format_docs(docs)
    return call_llm(context, query)