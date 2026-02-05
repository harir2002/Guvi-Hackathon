from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict
from datetime import datetime

class Message(BaseModel):
    sender: str = Field(default="scammer")
    text: str
    timestamp: int  # Changed to int for Unix timestamp
    
    class Config:
        extra = "allow"

class Metadata(BaseModel):
    channel: Optional[str] = None
    language: Optional[str] = "English"
    locale: Optional[str] = "IN"
    
    class Config:
        extra = "allow"

class ScamDetectionRequest(BaseModel):
    sessionId: Optional[str] = None  # NEW FIELD from Guvi
    message: Message
    conversationHistory: Optional[List[Message]] = Field(default_factory=list)
    metadata: Optional[Metadata] = None
    
    class Config:
        extra = "allow"

# SIMPLIFIED RESPONSE - What Guvi Actually Wants
class ScamDetectionResponse(BaseModel):
    status: str = "success"
    reply: str  # Agent's response message
    
    class Config:
        extra = "allow"

class ErrorResponse(BaseModel):
    status: str = "error"
    message: str
