# 🎯 OnePath.ai Interview Project - LangChain Agent System

**Production-ready service dispatch agent system demonstrating:**
- ✅ LangChain agent orchestration  
- ✅ OpenAI function calling integration
- ✅ MCP-style multi-step reasoning
- ✅ FastAPI microservice architecture
- ✅ Error handling and fallback mechanisms

## 🚀 Quick Start (Interview Demo)

### Prerequisites
```bash
pip install -r requirements.txt
```

### Option 1: With OpenAI API Key (Full Demo)
```bash
# Create .env file
cp .env.example .env
# Add your OpenAI API key to .env

# Run the system
python3 langchain_agent_system.py
```

### Option 2: Without API Key (Mock Mode)
```bash
# System works in fallback mode for demonstration
python3 langchain_agent_system.py
```

### Run Interview Demo Script
```bash
python3 interview_demo_script.py
```

## 🎪 Live Demo Scenarios

### 1. **AC Repair Request**
```bash
curl -X POST "http://localhost:8000/api/v1/demo/ac-repair"
```
**Customer:** "My AC is broken. Can someone fix it this week?"
**Agent:** Analyzes → Checks calendar → Calculates pricing → Responds

### 2. **Bundle Followup**  
```bash
curl -X POST "http://localhost:8000/api/v1/demo/bundle-followup"
```
**Customer:** "Can you add thermostat installation too and bundle it?"
**Agent:** Maintains context → Recalculates with bundle → Optimizes pricing

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   FastAPI       │    │   LangChain      │    │   OpenAI        │
│   REST APIs     │───▶│   Agent          │───▶│   Function      │
│                 │    │   Orchestrator   │    │   Calling       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                        │                       │
         ▼                        ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Business      │    │   Conversation   │    │   Tool          │
│   Logic APIs    │    │   Memory         │    │   Integration   │
│   (Mock)        │    │   Management     │    │   Layer         │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 🔧 Key Technical Components

### **LangChain Integration**
```python
# Agent with custom tools and memory
agent = create_openai_functions_agent(
    llm=ChatOpenAI(model="gpt-4"),
    tools=[analysis_tool, calendar_tool, pricing_tool],
    prompt=custom_prompt_template
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=ConversationBufferWindowMemory(k=10),
    handle_parsing_errors=True
)
```

### **Function Calling Tools**
```python
def create_analysis_tool() -> Tool:
    return Tool(
        name="analyze_customer_request",
        description="Analyze customer service requests for intent and urgency",
        func=analyze_request_function
    )
```

### **Multi-Step Reasoning**
1. **Analyze** customer request (service type, urgency)
2. **Route** to appropriate tools (calendar, pricing)  
3. **Orchestrate** multi-tool workflows
4. **Optimize** business outcomes (bundling, scheduling)

## 🎯 Interview Demonstration Points

### **1. ReACT Architecture**
> "I've implemented ReACT using LangChain's function calling agent. The agent reasons about customer requests, selects appropriate tools, and observes results in a natural conversation flow."

### **2. Tool Orchestration**  
> "The system uses custom LangChain tools that wrap our business logic. The agent intelligently sequences tool calls - always analyzing first, then checking availability or pricing based on customer intent."

### **3. Prompt Engineering**
> "I use dynamic prompt composition with ChatPromptTemplate. The system prompt establishes the agent's role, while MessagesPlaceholder maintains conversation context across multiple turns."

### **4. Production Architecture**
> "Built as a scalable FastAPI microservice with proper error handling, CORS, health checks, and Docker containerization. Ready for deployment to Render, Fly.io, or Kubernetes."

### **5. Error Handling**
> "The system gracefully degrades - if OpenAI API fails, it falls back to mock responses while maintaining all business logic. This ensures reliability in production."

## 📋 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/service-request` | POST | Main service request processing |
| `/api/v1/followup/{id}` | POST | Handle conversation followups |
| `/api/v1/session/{id}` | GET | Get conversation session info |
| `/api/v1/health` | GET | System health check |
| `/api/v1/demo/ac-repair` | POST | AC repair demo scenario |
| `/api/v1/demo/bundle-followup` | POST | Bundle followup demo |

## 🔄 Business Logic Flow

```
Customer Request
     │
     ▼
┌─────────────────┐
│ Request Analysis│ ◄─── "My AC is broken"
│ (AI Tool)       │
└─────────────────┘
     │
     ▼
┌─────────────────┐      ┌─────────────────┐
│ Calendar Check  │      │ Pricing Calc    │
│ (API Tool)      │      │ (Business Tool) │
└─────────────────┘      └─────────────────┘
     │                          │
     └──────────┬─────────────────┘
                ▼
     ┌─────────────────┐
     │ Response        │ ◄─── "Available Thursday 2PM, $275"
     │ Generation      │
     └─────────────────┘
                │
                ▼
     Customer Followup: "Add thermostat too?"
                │
                ▼
     ┌─────────────────┐
     │ Bundle          │ ◄─── Recalculate with bundle discount
     │ Optimization    │
     └─────────────────┘
```

## 🛡️ Production Features

- ✅ **Error Handling**: Graceful degradation with fallback responses
- ✅ **Observability**: Custom callback handlers for monitoring  
- ✅ **Session Management**: Persistent conversation context
- ✅ **Health Checks**: System status monitoring
- ✅ **Docker Ready**: Container deployment configuration
- ✅ **CORS Enabled**: Web client integration
- ✅ **API Documentation**: Auto-generated OpenAPI docs

## 🚀 Deployment Options

### **Local Development**
```bash
uvicorn langchain_agent_system:app --reload
```

### **Docker Container**
```bash
docker build -t onepath-agent .
docker run -p 8000:8000 onepath-agent
```

### **Docker Compose**  
```bash
docker-compose up
```

### **Production Platforms**
- **Render**: One-click deployment with `render.yaml`
- **Fly.io**: Deploy with `fly.toml` configuration
- **Railway**: Git-based deployment
- **Kubernetes**: Production orchestration

## 💡 Interview Talking Points

### **Technical Depth**
- "I chose LangChain because it provides production-grade agent patterns with OpenAI function calling, which is exactly what OnePath needs for autonomous service agents."

### **Business Understanding**  
- "The system prioritizes customer experience - emergency requests get immediate response, bundle opportunities are automatically identified, and pricing is transparent."

### **Scalability Planning**
- "This microservice architecture scales horizontally. We can add specialized agents, integrate with real APIs, and deploy across multiple regions."

### **Production Readiness**
- "I've included error handling, monitoring, containerization, and fallback mechanisms because production systems need reliability, not just functionality."

## 🤔 Questions for Interviewer

1. **"What's OnePath's current agent architecture? How does this approach compare?"**
2. **"Are there specific external APIs (calendar, CRM, pricing) I should integrate with?"**  
3. **"What's the expected scale - concurrent conversations, requests per minute?"**
4. **"How do you currently handle conversation context and customer history?"**
5. **"What's your deployment infrastructure - containers, Kubernetes, cloud platforms?"**

---

## 🏆 Ready for Interview Success!

This system demonstrates:
- ✅ **LangChain expertise** with agent orchestration
- ✅ **OpenAI integration** with function calling  
- ✅ **Production architecture** with FastAPI
- ✅ **Business logic** understanding
- ✅ **Error handling** and reliability
- ✅ **Scalable design** patterns

**You're prepared to show world-class AI engineering skills!** 🚀