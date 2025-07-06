from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
import os

app = FastAPI()

# Allow all frontend origins (Netlify, localhost, etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GROQ_API_KEY = "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"  # your key
GROQ_MODEL = "llama3-8b-8192"

@app.get("/")
def home():
    return {"message": "✅ School Chatbot backend is live!"}

@app.post("/ask")
async def ask_question(request: Request):
    try:
        data = await request.json()
        question = data.get("question", "")

        payload = {
            "model": GROQ_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful school assistant. Answer questions related to admissions, timings, holidays, facilities, events, fees, etc."
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
