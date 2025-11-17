from fastapi import APIRouter
from openai import OpenAI

router = APIRouter()
client = OpenAI()

@router.post("/report")
def generate_report(data: dict):
    prediction = data["prediction"]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an EV forecast analyst."},
            {"role": "user", "content": f"Generate EV demand report for prediction: {prediction}"}
        ]
    )

    return {"report": response.choices[0].message["content"]}
