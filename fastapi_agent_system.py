"""
FastAPI Agent Orchestration System for OnePath Interview

Key Interview Points to Emphasize:
1. Modular microservice architecture
2. Agent chaining and orchestration  
3. Error handling and resilience
4. Dynamic workflow management
5. Clear separation of concerns
"""

from fastapi import FastAPI, HTTPException, BackgroundTaskss
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any, Union
from enum import Enum
import asyncio
import uuid
from datetime import datetime
import json

# Import our ReACT agent
from react_architecture_guide import ReACTAgent, ActionType

app = FastAPI(
    title="OnePath Service Dispatch System",
    description="Agent-driven service dispatch and workflow orchestration",
    version="1.0.0"
)

# Enable CORS for web frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# MODELS - Interview Tip: Always define clear data models
# ============================================================================

class ServiceRequest(BaseModel):
    """Initial customer service request"""
    message: str = Field(..., description="Customer's service request message")
    customer_id: Optional[str] = Field(None, description="Customer identifier")
    priority: Optional[str] = Field("normal", description="Request priority level")
    location: Optional[Dict[str, Any]] = Field(None, description="Service location")

class AgentResponse(BaseModel):
    """Standard agent response format"""
    agent_id: str
    request_id: str
    reasoning: str
    action_taken: str
    result: Dict[str, Any]
    next_steps: List[str]
    confidence: float
    timestamp: datetime

class WorkflowStatus(BaseModel):
    """Current workflow status"""
    request_id: str
    status: str  # pending, processing, completed, failed
    current_agent: str
    steps_completed: List[str]
    next_action: Optional[str]
    estimated_completion: Optional[datetime]

class ServiceQuote(BaseModel):
    """Service pricing quote"""
    base_cost: float
    additional_services: Dict[str, float]
    total_cost: float
    bundle_discount: float
    emergency_surcharge: float

# ============================================================================
# AGENT ORCHESTRATOR - Core interview component
# ============================================================================

class AgentOrchestrator:
    """
    Central orchestrator for managing multiple agents and workflows
    
    Interview Strategy: Explain how this coordinates different specialized agents
    """
    
    def __init__(self):
        self.active_workflows = {}
        self.agent_registry = {
            "primary": ReACTAgent("PrimaryDispatchAgent"),
            "calendar": ReACTAgent("CalendarAgent"), 
            "pricing": ReACTAgent("PricingAgent"),
            "followup": ReACTAgent("FollowupAgent")
        }
    
    async def process_request(self, request: ServiceRequest) -> AgentResponse:
        """
        Main entry point - route request to appropriate agent chain
        
        Interview Points:
        1. Show how you decide which agent to start with
        2. Explain the routing logic
        3. Demonstrate error handling
        """
        
        request_id = str(uuid.uuid4())
        
        # Initialize workflow tracking
        self.active_workflows[request_id] = {
            "status": "processing",
            "current_agent": "primary",
            "steps": [],
            "context": {},
            "start_time": datetime.now()
        }
        
        try:
            # Start with primary agent for initial reasoning
            primary_agent = self.agent_registry["primary"]
            
            # Get initial reasoning and action plan
            reasoning_result = primary_agent.reason(
                request.message, 
                {"customer_id": request.customer_id, "priority": request.priority}
            )
            
            # Execute the determined action
            action_result = await self._execute_action_chain(
                request_id,
                reasoning_result["next_action"],
                {"original_request": request.message}
            )
            
            # Update workflow status
            self.active_workflows[request_id]["status"] = "completed"
            self.active_workflows[request_id]["steps"].append("primary_reasoning_complete")
            
            return AgentResponse(
                agent_id="primary",
                request_id=request_id,
                reasoning=reasoning_result["reasoning"],
                action_taken=str(reasoning_result["next_action"]),
                result=action_result,
                next_steps=self._determine_next_steps(action_result),
                confidence=reasoning_result["confidence"],
                timestamp=datetime.now()
            )
            
        except Exception as e:
            # Error handling - crucial for interview
            self.active_workflows[request_id]["status"] = "failed"
            self.active_workflows[request_id]["error"] = str(e)
            
            raise HTTPException(
                status_code=500,
                detail=f"Agent processing failed: {str(e)}"
            )
    
    async def _execute_action_chain(self, request_id: str, action_type: ActionType, context: Dict) -> Dict:
        """
        Execute a chain of actions based on the determined action type
        
        Interview Gold: Show how agents hand off to each other
        """
        
        workflow = self.active_workflows[request_id]
        
        if action_type == ActionType.CALENDAR_CHECK:
            # Hand off to calendar specialist agent
            workflow["current_agent"] = "calendar"
            calendar_agent = self.agent_registry["calendar"]
            
            result = calendar_agent.execute_action(ActionType.CALENDAR_CHECK, context)
            workflow["steps"].append("calendar_check_complete")
            
            # If calendar check successful, might need pricing next
            if result.get("available_slots"):
                pricing_result = await self._get_pricing_for_service(context)
                result["pricing"] = pricing_result
                workflow["steps"].append("pricing_added")
            
            return result
            
        elif action_type == ActionType.PRICING_QUERY:
            workflow["current_agent"] = "pricing"
            pricing_agent = self.agent_registry["pricing"]
            
            result = pricing_agent.execute_action(ActionType.PRICING_QUERY, context)
            workflow["steps"].append("pricing_complete")
            
            return result
            
        elif action_type == ActionType.CUSTOMER_FOLLOWUP:
            workflow["current_agent"] = "followup"
            followup_agent = self.agent_registry["followup"]
            
            result = followup_agent.execute_action(ActionType.CUSTOMER_FOLLOWUP, context)
            workflow["steps"].append("followup_generated")
            
            return result
        
        else:
            return {"error": "Unknown action type", "action": str(action_type)}
    
    async def _get_pricing_for_service(self, context: Dict) -> Dict:
        """Helper method to get pricing information"""
        pricing_agent = self.agent_registry["pricing"]
        return pricing_agent.execute_action(ActionType.PRICING_QUERY, context)
    
    def _determine_next_steps(self, action_result: Dict) -> List[str]:
        """
        Determine what the customer can do next
        
        Interview Tip: Always think about user experience and next actions
        """
        next_steps = []
        
        if "available_slots" in action_result:
            next_steps.append("Select preferred appointment time")
            
        if "pricing" in action_result:
            next_steps.append("Review pricing and confirm service")
            
        if "questions" in action_result:
            next_steps.append("Answer additional questions to refine service")
            
        if not next_steps:
            next_steps.append("Await customer response")
            
        return next_steps

# Global orchestrator instance
orchestrator = AgentOrchestrator()

# ============================================================================
# API ENDPOINTS - Interview focus: Clean, RESTful design
# ============================================================================

@app.post("/api/v1/service-request", response_model=AgentResponse)
async def create_service_request(request: ServiceRequest):
    """
    Main endpoint for service requests
    
    Interview Strategy: 
    1. Walk through the request flow
    2. Explain validation and error handling
    3. Show how this scales to multiple requests
    """
    
    # Input validation
    if not request.message.strip():
        raise HTTPException(
            status_code=400,
            detail="Service request message cannot be empty"
        )
    
    # Process through agent orchestrator
    try:
        response = await orchestrator.process_request(request)
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process service request: {str(e)}"
        )

@app.get("/api/v1/workflow/{request_id}", response_model=WorkflowStatus)
async def get_workflow_status(request_id: str):
    """
    Get current status of a workflow
    
    Interview Point: Show how you track long-running processes
    """
    
    if request_id not in orchestrator.active_workflows:
        raise HTTPException(
            status_code=404,
            detail="Workflow not found"
        )
    
    workflow = orchestrator.active_workflows[request_id]
    
    return WorkflowStatus(
        request_id=request_id,
        status=workflow["status"],
        current_agent=workflow["current_agent"],
        steps_completed=workflow["steps"],
        next_action=workflow.get("next_action"),
        estimated_completion=None  # Would calculate based on current step
    )

@app.post("/api/v1/followup/{request_id}")
async def handle_followup(request_id: str, followup_message: Dict[str, str]):
    """
    Handle customer followup messages
    
    Interview Gold: Show how conversations continue and context is maintained
    """
    
    if request_id not in orchestrator.active_workflows:
        raise HTTPException(
            status_code=404,
            detail="Original request not found"
        )
    
    workflow = orchestrator.active_workflows[request_id]
    
    # Add followup to context
    if "followups" not in workflow["context"]:
        workflow["context"]["followups"] = []
    
    workflow["context"]["followups"].append({
        "message": followup_message.get("message"),
        "timestamp": datetime.now().isoformat()
    })
    
    # Process followup through primary agent
    primary_agent = orchestrator.agent_registry["primary"]
    
    # Create enhanced context with conversation history
    enhanced_context = {
        **workflow["context"],
        "conversation_history": workflow["context"]["followups"],
        "current_status": workflow["status"]
    }
    
    reasoning_result = primary_agent.reason(
        followup_message.get("message", ""), 
        enhanced_context
    )
    
    # Execute new action based on followup
    action_result = await orchestrator._execute_action_chain(
        request_id,
        reasoning_result["next_action"],
        enhanced_context
    )
    
    return {
        "request_id": request_id,
        "reasoning": reasoning_result["reasoning"],
        "action_taken": str(reasoning_result["next_action"]),
        "result": action_result,
        "updated_workflow": workflow["steps"]
    }

@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "active_workflows": len(orchestrator.active_workflows),
        "agents_available": list(orchestrator.agent_registry.keys())
    }

# ============================================================================
# INTERVIEW DEMO ENDPOINTS - Show different scenarios
# ============================================================================

@app.post("/api/v1/demo/ac-repair")
async def demo_ac_repair():
    """
    Demo endpoint showing AC repair scenario
    
    Interview Strategy: Use this to walkthrough the complete flow
    """
    
    demo_request = ServiceRequest(
        message="My AC is broken. Can someone fix it this week?",
        customer_id="demo-customer-123",
        priority="urgent"
    )
    
    response = await orchestrator.process_request(demo_request)
    
    return {
        "scenario": "AC Repair Request",
        "demo_flow": "Customer request → Reasoning → Calendar check → Pricing → Response",
        "agent_response": response
    }

@app.post("/api/v1/demo/bundle-request")  
async def demo_bundle_request():
    """
    Demo endpoint showing bundle/add-on scenario
    
    Interview Focus: Show how system handles complex multi-service requests
    """
    
    demo_request = ServiceRequest(
        message="Can you add a thermostat installation too and bundle it?",
        customer_id="demo-customer-123",
        priority="normal"
    )
    
    response = await orchestrator.process_request(demo_request)
    
    return {
        "scenario": "Bundle Service Request",
        "demo_flow": "Bundle request → Pricing calculation → Bundle discount → Combined quote",
        "agent_response": response
    }

# ============================================================================
# STARTUP EVENT - Interview prep
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize system on startup"""
    print("🚀 OnePath Agent System Starting...")
    print("📊 Available Agents:", list(orchestrator.agent_registry.keys()))
    print("🔄 ReACT Architecture Loaded")
    print("✅ System Ready for Interview Demo")

if __name__ == "__main__":
    import uvicorn
    
    print("Starting OnePath Interview Demo System...")
    print("Visit http://localhost:8000/docs for API documentation")
    
    uvicorn.run(
        "fastapi_agent_system:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
