import uuid
import structlog
from contextlib import asynccontextmanager
from typing import Dict, Any
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import time

from config.settings import settings
from .models import ChatRequest, ChatResponse
from .react_agents import agent
from .agent_orchestrator import chain_orchestrator

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting Onepath AI Orchestration Agent v1.0")
    logger.info("Configuration loaded", 
                debug=settings.debug,
                model=settings.openai_model,
                max_iterations=settings.max_iterations)
    yield
    # Shutdown
    logger.info("Shutting down Onepath AI Orchestration Agent")


app = FastAPI(
    title="Onepath AI Orchestration Agent",
    description="AI-powered customer service orchestration system for home services",
    version="1.0.0",
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
    lifespan=lifespan
)

# Security and CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=["localhost", "127.0.0.1", "*.onepath.ai"]
)


# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    request_id = str(uuid.uuid4())
    
    # Add request ID to context
    with structlog.contextvars.bound_contextvars(request_id=request_id):
        logger.info("Request started",
                   method=request.method,
                   url=str(request.url),
                   client_ip=request.client.host if request.client else None)
        
        try:
            response = await call_next(request)
            process_time = time.time() - start_time
            
            logger.info("Request completed",
                       status_code=response.status_code,
                       process_time=round(process_time, 4))
            
            # Add custom headers
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Process-Time"] = str(round(process_time, 4))
            
            return response
            
        except Exception as e:
            process_time = time.time() - start_time
            logger.error("Request failed",
                        error=str(e),
                        process_time=round(process_time, 4))
            raise


# Health check endpoints
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": time.time()
    }


@app.get("/health/ready")
async def readiness_check():
    # Check if all dependencies are ready
    try:
        # Could add checks for OpenAI API, internal APIs, etc.
        return {
            "status": "ready",
            "checks": {
                "agent": "ready",
                "tools": "ready"
            }
        }
    except Exception as e:
        logger.error("Readiness check failed", error=str(e))
        raise HTTPException(status_code=503, detail="Service not ready")


# Rate limiting dependency (simplified version)
async def rate_limit_check(request: Request):
    # In production, implement proper rate limiting with Redis or similar
    # For now, just log the request
    logger.debug("Rate limit check", client_ip=request.client.host if request.client else None)
    return True


# Main chat endpoint
@app.post("/v1/chat", response_model=ChatResponse)
async def chat_endpoint(
    chat_request: ChatRequest,
    request: Request,
    _: bool = Depends(rate_limit_check)
):
    try:
        logger.info("Chat request received", 
                   query=chat_request.query[:100],  # Log first 100 chars only
                   session_id=chat_request.session_id)
        
        # Validate input
        if not chat_request.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        if len(chat_request.query) > 1000:
            raise HTTPException(status_code=400, detail="Query too long (max 1000 characters)")
        
        # Process the query with the agent
        agent_response = await agent.process_query(
            query=chat_request.query,
            session_id=chat_request.session_id,
            context=chat_request.context
        )
        
        # Convert to API response format
        response = ChatResponse(
            response=agent_response.response,
            session_id=agent_response.conversation_context.session_id,
            intent=agent_response.intent_detected,
            confidence=agent_response.confidence,
            tools_used=agent_response.tools_used
        )
        
        logger.info("Chat response generated",
                   intent=response.intent,
                   confidence=response.confidence,
                   tools_used=response.tools_used,
                   session_id=response.session_id)
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Chat endpoint error", error=str(e), exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Internal server error while processing your request"
        )


# Agent metrics endpoint (for monitoring)
@app.get("/v1/metrics")
async def get_metrics():
    try:
        # In production, return actual metrics
        return {
            "active_conversations": len(agent.conversations),
            "tools_available": len(agent.tool_registry.get_available_tools()),
            "uptime": time.time(),
            "version": "1.0.0"
        }
    except Exception as e:
        logger.error("Metrics endpoint error", error=str(e))
        raise HTTPException(status_code=500, detail="Unable to retrieve metrics")


# Tool information endpoint
@app.get("/v1/tools")
async def get_available_tools():
    try:
        from .tools import tool_registry
        return {
            "available_tools": tool_registry.get_available_tools(),
            "tool_descriptions": tool_registry.get_tool_descriptions()
        }
    except Exception as e:
        logger.error("Tools endpoint error", error=str(e))
        raise HTTPException(status_code=500, detail="Unable to retrieve tool information")


# Enhanced chat endpoint with chain agents
@app.post("/v1/chat/chain", response_model=ChatResponse)
async def chain_chat_endpoint(
    chat_request: ChatRequest,
    request: Request,
    _: bool = Depends(rate_limit_check)
):
    try:
        logger.info("Chain chat request received", 
                   query=chat_request.query[:100],
                   session_id=chat_request.session_id)
        
        # Validate input
        if not chat_request.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        if len(chat_request.query) > 1000:
            raise HTTPException(status_code=400, detail="Query too long (max 1000 characters)")
        
        # Process with chain agents
        response = await chain_orchestrator.process_query(
            query=chat_request.query,
            session_id=chat_request.session_id
        )
        
        logger.info("Chain chat response generated",
                   intent=response.intent,
                   confidence=response.confidence,
                   tools_used=response.tools_used,
                   session_id=response.session_id)
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Chain chat endpoint error", error=str(e), exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Internal server error while processing your request"
        )

# Session management endpoint
@app.delete("/v1/sessions/{session_id}")
async def clear_session(session_id: str):
    try:
        # Clear from both single agent and chain orchestrator
        cleared_single = session_id in agent.conversations
        cleared_chain = chain_orchestrator.clear_session(session_id)
        
        if cleared_single:
            del agent.conversations[session_id]
        
        if cleared_single or cleared_chain:
            logger.info("Session cleared", session_id=session_id)
            return {"status": "success", "message": f"Session {session_id} cleared"}
        else:
            raise HTTPException(status_code=404, detail="Session not found")
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Session clear error", error=str(e), session_id=session_id)
        raise HTTPException(status_code=500, detail="Unable to clear session")


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error("Unhandled exception",
                method=request.method,
                url=str(request.url),
                error=str(exc),
                exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content={
            "detail": "An unexpected error occurred",
            "request_id": request.headers.get("X-Request-ID", "unknown")
        }
    )


# Custom HTTP exception handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.warning("HTTP exception",
                  method=request.method,
                  url=str(request.url),
                  status_code=exc.status_code,
                  detail=exc.detail)
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "request_id": request.headers.get("X-Request-ID", "unknown")
        }
    )
