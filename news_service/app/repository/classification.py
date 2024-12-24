import spacy

from news_service.app.utils.groq_client import create_chat_completion



def classify_article(title, body):
    prompt = f"""
    Classify the following article into one of three categories:
    - General News
    - Historical Terror Event
    - Current Terror Event

    Title: {title}
    Body: {body}

    Return only the category name.
    """
    messages = [{"role": "user", "content": prompt}]
    response = create_chat_completion(messages)
    return response.choices[0].message.content.strip()


def try_groq_extraction(title: str, body: str) -> str:
    try:
        prompt = f"""
            Analyze the following article and extract the most significant geographical location (city, country, or region).
            Pay special attention to:
            1. Locations mentioned in the title
            2. Locations that are the main focus of events
            3. Most frequently mentioned locations

            Title: {title}
            Body: {body}

            Return only the name of the single most significant location.
            Do not return 'Global' unless absolutely no location is mentioned.
            Do not add any explanations or additional text.
            """
        messages = [{"role": "user", "content": prompt}]
        response = create_chat_completion(messages)
        location = response.choices[0].message.content.strip()

        # More strict filtering of invalid responses
        invalid_responses = ["global", "none", "unknown", "no location", "multiple", "various"]
        if location and location.lower() not in invalid_responses:
            return location

    except Exception as e:
        print(f"Groq API error: {e}")

    return ""


def get_primary_location(locations: list, title: str = "") -> str:
    """
    Get primary location with enhanced logic for title matches
    """
    if not locations:
        return ""

    # Create location frequency dict
    location_counts = {}
    for loc in locations:
        # Give extra weight to locations in title
        if title and loc in title:
            location_counts[loc] = location_counts.get(loc, 0) + 3  # Triple weight for title mentions
        location_counts[loc] = location_counts.get(loc, 0) + 1

    # Get location with highest count
    primary_location = max(location_counts.items(), key=lambda x: x[1])[0]
    return primary_location



def try_spacy_extraction(text: str, title: str = "") -> str:
    try:
        nlp = spacy.load('en_core_web_sm')
        doc = nlp(text)

        # Get GPE (geo-political entities) and LOC (locations)
        locations = [entity.text for entity in doc.ents if entity.label_ in ['GPE', 'LOC']]

        if locations:
            return get_primary_location(locations, title)

    except Exception as e:
        print(f"spaCy error: {e}")

    return ""


def extract_location(title: str, body: str) -> str:

    # Try Groq first
    groq_location = try_groq_extraction(title, body)

    # If Groq returns 'Global' or is empty, fallback to spaCy
    if not groq_location or groq_location.lower() in ["global", "none", "unknown", "no location", "multiple",
                                                      "various"]:
        spacy_location = try_spacy_extraction(body, title)
        if spacy_location:
            return spacy_location

    # If Groq provides a valid location or spaCy fails, return Groq's location
    return groq_location or "Global"


