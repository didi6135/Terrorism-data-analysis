import requests

from news_service.app.utils.config import GROQ_API_KEY
from news_service.app.utils.groq_client import create_chat_completion



def classify_article(title, body):
    prompt = f"""
    Classify the following article into one of three categories:
    - 'General News'
    - 'Historical Terror Event'
    - 'Current Terror Event'

    Title: {title}
    Body: {body}

    Return only the category name.
    """
    messages = [{"role": "user", "content": prompt}]
    response = create_chat_completion(messages)
    return response.choices[0].message.content.strip()




def extract_location(title, body):
    prompt = f"""
            Analyze the following article and extract the most likely geographical location (city, country, or region) mentioned.

            Title: {title}
            Body: {body}

            If no specific location is mentioned, return only the word 'Global'.
            If there is a location, return only the location name.
            Do not add any additional comments or explanations.
            """
    messages = [{"role": "user", "content": prompt}]
    print(f"Sending to Groq API: {messages}")  # Debug log
    response = create_chat_completion(messages)
    print(f"Response from Groq API: {response.choices[0].message.content}")  # Debug log

    location = response.choices[0].message.content.strip()

    # If the response is empty or matches fallback cases, return 'Global'
    if not location or location.lower() in ["global", "none", "unknown", "no location mentioned"]:
        return "Global"

    return location


