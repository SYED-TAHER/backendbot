from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests, os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can replace this with your Netlify domain
    allow_methods=["*"],
    allow_headers=["*"],
)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

@app.get("/")
def root():
    return {"message": "School Chatbot Backend is running."}

@app.post("/ask")
async def ask(request: Request):
    data = await request.json()
    question = data.get("question")

    try:
        res = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "mixtral-8x7b-32768",
                "messages": [
                    {"role": "system", "content": "You are a helpful school chatbot. Answer clearly."},
                    {"role": "user", "content": question}
                ],
                "temperature": 0.5
            }
        )

        result = res.json()
        return {"response": result["choices"][0]["message"]["content"]}

    except Exception as e:
        return {"error": str(e)}
