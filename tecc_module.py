# tecc_module.py

#This is your entire TECC + Generative Reasoning layer from the paper.

# tecc_module.py

from groq import Groq

client = Groq(api_key="Upload your key here")

def correct_text(raw_text, confidence):
    prompt = f"""You are a text correction system for an indoor robot.
    OCR detected: "{raw_text}"
    Confidence: {confidence}

    Rules:
    1. Fix spelling errors only — do NOT change proper nouns or brand names
    2. Expand obvious abbreviations (ICU = Intensive Care Unit, F = Floor)
    3. If unreadable garbage, return INVALID
    4. Return maximum 5 words
    5. Do NOT change proper nouns, brand names, or hotel/building name
    6. Return ONLY the corrected text — no explanation, no punctuation, nothing else"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100
    )
    return response.choices[0].message.content.strip()


def query_map(semantic_map, user_query):
    landmarks_str = "\n".join([f"- {k}: {v}" for k, v in semantic_map.items()])

    prompt = f"""You are a navigation assistant for an indoor robot.
Available landmarks in the building:
{landmarks_str}

User said: "{user_query}"
Reply with the exact landmark name to navigate to. One word or short phrase only."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=50
    )
    return response.choices[0].message.content.strip()
