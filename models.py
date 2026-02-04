from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime

class Message(BaseModel):
    sender: str = Field(..., description="Either 'scammer' or 'user'")
    text: str = Field(..., description="Message content")
    timestamp: str = Field(..., description="ISO-8601 timestamp")

class Metadata(BaseModel):
    channel: Optional[str] = Field(None, description="SMS, WhatsApp, Email, Chat")
    language: Optional[str] = Field("English", description="Language of conversation")
    locale: Optional[str] = Field("IN", description="Country/region code")

class ScamDetectionRequest(BaseModel):
    message: Message
    conversationHistory: List[Message] = Field(default_factory=list)
    metadata: Optional[Metadata] = None

class EngagementMetrics(BaseModel):
    engagementDurationSeconds: int
    totalMessagesExchanged: int

class ExtractedIntelligence(BaseModel):
    bankAccounts: List[str] = Field(default_factory=list)
    upiIds: List[str] = Field(default_factory=list)
    phoneNumbers: List[str] = Field(default_factory=list)
    phishingLinks: List[str] = Field(default_factory=list)
    emailAddresses: List[str] = Field(default_factory=list)

class ScamDetectionResponse(BaseModel):
    status: str = "success"
    scamDetected: bool
    agentResponse: Optional[str] = None
    engagementMetrics: Optional[EngagementMetrics] = None
    extractedIntelligence: Optional[ExtractedIntelligence] = None
    agentNotes: Optional[str] = None

class ErrorResponse(BaseModel):
    status: str = "error"
    message: str
