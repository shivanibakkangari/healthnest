# app.py (with strong fallback to avoid 'I don't know')
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA
import os
import spacy
import requests
import difflib
import random

# ✅ Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

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

# ✅ Illness lookup setup
nlp = spacy.load("en_core_web_sm")

illness_to_specialist = {
    "diabetes": "Diabetologist",
    "heart attack": "Cardiologist",
    "chest pain": "Cardiologist",
    "fever": "General Physician",
    "cold": "General Physician",
    "cough": "Pulmonologist",
    "headache": "Neurologist",
    "rash": "Dermatologist",
    "skin allergy": "Dermatologist",
    "eye pain": "Ophthalmologist",
    "anxiety": "Psychiatrist",
    "depression": "Psychiatrist",
    "itchy skin": "Dermatologist",
    "toothache": "Dentist",
    "joint pain": "Orthopedic",
    "vision problems": "Ophthalmologist",
    "urine infection": "Urologist",
    "pregnancy": "Gynecologist"
}

def extract_illness(text):
    matches = difflib.get_close_matches(text.lower(), illness_to_specialist.keys(), n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_specialist(illness):
    return illness_to_specialist.get(illness)

def find_doctors_nearby(pincode, specialization, api_key):
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    query = f"{specialization} near {pincode}"
    params = {"query": query, "key": api_key}
    response = requests.get(url, params=params)
    results = response.json().get("results", [])
    return [
        {
            "name": r["name"],
            "address": r["formatted_address"],
            "rating": r.get("rating", "N/A")
        }
        for r in results[:5]
    ] if results else [{"name": "No clinics found", "address": "", "rating": "N/A"}]

# ✅ Chat endpoint with stronger fallback
@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "")

    if not question:
        return jsonify({"answer": "Please provide a question."}), 400

    try:
        response = qa_chain.run(question)
        fallback_phrases = ["i don't know", "i dont know", "not sure", "unknown", "i am not sure"]
        if (
            not response or
            any(f in response.lower() for f in fallback_phrases) or
            len(question.strip().split()) < 3
        ):
            response = random.choice([
                "I'm here to help — could you describe your symptoms in a bit more detail?",
                "I'm not sure I understood that. Can you rephrase or add more context?",
                "To help you better, I need a little more information about how you're feeling.",
                "Could you clarify your concern so I can assist more accurately?"
            ])
        return jsonify({"answer": response})
    except Exception as e:
        return jsonify({"answer": "Something went wrong.", "error": str(e)}), 500

# ✅ Provider lookup endpoint
@app.route("/providers", methods=["POST"])
def providers():
    data = request.get_json()
    message = data.get("message", "")
    pincode = data.get("pincode", "")

    illness = extract_illness(message)
    specialist = get_specialist(illness) if illness else "General Physician"

    results = find_doctors_nearby(pincode, specialist, GOOGLE_MAPS_API_KEY)

    provider_lines = []
    for i, p in enumerate(results, 1):
        line = (
            f"{i}. 🏥 {p['name']}\n"
            f"   📍 {p['address']}\n"
            f"   ⭐ {p['rating']} stars"
        )
        provider_lines.append(line)

    providerText = f"📍 Found {len(results)} clinics for {specialist}:\n\n" + "\n\n".join(provider_lines)

    return jsonify({
        "illness": illness or "general",
        "specialist": specialist,
        "answer": providerText
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
