from typing import Dict, List, Optional, Any, Literal
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class IntentType(str, Enum):
    SCHEDULING = "scheduling"
    PRICING = "pricing"  
    GENERAL_INFO = "general_info"
    MIXED = "mixed"

class ActionType(str, Enum):
    GET_AVAILABILITY = "get_availability"
    GET_PRICING = "get_pricing"
    THINK = "think"
    RESPOND = "respond"

class ToolCall(BaseModel):
    tool_name: str
    parameters: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.now)

class ToolResult(BaseModel):
    tool_name: str
    result: Any
    success: bool
    error_message: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)

class AgentThought(BaseModel):
    reasoning: str
    intent_detected: IntentType
    next_action: ActionType
    confidence: float = Field(ge=0.0, le=1.0)
    timestamp: datetime = Field(default_factory=datetime.now)

class AgentStep(BaseModel):
    step_id: int
    thought: Optional[AgentThought] = None
    action: Optional[ToolCall] = None
    observation: Optional[ToolResult] = None
    timestamp: datetime = Field(default_factory=datetime.now)

class ConversationContext(BaseModel):
    user_query: str
    conversation_history: List[Dict[str, str]] = Field(default_factory=list)
    detected_services: List[str] = Field(default_factory=list)
    customer_info: Optional[Dict[str, Any]] = None
    session_id: str
    
    # Chain agents specific fields
    intent_analysis: Optional[Dict[str, Any]] = None
    scheduling_info: Optional[Dict[str, Any]] = None
    pricing_info: Optional[Dict[str, Any]] = None
    
    class Config:
        arbitrary_types_allowed = True

class AgentResponse(BaseModel):
    response: str
    intent_detected: IntentType
    tools_used: List[str]
    confidence: float
    processing_steps: List[AgentStep]
    conversation_context: ConversationContext

class ChatRequest(BaseModel):
    query: str
    session_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str
    intent: IntentType
    confidence: float
    tools_used: List[str]
    timestamp: datetime = Field(default_factory=datetime.now)
