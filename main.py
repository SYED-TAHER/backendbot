from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
import os

app = FastAPI()

# CORS setup: allows access from frontend (Netlify, localhost, etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ✅ Load school info from local JSON file
try:
    with open("school_info.json", "r", encoding="utf-8") as f:
        school_data = json.load(f)
except Exception as e:
    print("❌ Error loading school_info.json:", e)
    school_data = []

# ✅ Create a structured knowledge base prompt
knowledge_base = "\n".join(
    [f"Q: {item['question']}\nA: {item['answer']}" for item in school_data]
)





# 🔐 Get API Key from Render environment variable
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama3-8b-8192"

@app.get("/")
def home():
    return {"message": "✅ School Chatbot backend is live on Render!"}

@app.post("/ask")
async def ask_question(request: Request):
    try:
        data = await request.json()
        question = data.get("question", "")

        payload = {
            "model": GROQ_MODEL,
           "messages" = [
            {
                "role": "system",
                "content": (
                    "You are Skoolie 🤖, a helpful and friendly school assistant chatbot. "
                    "Only answer questions using the school information provided below. "
                    "If you don't know the answer, politely say: 'Sorry, I can only answer school-related queries.'\n\n"
                    f"{knowledge_base}"
                )
            },
            {
                "role": "user",
                "content": question
            }
        ]
        }

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json=payload
        )

        response.raise_for_status()
        data = response.json()
        return {"answer": data['choices'][0]['message']['content'].strip()}

    except Exception as e:
        return {"error": str(e)}
