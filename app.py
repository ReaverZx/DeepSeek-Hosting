import os
from openai import OpenAI
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ Enable CORS for all origins (or restrict to gd.games)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or ["https://gd.games"] to be more secure
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(
    base_url="https://glama.ai/api/gateway/openai/v1",
    api_key=os.environ.get("GLAMA_API_KEY"),
)

class Message(BaseModel):
    content: str

@app.post("/ask")
def ask(message: Message):
    completion = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-V3:together",
        messages=[{"role": "user", "content": message.content}],
    )
    # ✅ Return full object (works in preview and now CORS allows web fetch)
    return {"reply": completion.choices[0].message}
