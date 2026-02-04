from pydantic import BaseModel, Field, validator, ConfigDict
from typing import List, Optional, Dict, Any, Union
from datetime import datetime

class Message(BaseModel):
    sender: str = Field(default="scammer", description="Either 'scammer' or 'user'")
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
    metadata: Optional[Metadata] = Field(default=None)
    
    @validator('conversationHistory', pre=True, always=True)
    def ensure_list(cls, v):
        """Ensure conversationHistory is always a list"""
        if v is None:
            return []
        return v
    
    @validator('metadata', pre=True, always=True)
    def ensure_metadata(cls, v):
        """Create default metadata if missing"""
        if v is None:
            return Metadata()
        if isinstance(v, dict):
            return Metadata(**v)
        return v
    
    model_config = ConfigDict(populate_by_name=True, extra='ignore')

class EngagementMetrics(BaseModel):
    engagementDurationSeconds: int = 0
    totalMessagesExchanged: int = 0
    model_config = ConfigDict(populate_by_name=True, extra='ignore')

class ExtractedIntelligence(BaseModel):
    bankAccounts: List[str] = Field(default_factory=list)
    upiIds: List[str] = Field(default_factory=list)
    phoneNumbers: List[str] = Field(default_factory=list)
    phishingLinks: List[str] = Field(default_factory=list)
    emailAddresses: List[str] = Field(default_factory=list)
    model_config = ConfigDict(populate_by_name=True, extra='ignore')

class ScamDetectionResponse(BaseModel):
    status: str = "success"
    scamDetected: bool
    agentResponse: Optional[str] = None
    engagementMetrics: Optional[EngagementMetrics] = None
    extractedIntelligence: Optional[ExtractedIntelligence] = None
    agentNotes: Optional[str] = None
    
    model_config = ConfigDict(populate_by_name=True, extra='ignore')

class ErrorResponse(BaseModel):
    status: str = "error"
    message: str
