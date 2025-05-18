# upload_to_faiss.py
import os
import pandas as pd
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.docstore.document import Document

# Load API keys from .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Load dataset
df = pd.read_csv("final.csv")

# Format as LangChain Documents
docs = [
    Document(
        page_content=f"Q: {row['question']}\nContext: {row['context']}\nA: {row['answer']}",
        metadata={"source": row.get("source", "manual")}
    )
    for _, row in df.iterrows()
]

# Embed using OpenAI
print("🔄 Generating embeddings and building FAISS index...")
embedding_model = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(docs, embedding_model)

# Save index locally
faiss_path = "faiss_index"
vectorstore.save_local(faiss_path)

print(f"✅ FAISS index saved at: {faiss_path}/")
