import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)

FAST_MODEL = os.getenv("FLOWSPEC_FAST_MODEL", "gemini-2.0-flash")
QUALITY_MODEL = os.getenv("FLOWSPEC_QUALITY_MODEL", "gemini-2.0-pro")


def call_llm(prompt: str, model: str | None = None) -> str:
    """
    General LLM caller.
    - model=None -> use FAST_MODEL
    - model can be overridden per-call
    """
    if model is None:
        model = FAST_MODEL

    try:
        m = genai.GenerativeModel(model)
        res = m.generate_content(prompt)
        return res.text or ""
    except Exception as e:
        return f"LLM Error: {e}"
