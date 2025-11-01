import google.generativeai as genai
from threading import Lock
import subprocess
import os
import tempfile
from google.genai import types
from google.generativeai.types import generation_types
class GeminiClient:
    """
    Singleton wrapper for Google Gemini LLM.
    Usage:
        client = GeminiClient.get_instance("YOUR_API_KEY")
        response = client.get_response("Explain AI in simple terms.")
    """

    _instance = None
    _lock = Lock()

    def __init__(self, api_key: str="AIzaSyD_LZvBS3iqIYU-2a6ZgFrdn89uaQhG9FM", model_name: str = "gemini-2.5-flash"):
        if not api_key:
            raise ValueError("API key must be provided.")

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(
            model_name,
            generation_config={
                "temperature": 0.7,      # creativity control
                        # diversity control
                
            }
        )

    @classmethod
    def get_instance(cls, api_key: str = None):
        """Get or create the singleton instance."""
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = cls(api_key)
        return cls._instance

    def get_response(self, prompt: str) -> str:
        """Generate text response for a given prompt."""
        if not prompt.strip():
            return "Prompt cannot be empty."

        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"Error generating response: {e}"


if __name__ == "__main__":
    API_KEY = "AIzaSyD_LZvBS3iqIYU-2a6ZgFrdn89uaQhG9FM"
    client = GeminiClient.get_instance(API_KEY)

    user_input = "Summarize the history of the Internet."
    output = client.get_response(user_input)
    print("Gemini:", output)


