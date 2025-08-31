import os
from openai import OpenAI
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 👈 or restrict to ["https://gd.games"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app = FastAPI()

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ.get("HF_TOKEN"),
)

class Message(BaseModel):
    content: str

@app.post("/ask")
def ask(message: Message):
    completion = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-V3:together",
        messages=[
            {"role": "user", "content": message.content}
        ],
    )
    return {"reply": completion.choices[0].message}
