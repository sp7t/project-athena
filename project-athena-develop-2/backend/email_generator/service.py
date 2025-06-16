import os  # noqa: I001, INP001
from dotenv import load_dotenv
from backend.email_generator.prompts import EMAIL_GENERATION_PROMPT
import google.generativeai as genai

# Load .env
load_dotenv()

# Load Gemini key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")


async def generate_email(candidate, verdict, rejection_reason, notes):  # noqa: ANN001, ANN201, D103
    prompt = EMAIL_GENERATION_PROMPT.format(
        name=candidate["name"],
        title=candidate["title"],
        experience=candidate["experience"],
        skills=", ".join(candidate["skills"]),
        verdict=verdict,
        rejection_reason=rejection_reason or "N/A",
        notes=notes or "N/A",
    )

    response = model.generate_content(prompt)
    return response.text
