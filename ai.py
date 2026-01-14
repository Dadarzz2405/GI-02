from groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

GROQ_API_KEY = os.getenv("API_KEY")

if not GROQ_API_KEY:
    raise RuntimeError("API_KEY not found. Check your .env file.")

client = Groq(api_key=GROQ_API_KEY)

# System prompt
SYSTEM_PROMPT = """
You are an Islamic educational assistant for a school Rohis organization.
Explain concepts clearly and respectfully.
Do not issue fatwas or definitive rulings.
If a question requires a scholar, advise consulting a trusted ustadz.
Give concise short answers focused on Islamic teachings and values.
Avoid using table format in your responses.
Avoid using '**' for bold text in your responses.
If you don't know the answer, say "I'm sorry, I don't have that information."
Do not reference yourself as an AI model.
Keep answers under 200 words.
Do not provide legal, medical, or political advice.

If the user asks to go to a page or feature, respond ONLY with:
NAVIGATE: <page_name>

Valid page names:
dashboard, attendance, members, login
"""

# Safe route mapping (AI never sends URLs)
ROUTE_MAP = {
    "dashboard": "/dashboard",
    "attendance": "/attendance",
    "members": "/members",
    "login": "/login"
}

def call_chatbot_groq(message: str) -> dict:
    # Basic input guard
    if not message or len(message) > 500:
        return {
            "action": "chat",
            "message": "Please ask a shorter question."
        }

    try:
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT.strip()},
                {"role": "user", "content": message}
            ],
            temperature=0.4,
            max_tokens=200,
        )

        content = completion.choices[0].message.content.strip()

        # Handle navigation intent
        if content.startswith("NAVIGATE:"):
            page = content.replace("NAVIGATE:", "").strip().lower()
            route = ROUTE_MAP.get(page)

            if route:
                return {
                    "action": "navigate",
                    "redirect": route
                }
            else:
                return {
                    "action": "chat",
                    "message": "I'm sorry, I can't navigate to that page."
                }

        # Normal chatbot response
        return {
            "action": "chat",
            "message": content
        }

    except Exception:
        return {
            "action": "chat",
            "message": "I'm sorry, I can't respond right now. Please try again later."
        }

