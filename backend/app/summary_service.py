from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_summary(forecast_data):
    prompt = f"""
    Generate a clean summary of EV adoption based on this data:
    {forecast_data}

    Explain trends, growth, and projections.
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message["content"]
