import os
from openai import OpenAI
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or ["https://gd.games"] for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Configure Mistral client
client = OpenAI(
    base_url="https://api.mistral.ai/v1",
    api_key=os.environ.get("MISTRAL_API_KEY"),  # Get your free API key from Mistral
)

class Message(BaseModel):
    content: str

@app.post("/ask")
def ask(message: Message):
    completion = client.chat.completions.create(
        model="mistral-tiny",  # free tier model
        messages=[{"role": "user", "content": message.content}],
    )
    return {"reply": completion.choices[0].message}
