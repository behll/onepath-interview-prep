"""
OnePath.ai Interview Project - LangChain Agent System
====================================================

Production-grade agent system using:
- LangChain for agent orchestration
- OpenAI function calling
- FastAPI for scalable APIs
- MCP-style multi-step reasoning
- ReACT architecture patterns

Interview Demo: AC Repair Service Dispatch System
"""

import os
import json
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
from enum import Enum

# LangChain imports
from langchain.agents import Tool, AgentExecutor, create_openai_functions_agent
from langchain.schema import AgentAction, AgentFinish
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferWindowMemory
from langchain.callbacks.base import BaseCallbackHandler
from langchain_openai import ChatOpenAI

# FastAPI imports
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Environment setup
from dotenv import load_dotenv
load_dotenv()

# ============================================================================
# MODELS & SCHEMAS - Interview Focus: Clear data structures
# ============================================================================

class ServiceType(str, Enum):
    AC_REPAIR = "ac_repair"
    HEATING = "heating"
    PLUMBING = "plumbing"
    ELECTRICAL = "electrical"

class UrgencyLevel(str, Enum):
    EMERGENCY = "emergency"
    HIGH = "high"
    NORMAL = "normal"
    LOW = "low"

class ServiceRequest(BaseModel):
    """Customer service request model"""
    message: str = Field(..., description="Customer's service request message")
    customer_id: Optional[str] = Field(None, description="Customer identifier")
    location: Optional[str] = Field(None, description="Service location")
    preferred_time: Optional[str] = Field(None, description="Preferred service time")

class AgentResponse(BaseModel):
    """Agent response model"""
    request_id: str
    reasoning: str
    actions_taken: List[str]
    result: Dict[str, Any]
    next_steps: List[str]
    confidence: float
    total_cost: Optional[float] = None

class FollowUpRequest(BaseModel):
    """Follow-up request model"""
    request_id: str
    message: str

# ============================================================================
# SERVICE LAYER - Mock External APIs (Interview: Show realistic integration)
# ============================================================================

class CalendarService:
    """
    Mock calendar service - In production would integrate with real API
    
    Interview Point: Show how you handle external service integration
    """
    
    @staticmethod
    async def check_availability(service_type: str, urgency: str, location: str = None) -> Dict[str, Any]:
        """
        Check technician availability
        
        Interview Strategy: Explain this would call real calendar API
        """
        # Simulate API delay
        await asyncio.sleep(0.1)
        
        # Mock availability data
        base_date = datetime.now() + timedelta(days=1)
        
        if urgency == "emergency":
            slots = [
                {
                    "datetime": base_date.strftime("%Y-%m-%d %H:%M"),
                    "technician": "Emergency Tech Mike",
                    "estimated_duration": "2-3 hours",
                    "travel_time": "30 minutes",
                    "surcharge": 75
                }
            ]
        else:
            slots = [
                {
                    "datetime": (base_date + timedelta(days=i)).strftime("%Y-%m-%d %H:%M"),
                    "technician": f"Tech {['Sarah', 'John', 'Mike'][i]}",
                    "estimated_duration": "2-3 hours",
                    "travel_time": "15 minutes",
                    "surcharge": 0
                }
                for i in range(3)
            ]
        
        return {
            "available_slots": slots,
            "earliest_available": slots[0]["datetime"] if slots else None,
            "emergency_available": urgency == "emergency"
        }

class PricingService:
    """
    Mock pricing service - In production would integrate with pricing API
    
    Interview Point: Show business logic integration
    """
    
    @staticmethod
    async def calculate_pricing(service_type: str, 
                              additional_services: List[str] = None,
                              urgency: str = "normal",
                              location: str = None) -> Dict[str, Any]:
        """
        Calculate service pricing with bundle optimization
        
        Interview Strategy: Show complex business logic handling
        """
        await asyncio.sleep(0.1)
        
        # Base pricing
        base_prices = {
            "ac_repair": {"diagnostic": 75, "repair": 150},
            "heating": {"diagnostic": 75, "repair": 175},
            "plumbing": {"diagnostic": 50, "repair": 125},
            "electrical": {"diagnostic": 100, "repair": 200}
        }
        
        # Additional services
        addon_prices = {
            "thermostat_install": 200,
            "filter_replacement": 25,
            "duct_cleaning": 300,
            "maintenance_plan": 150
        }
        
        base_cost = sum(base_prices.get(service_type, base_prices["ac_repair"]).values())
        addon_cost = sum(addon_prices.get(service, 0) for service in (additional_services or []))
        
        subtotal = base_cost + addon_cost
        
        # Bundle discount
        bundle_discount = 0.15 if additional_services and len(additional_services) > 0 else 0
        discount_amount = subtotal * bundle_discount
        
        # Urgency surcharge
        urgency_surcharge = {"emergency": 75, "high": 25}.get(urgency, 0)
        
        total = subtotal - discount_amount + urgency_surcharge
        tax = total * 0.08
        final_total = total + tax
        
        return {
            "base_cost": base_cost,
            "addon_cost": addon_cost,
            "subtotal": subtotal,
            "bundle_discount": discount_amount,
            "urgency_surcharge": urgency_surcharge,
            "tax": tax,
            "total": final_total,
            "savings": discount_amount,
            "payment_options": ["cash", "card", "financing"]
        }

# ============================================================================
# LANGCHAIN TOOLS - Interview Focus: Function calling integration
# ============================================================================

def create_calendar_tool() -> Tool:
    """
    Create calendar checking tool
    
    Interview Point: Show how to create LangChain tools with proper schemas
    """
    
    async def check_calendar(service_type: str, urgency: str = "normal", location: str = "default") -> str:
        """Check technician availability for service"""
        try:
            result = await CalendarService.check_availability(service_type, urgency, location)
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error checking calendar: {str(e)}"
    
    return Tool(
        name="check_calendar_availability",
        description="Check technician availability for service appointments. Use this when customer asks about scheduling or timing.",
        func=lambda **kwargs: asyncio.run(check_calendar(**kwargs))
    )

def create_pricing_tool() -> Tool:
    """
    Create pricing calculation tool
    
    Interview Point: Show complex business logic in tool form
    """
    
    async def calculate_price(service_type: str, 
                            additional_services: str = "", 
                            urgency: str = "normal") -> str:
        """Calculate pricing for services"""
        try:
            additional_list = [s.strip() for s in additional_services.split(",") if s.strip()] if additional_services else []
            result = await PricingService.calculate_pricing(service_type, additional_list, urgency)
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error calculating pricing: {str(e)}"
    
    return Tool(
        name="calculate_service_pricing",
        description="Calculate pricing for services including bundles and discounts. Use when customer asks about cost or wants to add services.",
        func=lambda **kwargs: asyncio.run(calculate_price(**kwargs))
    )

def create_analysis_tool() -> Tool:
    """
    Create customer request analysis tool
    
    Interview Point: Show business intelligence integration
    """
    
    def analyze_request(customer_message: str) -> str:
        """Analyze customer request for service type and urgency"""
        
        # Service type detection
        service_keywords = {
            "ac_repair": ["ac", "air conditioning", "cooling", "hvac", "conditioner"],
            "heating": ["heat", "heating", "furnace", "boiler", "warm"],
            "plumbing": ["plumb", "water", "leak", "pipe", "drain", "toilet"],
            "electrical": ["electric", "power", "outlet", "wiring", "lights"]
        }
        
        # Urgency detection
        urgency_keywords = {
            "emergency": ["emergency", "urgent", "asap", "immediately", "broken", "not working", "dead"],
            "high": ["soon", "this week", "quickly", "today", "tomorrow"],
            "normal": ["convenient", "schedule", "when possible"],
            "low": ["whenever", "no rush", "flexible"]
        }
        
        message_lower = customer_message.lower()
        
        # Detect service type
        detected_service = "ac_repair"  # default
        for service, keywords in service_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                detected_service = service
                break
        
        # Detect urgency
        detected_urgency = "normal"
        for urgency, keywords in urgency_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                detected_urgency = urgency
                break
        
        # Detect additional requests
        additional_services = []
        addon_keywords = {
            "thermostat_install": ["thermostat", "temperature control"],
            "filter_replacement": ["filter", "air filter"],
            "duct_cleaning": ["duct", "air duct"],
            "maintenance_plan": ["maintenance", "service plan", "regular service"]
        }
        
        for service, keywords in addon_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                additional_services.append(service)
        
        analysis = {
            "service_type": detected_service,
            "urgency_level": detected_urgency,
            "additional_services": additional_services,
            "customer_intent": "service_request",
            "requires_scheduling": "this week" in message_lower or "today" in message_lower or "tomorrow" in message_lower,
            "requires_pricing": "cost" in message_lower or "price" in message_lower or "how much" in message_lower
        }
        
        return json.dumps(analysis, indent=2)
    
    return Tool(
        name="analyze_customer_request",
        description="Analyze customer message to extract service type, urgency, and intent. Always use this first to understand what the customer needs.",
        func=analyze_request
    )

# ============================================================================
# CUSTOM CALLBACK HANDLER - Interview Focus: Observability
# ============================================================================

class InterviewCallbackHandler(BaseCallbackHandler):
    """
    Custom callback handler for interview demonstration
    
    Interview Point: Show how you add observability to LangChain agents
    """
    
    def __init__(self):
        self.actions_taken = []
        self.reasoning_steps = []
    
    def on_agent_action(self, action: AgentAction, **kwargs) -> None:
        """Log agent actions for interview demo"""
        self.actions_taken.append({
            "tool": action.tool,
            "input": action.tool_input,
            "timestamp": datetime.now().isoformat()
        })
        print(f"🔧 AGENT ACTION: {action.tool} with input: {action.tool_input}")
    
    def on_agent_finish(self, finish: AgentFinish, **kwargs) -> None:
        """Log agent completion"""
        print(f"✅ AGENT FINISHED: {finish.return_values}")

# ============================================================================
# MAIN AGENT ORCHESTRATOR - Interview Focus: Core system
# ============================================================================

class OnepathAgentOrchestrator:
    """
    Main agent orchestrator using LangChain + OpenAI
    
    Interview Strategy: This is your main demonstration piece
    """
    
    def __init__(self, openai_api_key: str = None):
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        if not self.openai_api_key:
            print("⚠️ Warning: No OpenAI API key found. Using mock responses.")
        
        self.llm = self._initialize_llm()
        self.tools = self._create_tools()
        self.agent = self._create_agent()
        self.active_sessions = {}
    
    def _initialize_llm(self) -> ChatOpenAI:
        """
        Initialize OpenAI LLM
        
        Interview Point: Show production-ready LLM configuration
        """
        if self.openai_api_key:
            return ChatOpenAI(
                model="gpt-4",
                temperature=0.1,  # Low temperature for consistent reasoning
                max_tokens=1000,
                openai_api_key=self.openai_api_key
            )
        else:
            # Mock LLM for demo without API key
            return None
    
    def _create_tools(self) -> List[Tool]:
        """
        Create available tools for the agent
        
        Interview Focus: Show comprehensive tool ecosystem
        """
        return [
            create_analysis_tool(),
            create_calendar_tool(),
            create_pricing_tool()
        ]
    
    def _create_agent(self) -> Optional[AgentExecutor]:
        """
        Create the main ReACT agent
        
        Interview Point: Show LangChain agent creation with custom prompts
        """
        if not self.llm:
            return None
        
        # Custom prompt for OnePath service dispatch
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert service dispatch agent for OnePath, a home services company.

Your role is to:
1. Analyze customer service requests intelligently
2. Use available tools to check availability and pricing
3. Provide helpful, accurate responses
4. Handle follow-up requests and service modifications
5. Always prioritize customer satisfaction and business efficiency

Key principles:
- Always analyze the customer request first using the analysis tool
- For scheduling requests, check calendar availability
- For pricing questions or bundles, calculate accurate pricing
- Be conversational and helpful
- Ask clarifying questions when needed
- Show your reasoning process clearly

Available tools: {tools}

Remember: You're helping real customers with real home service needs. Be professional, efficient, and thorough."""),
            
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])
        
        # Create agent with tools
        agent = create_openai_functions_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt
        )
        
        # Create memory for conversation continuity
        memory = ConversationBufferWindowMemory(
            k=10,  # Keep last 10 exchanges
            memory_key="chat_history",
            return_messages=True
        )
        
        return AgentExecutor(
            agent=agent,
            tools=self.tools,
            memory=memory,
            verbose=True,
            max_iterations=5,
            handle_parsing_errors=True
        )
    
    async def process_service_request(self, request: ServiceRequest) -> AgentResponse:
        """
        Process initial service request
        
        Interview Strategy: This is your main demo method
        """
        request_id = f"req_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        print(f"🎯 PROCESSING SERVICE REQUEST: {request_id}")
        print(f"Customer Message: '{request.message}'")
        
        # Create callback handler for observability
        callback_handler = InterviewCallbackHandler()
        
        if self.agent:
            try:
                # Use LangChain agent
                result = await self._process_with_langchain(request, callback_handler)
            except Exception as e:
                print(f"❌ LangChain processing failed: {e}")
                result = await self._process_with_fallback(request)
        else:
            # Fallback to manual processing
            result = await self._process_with_fallback(request)
        
        # Store session for follow-ups
        self.active_sessions[request_id] = {
            "original_request": request,
            "conversation_history": [request.message],
            "last_result": result,
            "timestamp": datetime.now()
        }
        
        return AgentResponse(
            request_id=request_id,
            reasoning="Agent analyzed request and executed appropriate tools",
            actions_taken=callback_handler.actions_taken,
            result=result,
            next_steps=self._determine_next_steps(result),
            confidence=0.9,
            total_cost=result.get("pricing", {}).get("total")
        )
    
    async def _process_with_langchain(self, request: ServiceRequest, callback_handler) -> Dict[str, Any]:
        """Process using LangChain agent"""
        
        # Format input for agent
        input_text = f"""
        Customer Request: {request.message}
        Customer ID: {request.customer_id or 'unknown'}
        Location: {request.location or 'not specified'}
        Preferred Time: {request.preferred_time or 'flexible'}
        
        Please analyze this request and take appropriate actions to help the customer.
        """
        
        # Execute agent
        response = await self.agent.ainvoke(
            {"input": input_text},
            callbacks=[callback_handler]
        )
        
        return {
            "agent_response": response["output"],
            "tools_used": [action["tool"] for action in callback_handler.actions_taken],
            "analysis_complete": True
        }
    
    async def _process_with_fallback(self, request: ServiceRequest) -> Dict[str, Any]:
        """
        Fallback processing without OpenAI API
        
        Interview Point: Show graceful degradation
        """
        print("🔄 Using fallback processing (no OpenAI API)")
        
        # Manual analysis
        analysis_tool = create_analysis_tool()
        analysis_result = json.loads(analysis_tool.func(request.message))
        
        # Get calendar availability
        calendar_tool = create_calendar_tool()
        calendar_result = json.loads(calendar_tool.func(
            service_type=analysis_result["service_type"],
            urgency=analysis_result["urgency_level"]
        ))
        
        # Get pricing
        pricing_tool = create_pricing_tool()
        pricing_result = json.loads(pricing_tool.func(
            service_type=analysis_result["service_type"],
            additional_services=",".join(analysis_result["additional_services"]),
            urgency=analysis_result["urgency_level"]
        ))
        
        return {
            "analysis": analysis_result,
            "availability": calendar_result,
            "pricing": pricing_result,
            "recommendation": self._generate_recommendation(analysis_result, calendar_result, pricing_result),
            "tools_used": ["analyze_customer_request", "check_calendar_availability", "calculate_service_pricing"]
        }
    
    def _generate_recommendation(self, analysis: Dict, availability: Dict, pricing: Dict) -> str:
        """Generate human-readable recommendation"""
        
        service_type = analysis["service_type"].replace("_", " ").title()
        urgency = analysis["urgency_level"]
        total_cost = pricing["total"]
        earliest_slot = availability["earliest_available"]
        
        recommendation = f"""
        Based on your {service_type.lower()} request with {urgency} priority:
        
        📅 Availability: We can schedule you as early as {earliest_slot}
        💰 Estimated Cost: ${total_cost:.2f}
        
        """
        
        if analysis["additional_services"]:
            services = [s.replace("_", " ").title() for s in analysis["additional_services"]]
            savings = pricing.get("savings", 0)
            recommendation += f"🎁 Bundle Services: {', '.join(services)}\n"
            if savings > 0:
                recommendation += f"💵 Bundle Savings: ${savings:.2f}\n"
        
        recommendation += "\nWould you like to proceed with scheduling this service?"
        
        return recommendation.strip()
    
    async def handle_followup(self, followup: FollowUpRequest) -> AgentResponse:
        """
        Handle follow-up requests
        
        Interview Point: Show conversation continuity and context management
        """
        print(f"🔄 HANDLING FOLLOWUP: {followup.request_id}")
        print(f"Followup Message: '{followup.message}'")
        
        if followup.request_id not in self.active_sessions:
            raise HTTPException(status_code=404, detail="Original request not found")
        
        session = self.active_sessions[followup.request_id]
        session["conversation_history"].append(followup.message)
        
        # Process followup with context
        callback_handler = InterviewCallbackHandler()
        
        if self.agent:
            try:
                # Add followup to conversation
                context = f"""
                Previous conversation:
                {' -> '.join(session['conversation_history'][-3:])}
                
                Current request: {followup.message}
                
                Please handle this followup request, considering the previous context.
                """
                
                response = await self.agent.ainvoke(
                    {"input": context},
                    callbacks=[callback_handler]
                )
                
                result = {
                    "agent_response": response["output"],
                    "context_maintained": True
                }
            except Exception as e:
                print(f"❌ LangChain followup failed: {e}")
                result = await self._handle_followup_fallback(followup, session)
        else:
            result = await self._handle_followup_fallback(followup, session)
        
        session["last_result"] = result
        
        return AgentResponse(
            request_id=followup.request_id,
            reasoning="Processed followup with conversation context",
            actions_taken=callback_handler.actions_taken,
            result=result,
            next_steps=self._determine_next_steps(result),
            confidence=0.85
        )
    
    async def _handle_followup_fallback(self, followup: FollowUpRequest, session: Dict) -> Dict[str, Any]:
        """Handle followup without LangChain"""
        
        # Analyze the followup
        analysis_tool = create_analysis_tool()
        followup_analysis = json.loads(analysis_tool.func(followup.message))
        
        # If it's a bundle request, recalculate pricing
        if any(word in followup.message.lower() for word in ["add", "bundle", "also", "too"]):
            original_analysis = session["last_result"].get("analysis", {})
            
            # Combine services
            all_services = list(set(
                original_analysis.get("additional_services", []) + 
                followup_analysis.get("additional_services", [])
            ))
            
            # Recalculate pricing
            pricing_tool = create_pricing_tool()
            new_pricing = json.loads(pricing_tool.func(
                service_type=original_analysis.get("service_type", "ac_repair"),
                additional_services=",".join(all_services),
                urgency=original_analysis.get("urgency_level", "normal")
            ))
            
            return {
                "followup_analysis": followup_analysis,
                "updated_services": all_services,
                "updated_pricing": new_pricing,
                "recommendation": f"Great! I can add {', '.join(followup_analysis['additional_services'])} to your service. Your updated total is ${new_pricing['total']:.2f} with ${new_pricing['savings']:.2f} in bundle savings!"
            }
        
        return {
            "followup_analysis": followup_analysis,
            "response": "I understand your followup request. Let me help you with that."
        }
    
    def _determine_next_steps(self, result: Dict[str, Any]) -> List[str]:
        """Determine what customer can do next"""
        
        next_steps = []
        
        if "availability" in result:
            next_steps.append("Select preferred appointment time")
        
        if "pricing" in result:
            next_steps.append("Review pricing and confirm service")
        
        if "additional_services" in result.get("analysis", {}):
            next_steps.append("Consider additional services for bundle savings")
        
        if not next_steps:
            next_steps.append("Provide any additional requirements or questions")
        
        return next_steps

# ============================================================================
# FASTAPI APPLICATION - Interview Focus: Production-ready API
# ============================================================================

# Initialize FastAPI app
app = FastAPI(
    title="OnePath Service Dispatch System",
    description="LangChain-powered agent system for home service dispatch",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize orchestrator
orchestrator = OnepathAgentOrchestrator()

# ============================================================================
# API ENDPOINTS - Interview Focus: Clean API design
# ============================================================================

@app.post("/api/v1/service-request", response_model=AgentResponse)
async def create_service_request(request: ServiceRequest):
    """
    Main endpoint for service requests
    
    Interview Strategy: This is your main API demonstration
    """
    try:
        response = await orchestrator.process_service_request(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process request: {str(e)}")

@app.post("/api/v1/followup/{request_id}", response_model=AgentResponse)
async def handle_followup_request(request_id: str, followup: FollowUpRequest):
    """
    Handle follow-up requests
    
    Interview Point: Show conversation continuity
    """
    followup.request_id = request_id
    try:
        response = await orchestrator.handle_followup(followup)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process followup: {str(e)}")

@app.get("/api/v1/session/{request_id}")
async def get_session_info(request_id: str):
    """Get session information"""
    if request_id not in orchestrator.active_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return orchestrator.active_sessions[request_id]

@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "langchain_available": orchestrator.agent is not None,
        "active_sessions": len(orchestrator.active_sessions),
        "tools_available": len(orchestrator.tools)
    }

# ============================================================================
# INTERVIEW DEMO ENDPOINTS - Show different scenarios
# ============================================================================

@app.post("/api/v1/demo/ac-repair")
async def demo_ac_repair():
    """
    Demo endpoint: AC repair scenario
    
    Interview Strategy: Use this to walkthrough main scenario
    """
    demo_request = ServiceRequest(
        message="My AC is broken. Can someone fix it this week?",
        customer_id="demo-001",
        location="123 Main St, Austin TX"
    )
    
    response = await orchestrator.process_service_request(demo_request)
    
    return {
        "scenario": "AC Repair Request",
        "demo_flow": "Customer request → Agent analysis → Tool orchestration → Response",
        "langchain_integration": "LangChain agent with OpenAI function calling",
        "response": response
    }

@app.post("/api/v1/demo/bundle-followup")
async def demo_bundle_followup():
    """
    Demo endpoint: Bundle followup scenario
    
    Interview Focus: Show multi-turn conversation handling
    """
    # First request
    initial_request = ServiceRequest(
        message="My AC is broken. Can someone fix it this week?",
        customer_id="demo-002"
    )
    
    initial_response = await orchestrator.process_service_request(initial_request)
    
    # Followup request
    followup = FollowUpRequest(
        request_id=initial_response.request_id,
        message="Can you add thermostat installation too and bundle it?"
    )
    
    followup_response = await orchestrator.handle_followup(followup)
    
    return {
        "scenario": "Bundle Followup Request",
        "initial_request": initial_response,
        "followup_request": followup_response,
        "conversation_continuity": "Maintained through LangChain memory",
        "business_logic": "Bundle optimization with pricing recalculation"
    }

# ============================================================================
# STARTUP & CONFIGURATION
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize system on startup"""
    print("🚀 OnePath LangChain Agent System Starting...")
    print(f"📊 Tools Available: {len(orchestrator.tools)}")
    print(f"🤖 LangChain Agent: {'✅ Loaded' if orchestrator.agent else '❌ Using Fallback'}")
    print(f"🔗 OpenAI Integration: {'✅ Connected' if orchestrator.openai_api_key else '❌ Mock Mode'}")
    print("✅ System Ready for Interview Demo")

if __name__ == "__main__":
    import uvicorn
    
    print("🎯 OnePath Interview Demo System - LangChain Edition")
    print("=" * 60)
    print()
    print("Features:")
    print("✅ LangChain agent orchestration")
    print("✅ OpenAI function calling integration")
    print("✅ Production-ready FastAPI")
    print("✅ MCP-style multi-step reasoning")
    print("✅ Conversation memory and context")
    print("✅ Error handling and fallbacks")
    print()
    print("Visit http://localhost:8000/docs for API documentation")
    print("Demo endpoints: /demo/ac-repair and /demo/bundle-followup")
    print()
    
    uvicorn.run(
        "langchain_agent_system:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )