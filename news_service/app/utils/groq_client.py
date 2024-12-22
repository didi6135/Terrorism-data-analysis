import os
from groq import Groq

from news_service.app.utils.config import GROQ_API_KEY


# Initialize Groq client
def get_groq_client():
    api_key = GROQ_API_KEY
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable not set.")
    return Groq(api_key=api_key)

# Create a chat completion
def create_chat_completion(messages, model="llama3-8b-8192"):
    client = get_groq_client()
    response = client.chat.completions.create(
        messages=messages,
        model=model,
    )
    return response



