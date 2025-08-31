import os
from openai import OpenAI
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ Add CORS after app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 👈 or ["https://gd.games"] if you want to restrict
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

    # ✅ Extract only the text (string)
    reply = completion.choices[0].message["content"]
    return {"reply": reply}
