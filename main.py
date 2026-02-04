from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from datetime import datetime

from config import get_settings
from models import (
    ScamDetectionRequest, 
    ScamDetectionResponse, 
    ErrorResponse,
    EngagementMetrics,
    ExtractedIntelligence
)
from services.scam_detector import detect_scam
from services.agent_service import generate_agent_response
from services.intelligence import extract_intelligence
from database.session_store import get_session_id, load_session, save_session, initialize_session
from database.chroma_db import store_conversation

# Initialize app
app = FastAPI(
    title="Scam Detection API",
    description="Agentic Honey-Pot for Scam Detection & Intelligence Extraction",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

settings = get_settings()

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "Scam Detection API",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/scam-detection", response_model=ScamDetectionResponse)
async def scam_detection_endpoint(
    request: ScamDetectionRequest,
    x_api_key: str = Header(..., description="API Key for authentication")
):
    """Main scam detection endpoint"""
    
    # Validate API key
    if x_api_key != settings.API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    try:
        # Step 1: Detect scam
        detection_result = await detect_scam(
            request.message,
            request.conversationHistory
        )
        
        if not detection_result.get("is_scam", False):
            # Not a scam - return simple response
            return ScamDetectionResponse(
                status="success",
                scamDetected=False,
                agentNotes="No scam detected in this message"
            )
        
        # Step 2: Get or create session
        session_id = get_session_id(
            request.message.sender,
            request.message.timestamp
        )
        session = load_session(session_id) or initialize_session(session_id)
        session["turn_count"] += 1
        
        # Step 3: Generate agent response
        agent_response = await generate_agent_response(
            scammer_message=request.message.text,
            conversation_history=request.conversationHistory,
            metadata=request.metadata
        )
        
        # Step 4: Extract intelligence (after 2+ turns)
        intelligence = ExtractedIntelligence()
        if session["turn_count"] >= 2:
            intelligence = await extract_intelligence(
                request.conversationHistory,
                request.message,
                agent_response
            )
            session["intelligence_extracted"] = True
            
            # Store in ChromaDB
            full_conversation = "\n".join([
                f"{msg.sender}: {msg.text}" for msg in request.conversationHistory
            ]) + f"\n{request.message.sender}: {request.message.text}\nuser: {agent_response}"
            
            store_conversation(
                session_id=session_id,
                conversation_text=full_conversation,
                metadata={
                    "scam_type": detection_result.get("scam_type", "unknown"),
                    "turn_count": session["turn_count"],
                    "confidence": detection_result.get("confidence", 0.0)
                }
            )
        
        # Update session
        save_session(session_id, session)
        
        # Step 5: Build response
        return ScamDetectionResponse(
            status="success",
            scamDetected=True,
            agentResponse=agent_response,
            engagementMetrics=EngagementMetrics(
                engagementDurationSeconds=session["turn_count"] * 60,
                totalMessagesExchanged=session["turn_count"] * 2
            ),
            extractedIntelligence=intelligence if session["intelligence_extracted"] else None,
            agentNotes=detection_result.get("reasoning", "Scam detected")
        )
        
    except Exception as e:
        print(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Custom exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            status="error",
            message=exc.detail
        ).dict()
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True if settings.DEBUG else False
    )
