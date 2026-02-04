from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Union, Any
from datetime import datetime

class Message(BaseModel):
    sender: str = Field(..., description="Either 'scammer' or 'user'")
    text: str = Field(..., alias="content", description="Message content")
    timestamp: Optional[Union[str, float, int]] = Field(default_factory=lambda: datetime.now().isoformat(), description="ISO-8601 timestamp")

    model_config = ConfigDict(populate_by_name=True, extra='ignore')

class Metadata(BaseModel):
    channel: Optional[str] = Field(None, description="SMS, WhatsApp, Email, Chat")
    language: Optional[str] = Field("English", description="Language of conversation")
    locale: Optional[str] = Field("IN", description="Country/region code")

    model_config = ConfigDict(populate_by_name=True, extra='ignore')

class ScamDetectionRequest(BaseModel):
    message: Message
    conversationHistory: Optional[List[Message]] = Field(default_factory=list, alias="conversation_history")
    metadata: Optional[Metadata] = None

    model_config = ConfigDict(populate_by_name=True, extra='ignore')

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
