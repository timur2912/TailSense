from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import requests
import logging
from datetime import datetime
from typing import Dict, Any

from models import ChatRequest, ChatResponse, ErrorResponse, HealthResponse
from config import settings

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=settings.cors_methods,
    allow_headers=settings.cors_headers,
)


# Dependency for checking external API availability
async def check_external_api():
    """Check external API service availability"""
    try:
        # Simple availability check without full request
        response = requests.head(
            settings.external_api_url.split("/api/v1/run")[0] + "/health",
            timeout=5
        )
        return True
    except Exception as e:
        logger.warning(f"External API might be unavailable: {e}")
        return True  # Continue working even if health check failed


@app.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check endpoint",
    description="Returns API service status"
)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version=settings.api_version
    )


@app.post(
    "/api/v1/chat",
    response_model=Dict[str, Any],
    summary="Send message to AI assistant",
    description="Sends message to veterinary AI assistant and returns response",
    responses={
        200: {
            "description": "Successful response from AI assistant",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Response from AI assistant",
                        "session_id": "550e8400-e29b-41d4-a716-446655440000"
                    }
                }
            }
        },
        400: {"model": ErrorResponse, "description": "Bad request"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
        503: {"model": ErrorResponse, "description": "External service unavailable"}
    }
)
async def chat(
    request: ChatRequest,
    api_available: bool = Depends(check_external_api)
):
    """
    Process chat request to AI assistant
    
    Accepts user message and returns response from veterinary AI assistant.
    Automatically generates session_id if not provided.
    """
    try:
        # Подготовка заголовков для внешнего API
        headers = {
            "Content-Type": "application/json",
            "x-api-key": settings.external_api_key
        }
        
        # Подготовка payload для внешнего API
        payload = {
            "output_type": request.output_type,
            "input_type": request.input_type,
            "input_value": request.input_value,
            "session_id": request.session_id
        }
        
        logger.info(f"Sending request to external API with session_id: {request.session_id}")
        
        # Send request to external API
        response = requests.post(
            settings.external_api_url,
            json=payload,
            headers=headers,
            timeout=settings.request_timeout
        )
        
        # Check response status
        response.raise_for_status()
        
        # Parse response
        resp_json = response.json()
        
        # Extract message text
        try:
            message_text = resp_json["outputs"][0]["outputs"][0]["results"]["message"]["data"]["text"]
            session_id = resp_json.get("session_id", request.session_id)
        except (KeyError, IndexError, TypeError) as e:
            logger.error(f"Error parsing response structure: {e}")
            raise HTTPException(
                status_code=500,
                detail="Unexpected response structure from external API"
            )
        
        # Return simplified response
        return {
            "message": message_text,
            "session_id": session_id
        }
        
    except requests.exceptions.Timeout:
        logger.error("Request timeout to external API")
        raise HTTPException(
            status_code=503,
            detail="Request timeout to AI service"
        )
    
    except requests.exceptions.ConnectionError:
        logger.error("Connection error to external API")
        raise HTTPException(
            status_code=503,
            detail="Unable to connect to AI service"
        )
    
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error from external API: {e}")
        if e.response.status_code == 401:
            raise HTTPException(
                status_code=500,
                detail="Authorization error in external API"
            )
        elif e.response.status_code == 429:
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded for AI service"
            )
        else:
            raise HTTPException(
                status_code=500,
                detail=f"External API error: {e.response.status_code}"
            )
    
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )


@app.get(
    "/api/v1/sessions/{session_id}",
    summary="Get session information",
    description="Returns information about existing chat session"
)
async def get_session_info(session_id: str):
    """Getting information about the session"""
    # In real application there would be database logic here
    return {
        "session_id": session_id,
        "status": "active",
        "created_at": datetime.now().isoformat()
    }


# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "detail": None}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """General exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc)}
    )


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info"
    )
