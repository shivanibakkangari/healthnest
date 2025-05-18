# app.py (FAISS-based RAG backend)
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA
import os

# ✅ Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
CORS(app)

# ✅ Load FAISS index
print("🔄 Loading FAISS index...")
embedding_model = OpenAIEmbeddings()
vectorstore = FAISS.load_local("faiss_index", embedding_model, allow_dangerous_deserialization=True)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# ✅ Set up LLM and RetrievalQA chain
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "")

    if not question:
        return jsonify({"answer": "Please provide a question."}), 400

    try:
        response = qa_chain.run(question)
        return jsonify({"answer": response})
    except Exception as e:
        return jsonify({"answer": "Something went wrong.", "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)