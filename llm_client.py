import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    print("⚠️ No Gemini API key found in .env")

def call_llm(prompt, model="gemini-2.0-flash"):
    try:
        model = genai.GenerativeModel(model)
        res = model.generate_content(prompt)
        return res.text
    except Exception as e:
        return f"[LLM ERROR] {e}"
