# backend/app/routers/assistant.py

from fastapi import APIRouter, HTTPException
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file

router = APIRouter(prefix="/api/v1/assistant")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@router.post("/chat")
def ev_assistant(payload: dict):
    try:
        user_message = payload.get("message", "")

        if not user_message:
            raise HTTPException(status_code=400, detail="Message is required.")

        # New OpenAI API format
        response = client.responses.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are an EV expert assistant. Help users with EV range, charging, and battery health."
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        )

        ai_message = response.output[0].content[0].text

        return {"response": ai_message}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chatbot ERROR → {str(e)}")
