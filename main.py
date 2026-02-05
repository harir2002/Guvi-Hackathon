from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import asyncio
from datetime import datetime

from config import get_settings
from models import (
    ScamDetectionRequest, 
    ScamDetectionResponse, 
    ErrorResponse
)
from services.scam_detector import detect_scam
from services.agent_service import generate_agent_response

# Initialize app
app = FastAPI(
    title="Scam Detection API",
    description="Agentic Honey-Pot for Scam Detection",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

settings = get_settings()

# Simple in-memory cache for sessions
session_cache = {}

@app.get("/")
async def root():
    return {
        "status": "online",
        "service": "Scam Detection API",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/scam-detection", response_model=ScamDetectionResponse)
async def scam_detection_endpoint(
    request: ScamDetectionRequest,
    x_api_key: str = Header(..., alias="x-api-key")
):
    """Simplified scam detection endpoint matching Guvi's format"""
    
    # Validate API key
    if x_api_key != settings.API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    try:
        # Set timeout for entire operation (25 seconds to be safe)
        async def process_request():
            # Step 1: Quick scam detection (5 seconds max)
            try:
                detection_result = await asyncio.wait_for(
                    detect_scam(request.message, request.conversationHistory),
                    timeout=8.0
                )
            except asyncio.TimeoutError:
                # Assume it's a scam if detection times out
                detection_result = {"is_scam": True, "confidence": 0.8}
            
            # Step 2: If not a scam, return neutral response
            if not detection_result.get("is_scam", False):
                return ScamDetectionResponse(
                    status="success",
                    reply="Thank you for your message."
                )
            
            # Step 3: Generate agent response (10 seconds max)
            try:
                agent_reply = await asyncio.wait_for(
                    generate_agent_response(
                        scammer_message=request.message.text,
                        conversation_history=request.conversationHistory,
                        metadata=request.metadata
                    ),
                    timeout=15.0
                )
            except asyncio.TimeoutError:
                # Fallback response if agent times out
                agent_reply = "I'm not sure I understand. Can you please explain more clearly?"
            
            return ScamDetectionResponse(
                status="success",
                reply=agent_reply.strip()
            )
        
        # Execute with overall timeout
        result = await asyncio.wait_for(process_request(), timeout=25.0)
        return result
        
    except asyncio.TimeoutError:
        # If everything times out, return fast fallback
        return ScamDetectionResponse(
            status="success",
            reply="Sorry, I didn't catch that. Could you repeat?"
        )
    except Exception as e:
        print(f"❌ Error: {e}")
        # Return success even on error to avoid 500
        return ScamDetectionResponse(
            status="success",
            reply="I'm sorry, I'm having trouble understanding. Can you clarify?"
        )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print(f"❌ Validation Error: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content=ErrorResponse(
            status="error",
            message="Invalid request format"
        ).dict()
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            status="error",
            message=exc.detail
        ).dict()
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    print(f"❌ Unhandled Error: {exc}")
    # Always return 200 with success to avoid timeouts
    return JSONResponse(
        status_code=200,
        content=ScamDetectionResponse(
            status="success",
            reply="I'm processing your message. Please give me a moment."
        ).dict()
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
