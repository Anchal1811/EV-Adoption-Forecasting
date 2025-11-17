from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_report(year: int, value: float):
    prompt = f"""
    Generate a clean EV adoption forecast summary:
    Year: {year}
    Projected EV Count: {value}
    """

    response = client.responses.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    # Extract text from new API response format
    result = response.output[0].content[0].text

    return result
