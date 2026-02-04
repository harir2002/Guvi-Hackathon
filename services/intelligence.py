from services.groq_service import call_groq, parse_json_response
from prompts import INTELLIGENCE_EXTRACTION_PROMPT
from models import Message, ExtractedIntelligence
from typing import List

async def extract_intelligence(conversation_history: List[Message], latest_message: Message, agent_response: str) -> ExtractedIntelligence:
    """Extract intelligence from conversation"""
    
    # Build full conversation
    conversation_lines = []
    for msg in conversation_history:
        conversation_lines.append(f"{msg.sender}: {msg.text}")
    conversation_lines.append(f"{latest_message.sender}: {latest_message.text}")
    conversation_lines.append(f"user: {agent_response}")
    
    full_conversation = "\n".join(conversation_lines)
    
    # Create extraction prompt
    prompt = INTELLIGENCE_EXTRACTION_PROMPT.format(
        full_conversation=full_conversation
    )
    
    # Call Groq
    response = await call_groq(prompt, temperature=0.2, max_tokens=1024)
    
    # Parse response
    intelligence_data = parse_json_response(response)
    
    return ExtractedIntelligence(**intelligence_data)
