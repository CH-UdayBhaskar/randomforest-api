# chatbot.py
from fastapi import APIRouter
from pydantic import BaseModel
import openai
import os

router = APIRouter()

#openai.api_key = os.getenv("OPENAI_API_KEY")  # Or load from env

# Setup OpenAI client (v1.x syntax)
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ChatRequest(BaseModel):
    message: str

@router.post("/chat")
async def chat(request: ChatRequest):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # or "gpt-4" or llama3 via API
            messages=[
                {"role": "system", "content": "You are an AI assistant for a prediction API."},
                {"role": "user", "content": request.message}
            ]
        )
        return {"response": response.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}
