import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=API_KEY)

FAST_MODEL = "models/gemini-2.0-flash-lite-001"
QUALITY_MODEL = "models/gemini-2.5-pro"

def call_llm(prompt: str, model: str | None = None) -> str:
    if model is None:
        model = FAST_MODEL
    try:
        llm = genai.GenerativeModel(model)
        response = llm.generate_content(prompt)
        return response.text or ""
    except Exception as e:
        try:
            llm = genai.GenerativeModel(FAST_MODEL)
            response = llm.generate_content(f"Fallback due to error: {e}\n\n{prompt}")
            return response.text or ""
        except:
            return f"LLM Failure: {e}"
