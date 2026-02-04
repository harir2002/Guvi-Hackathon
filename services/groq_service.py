from groq import Groq
import json
import re
from config import get_settings

settings = get_settings()
client = Groq(api_key=settings.GROQ_API_KEY)

async def call_groq(prompt: str, temperature: float = 0.7, max_tokens: int = 2048) -> str:
    """Call Groq Llama 3.3 70B model"""
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful AI assistant. Always respond with valid JSON when requested."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="llama-3.3-70b-versatile",
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=1,
            stream=False
        )
        
        response_text = chat_completion.choices[0].message.content.strip()
        
        # Clean markdown code blocks if present
        response_text = re.sub(r'^```json\s*', '', response_text)
        response_text = re.sub(r'\s*```$', '', response_text)
        
        return response_text
        
    except Exception as e:
        print(f"Groq API Error: {e}")
        raise Exception(f"Groq API call failed: {str(e)}")

def parse_json_response(response: str) -> dict:
    """Parse JSON response from Groq"""
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        # Try to extract JSON from text
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        raise ValueError("Could not parse JSON from response")
