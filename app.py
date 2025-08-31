import os
from openai import OpenAI
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or restrict to ["https://gd.games"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# HuggingFace API setup
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ.get("HF_TOKEN"),  # Make sure this is set in Render!
)

class Message(BaseModel):
    content: str

@app.post("/ask")
def ask(message: Message):
    try:
        completion = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V3:together",
            messages=[
                {"role": "user", "content": message.content}
            ],
        )

        # Access the reply safely
        reply = completion.choices[0].message.content
        return {"reply": reply}

    except Exception as e:
        # 👀 Debug output
        return {"error": str(e)}
