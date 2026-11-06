from mistralai.client import MistralClient
import os
from dotenv import load_dotenv

load_dotenv()
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

def generate_post(topic):
    client = MistralClient(api_key=MISTRAL_API_KEY)
    response = client.chat(
        model="mistral-tiny",
        messages=[{"role": "user", "content": f"اكتب منشور ذكي وجذاب عن: {topic}"}]
    )
    return response.choices[0].message.content
