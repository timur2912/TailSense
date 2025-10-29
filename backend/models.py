from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
import uuid


class ChatRequest(BaseModel):
    """Chat API request model"""
    input_value: str = Field(..., description="User message text")
    session_id: Optional[str] = Field(default=None, description="Session ID (auto-generated if not provided)")
    output_type: str = Field(default="chat", description="Output data type")
    input_type: str = Field(default="chat", description="Input data type")

    def __init__(self, **data):
        if "session_id" not in data or data["session_id"] is None:
            data["session_id"] = str(uuid.uuid4())
        super().__init__(**data)


class MessageData(BaseModel):
    """Message data model"""
    text: str = Field(..., description="AI response text")


class MessageResult(BaseModel):
    """Message result model"""
    message: MessageData


class OutputResult(BaseModel):
    """Output result model"""
    results: MessageResult


class Output(BaseModel):
    """Output data model"""
    outputs: list[OutputResult]


class ChatResponse(BaseModel):
    """Chat API response model"""
    outputs: list[Output]
    session_id: str = Field(..., description="Session ID")
    
    def get_message_text(self) -> str:
        """Extracts message text from response"""
        try:
            return self.outputs[0].outputs[0].results.message.text
        except (IndexError, AttributeError):
            return ""


class ErrorResponse(BaseModel):
    """Error model"""
    error: str = Field(..., description="Error description")
    detail: Optional[str] = Field(None, description="Additional error details")


class HealthResponse(BaseModel):
    """Health check response model"""
    status: str = Field(..., description="Service status")
    timestamp: str = Field(..., description="Check timestamp")
    version: str = Field(..., description="API version")
