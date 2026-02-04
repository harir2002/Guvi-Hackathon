from services.groq_service import call_groq
from prompts import AGENT_ENGAGEMENT_PROMPT
from models import Message, Metadata
from typing import List

async def generate_agent_response(
    scammer_message: str,
    conversation_history: List[Message],
    metadata: Metadata
) -> str:
    """Generate human-like response from AI agent"""
    
    # Format conversation history
    history_text = "\n".join([
        f"{msg.sender}: {msg.text}" for msg in conversation_history
    ]) if conversation_history else "This is the first message"
    
    # Create engagement prompt
    prompt = AGENT_ENGAGEMENT_PROMPT.format(
        language=metadata.language if metadata else "English",
        conversation_history=history_text,
        scammer_message=scammer_message
    )
    
    # Call Groq with higher temperature for natural responses
    response = await call_groq(prompt, temperature=0.85, max_tokens=512)
    
    return response.strip()
