import json
from services.groq_service import call_groq, parse_json_response
from prompts import SCAM_DETECTION_PROMPT
from models import Message
from typing import List, Dict

async def detect_scam(message: Message, conversation_history: List[Message]) -> Dict:
    """Detect if a message is a scam"""
    
    # Format conversation history
    history_text = "\n".join([
        f"{msg.sender}: {msg.text}" for msg in conversation_history
    ]) if conversation_history else "No previous messages"
    
    # Create detection prompt
    prompt = SCAM_DETECTION_PROMPT.format(
        message_text=message.text,
        conversation_history=history_text
    )
    
    # Call Groq
    response = await call_groq(prompt, temperature=0.3, max_tokens=1024)
    
    # Parse response
    detection_result = parse_json_response(response)
    
    return detection_result
