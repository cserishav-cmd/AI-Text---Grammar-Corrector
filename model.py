import os
import google.generativeai as genai
from dotenv import load_dotenv

class GeminiCorrectionModule:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found. Please set it in your .env file.")
        genai.configure(api_key=api_key)
        
        # Using the latest, fastest model from Google
        self.model = genai.GenerativeModel('gemini-1.5-flash-latest')

    def correct_text(self, text_to_correct):
        prompt = (
            "You are an expert editor. Please correct the spelling and grammar of the following text. "
            "Only return the fully corrected text and nothing else. Do not add any commentary, greetings, or explanations."
            f"\n\nOriginal Text: \"{text_to_correct}\""
            "\n\nCorrected Text:"
        )
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"An error occurred: {e}")
            return f"Error correcting text. Please check the console. Original text: {text_to_correct}"