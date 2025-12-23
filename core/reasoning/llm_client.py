import os
from groq import Groq
from dotenv import load_dotenv
load_dotenv()

class LLMClient:
    def __init__(self, model_name="llama-3.1-8b-instant"):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError("GROQ_API_KEY not found in environment variables.")
        
        self.client = Groq(api_key=api_key)
        self.model = model_name
   
    def explain(self, prompt: str)-> str:
        response = self.client.chat.completions.create(
            model = self.model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a senior software engineer. "
                        "You only reason using provided evidence. "
                        "Do not hallucinate."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0.2,
            max_tokens=300,
        )

        return response.choices[0].message.content
    
    def generate(self, messages, max_tokens=400):
        response = self.client.chat.completions.create(
            model = self.model,
            messages = messages,
            temperature = 0.2,
            max_tokens = max_tokens,
        )
        return response.choices[0].message.content