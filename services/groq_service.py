from groq import Groq
import json
import re
from config import get_settings
import asyncio

settings = get_settings()
client = Groq(api_key=settings.GROQ_API_KEY)

async def call_groq(prompt: str, temperature: float = 0.7, max_tokens: int = 512) -> str:
    """Call Groq with timeout protection"""
    try:
        # Run in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        
        def sync_call():
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful AI assistant. Be concise."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model="llama-3.3-70b-versatile",
                temperature=temperature,
                max_tokens=max_tokens,  # Reduced for speed
                top_p=1,
                stream=False,
                timeout=10  # Groq API timeout
            )
            return chat_completion.choices[0].message.content.strip()
        
        response = await asyncio.wait_for(
            loop.run_in_executor(None, sync_call),
            timeout=12.0
        )
        
        # Clean markdown
        response = re.sub(r'^```json\s*', '', response)
        response = re.sub(r'\s*```$', '', response)
        
        return response
        
    except asyncio.TimeoutError:
        raise Exception("Groq API timeout")
    except Exception as e:
        print(f"Groq API Error: {e}")
        raise Exception(f"Groq API call failed: {str(e)}")

def parse_json_response(response: str) -> dict:
    """Parse JSON response"""
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        raise ValueError("Could not parse JSON")
