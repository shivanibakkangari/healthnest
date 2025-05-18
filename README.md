# 🌿 Health Nest — Your AI-Powered Healthcare Assistant

Health Nest is a full-stack AI-powered healthcare companion designed to provide instant, intelligent, and accessible medical assistance. It offers a conversational chatbot powered by GPT-3.5, Retrieval-Augmented Generation (RAG) using LangChain + FAISS, and real-time provider lookup using Google Maps API.

---

## Features

* **Login Page** — Secure login with mock credentials
* **Landing Hero Section** — Big, bold tagline with call/chat/email info
* **💬 AI Chat Assistant** — Conversational agent for symptoms, medications, and more
* **📍 Provider Lookup** — Finds doctors and clinics near you based on illness
* **RAG with FAISS** — Intelligent answers from real medical PDFs
* ** Symptom Extraction** — Uses spaCy + fuzzy match to detect illness
* **Smart Fallbacks** — Handles vague inputs and avoids “I don’t know” responses
* **Responsive UI** — Tailwind CSS layout with mobile support
* **Typing Animations** — Pulse effect for realistic feel
* **Floating Chat Button** — One-click AI access from any page

---

## 🧱 Built With

### 💻 Frontend:

* React
* Tailwind CSS
* Framer Motion
* Vite

### 🔙 Backend:

* Flask
* LangChain (RetrievalQA)
* OpenAI GPT-3.5 Turbo
* FAISS (Vector Search)
* Pandas
* dotenv
* spaCy

### 🌐 APIs:

* Google Maps Places API

### ☁️ Hosting:

* Frontend: Vite (Local)
* Backend: Flask (via Ngrok)

---

## 🧠 AI & RAG Pipeline

1. User submits a query via chat
2. Flask `/ask` route runs LangChain RetrievalQA with FAISS
3. Relevant content is retrieved from medical PDFs (embedded)
4. GPT-3.5 generates the final answer
5. Smart fallback logic avoids dead ends

---

## 🔍 Doctor Finder Flow

1. User says: “I want to consult a doctor” or “chest pain”
2. `/providers` endpoint extracts illness using spaCy & fuzzy match
3. Matches it to a specialist (e.g., cardiologist)
4. Google Maps API returns top 5 clinics in the ZIP code
5. Chat UI displays results with names, ratings, and addresses

---

## 📁 Project Structure

```
healthnest/
├── backend/
│   ├── app.py
│   ├── upload_to_faiss.py
│   ├── requirements.txt
├── data/
│   ├── final.csv
├── tailwind-test/ (Frontend)
│   ├── public/
│   ├── src/
│   ├── package.json
│   ├── vite.config.js
├── .gitignore
├── README.md
```

---

## 🔧 Setup Instructions

### Backend

```bash
cd backend
python -m spacy download en_core_web_sm
pip install -r requirements.txt
python app.py
```

### Ngrok (for public link)

```bash
ngrok http 5050
```

### Frontend

```bash
cd tailwind-test
npm install
npm run dev
```

Update `App.jsx`:

```js
const BASE_URL = 'https://your-ngrok-url.ngrok-free.app';
```

---

## ⚠️ Environment Variables

Set the following in `.env` or Render Dashboard:

```env
OPENAI_API_KEY=your-openai-api-key
GOOGLE_MAPS_API_KEY=your-maps-api-key
```

---

## 🧪 Sample Questions to Try

* What are the symptoms of diabetes?
* Can I take ibuprofen and paracetamol together?
* I feel dizzy and tired
* I want to consult a dermatologist near 95126
* I have a rash and fever

---

## 📸 Screenshots

> ![image](https://github.com/user-attachments/assets/4e671074-5ede-4d25-8903-c3d203564226)
> ![image](https://github.com/user-attachments/assets/9ecc84f0-84d8-492f-9051-c885d1fcba18)
> ![image](https://github.com/user-attachments/assets/66f80ff3-943c-4b9b-bd75-ad16a75ef082)
> ![image](https://github.com/user-attachments/assets/dfbe34f7-3fb5-4462-9c6c-d3173622520d)
> ![image](https://github.com/user-attachments/assets/79ee7d23-de81-435c-80b4-c6b169392b12)
> ![image](https://github.com/user-attachments/assets/973d3ac5-2406-4d56-a965-e32eaa66afee)
> ![image](https://github.com/user-attachments/assets/3865e73a-6305-4b1a-976a-cf8d233edc31)









---

## ✅ Future Improvements

* Save past chat context
* User authentication
* Add support for voice input

---

##  Acknowledgments

* OpenAI for GPT-3.5
* LangChain & FAISS
* spaCy
* Google Maps API
* Agentic RAG-a-thon team

---

## 📩 Contact

**GitHub:** [github.com/shivanibakkangari/healthnest](https://github.com/shivanibakkangari/healthnest)

---

Thank you for using Health Nest 💚

give script to paste to create read me file the above mentioned
