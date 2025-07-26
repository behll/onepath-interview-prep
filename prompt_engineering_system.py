"""
Dynamic Prompt Engineering System for OnePath Interview

Key Interview Points:
1. Show how prompts adapt to conversation context
2. Demonstrate prompt chaining and composition  
3. Explain prompt optimization techniques
4. Handle edge cases and error recovery
"""

from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
from dataclasses import dataclass, field
import json
import re
from datetime import datetime

class PromptType(Enum):
    REASONING = "reasoning"
    CALENDAR_QUERY = "calendar_query"
    PRICING_CALCULATION = "pricing_calculation"
    CUSTOMER_FOLLOWUP = "customer_followup"
    BUNDLE_ANALYSIS = "bundle_analysis"
    URGENCY_ASSESSMENT = "urgency_assessment"

class ConversationContext:
    """
    Maintains conversation context for dynamic prompt generation
    
    Interview Tip: Always explain how context shapes your prompts
    """
    
    def __init__(self):
        self.messages = []
        self.extracted_entities = {}
        self.customer_preferences = {}
        self.service_history = []
        self.current_intent = None
        self.confidence_scores = {}
        
    def add_message(self, role: str, content: str, metadata: Dict = None):
        """Add message to conversation context"""
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        self.messages.append(message)
        
        # Update extracted entities
        if role == "user":
            self._extract_entities_from_message(content)
    
    def _extract_entities_from_message(self, message: str):
        """
        Extract entities from user message
        
        Interview Strategy: Show how you identify key information
        """
        message_lower = message.lower()
        
        # Service type extraction
        service_keywords = {
            "ac": ["ac", "air conditioning", "cooling", "hvac"],
            "heating": ["heat", "heating", "furnace", "boiler"],
            "plumbing": ["plumb", "water", "leak", "pipe", "drain"],
            "electrical": ["electric", "power", "outlet", "wiring"]
        }
        
        for service, keywords in service_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                self.extracted_entities["service_type"] = service
                break
        
        # Urgency extraction
        urgency_keywords = {
            "emergency": ["emergency", "urgent", "asap", "immediately", "broken", "not working"],
            "soon": ["this week", "soon", "quickly", "today", "tomorrow"],
            "flexible": ["whenever", "no rush", "flexible", "convenient"]
        }
        
        for urgency, keywords in urgency_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                self.extracted_entities["urgency"] = urgency
                break
        
        # Location hints
        location_keywords = ["house", "home", "office", "building", "apartment", "condo"]
        for keyword in location_keywords:
            if keyword in message_lower:
                self.extracted_entities["location_type"] = keyword
                break
        
        # Bundle/addition requests
        if any(word in message_lower for word in ["add", "also", "too", "bundle", "package"]):
            self.extracted_entities["bundle_request"] = True

class PromptComposer:
    """
    Dynamic prompt composition engine
    
    Interview Focus: This is the core of your prompt engineering demonstration
    """
    
    def __init__(self):
        self.base_prompts = self._initialize_base_prompts()
        self.prompt_modifiers = self._initialize_prompt_modifiers()
        self.context_adapters = self._initialize_context_adapters()
    
    def compose_prompt(self, 
                      prompt_type: PromptType, 
                      context: ConversationContext,
                      specific_params: Dict = None) -> str:
        """
        Main method for dynamic prompt composition
        
        Interview Strategy: 
        1. Explain your composition logic step by step
        2. Show how context influences prompt structure
        3. Demonstrate handling of edge cases
        """
        
        # Start with base prompt
        base_prompt = self.base_prompts[prompt_type]
        
        # Apply context-specific modifications
        modified_prompt = self._apply_context_modifications(
            base_prompt, 
            prompt_type, 
            context
        )
        
        # Add specific parameters
        if specific_params:
            modified_prompt = self._inject_parameters(modified_prompt, specific_params)
        
        # Apply final optimizations
        optimized_prompt = self._optimize_prompt(modified_prompt, context)
        
        return optimized_prompt
    
    def _initialize_base_prompts(self) -> Dict[PromptType, str]:
        """
        Initialize base prompt templates
        
        Interview Tip: Explain why each template is structured this way
        """
        return {
            PromptType.REASONING: """
You are a service dispatch reasoning agent. Analyze the customer request and determine the best action.

Customer Request: {customer_message}
Context: {context_info}

Reasoning Framework:
1. UNDERSTAND: What is the customer really asking for?
2. CATEGORIZE: What type of service is needed? (AC, heating, plumbing, electrical)  
3. PRIORITIZE: What's the urgency level? (emergency, soon, flexible)
4. DECIDE: What action should be taken next?

Available Actions:
- CALENDAR_CHECK: Check technician availability  
- PRICING_QUERY: Get service pricing information
- CUSTOMER_FOLLOWUP: Ask clarifying questions
- BUNDLE_ANALYSIS: Analyze multi-service requests

Analysis:
""",

            PromptType.CALENDAR_QUERY: """
You are a calendar management agent. Find optimal appointment slots based on customer needs.

Service Required: {service_type}
Urgency Level: {urgency}
Customer Preferences: {preferences}
Current Availability: {availability_data}

Consider:
1. Service duration requirements
2. Technician specialization
3. Customer urgency
4. Geographic optimization
5. Emergency surcharge implications

Optimal Slots:
""",

            PromptType.PRICING_CALCULATION: """
You are a pricing calculation agent. Calculate accurate service costs including all relevant factors.

Base Service: {service_type}
Additional Services: {additional_services}
Urgency Level: {urgency}
Customer History: {customer_history}

Pricing Factors:
1. Base service cost
2. Additional services
3. Bundle discounts
4. Emergency surcharges  
5. Customer loyalty discounts
6. Geographic cost adjustments

Total Calculation:
""",

            PromptType.CUSTOMER_FOLLOWUP: """
You are a customer communication agent. Generate helpful followup questions to clarify service needs.

Current Understanding: {current_context}
Missing Information: {information_gaps}
Service Type: {service_type}

Generate questions that are:
1. Specific and actionable
2. Relevant to service delivery
3. Easy for customer to answer
4. Focused on critical details

Questions:
""",

            PromptType.BUNDLE_ANALYSIS: """
You are a bundle optimization agent. Analyze multi-service requests and optimize pricing and scheduling.

Services Requested: {services_list}
Individual Pricing: {individual_costs}
Available Bundles: {bundle_options}
Scheduling Constraints: {scheduling_info}

Optimization Goals:
1. Maximize customer value
2. Optimize technician routing
3. Minimize total service time
4. Apply appropriate discounts

Recommended Bundle:
""",

            PromptType.URGENCY_ASSESSMENT: """
You are an urgency assessment agent. Evaluate the true urgency of service requests.

Customer Message: {customer_message}
Service Type: {service_type}
Context Clues: {context_clues}

Urgency Assessment Criteria:
1. Safety implications
2. Property damage risk
3. Customer comfort impact
4. Seasonal factors
5. System functionality

Urgency Level: [EMERGENCY/HIGH/MEDIUM/LOW]
Reasoning:
"""
        }
    
    def _initialize_prompt_modifiers(self) -> Dict[str, str]:
        """
        Initialize prompt modification templates
        
        Interview Point: Show how prompts adapt to different scenarios
        """
        return {
            "emergency_modifier": """
EMERGENCY PROTOCOL ACTIVE:
- Prioritize immediate response
- Consider after-hours availability  
- Apply emergency surcharge
- Ensure safety protocols
""",
            
            "bundle_modifier": """
BUNDLE OPTIMIZATION ACTIVE:
- Look for service combinations
- Calculate bundle discounts
- Optimize technician routing
- Consider scheduling efficiency
""",
            
            "repeat_customer_modifier": """
RETURNING CUSTOMER DETECTED:
- Reference service history: {service_history}
- Apply loyalty discounts
- Consider previous preferences
- Leverage existing relationship
""",
            
            "complex_request_modifier": """
COMPLEX REQUEST DETECTED:
- Break down into sub-components
- Identify dependencies
- Plan multi-step workflow
- Consider resource allocation
"""
        }
    
    def _initialize_context_adapters(self) -> Dict[str, callable]:
        """
        Initialize context adaptation functions
        
        Interview Gold: Show sophisticated context handling
        """
        return {
            "time_sensitive": self._adapt_for_time_sensitivity,
            "multi_service": self._adapt_for_multi_service,  
            "customer_history": self._adapt_for_customer_history,
            "geographic": self._adapt_for_geographic_factors
        }
    
    def _apply_context_modifications(self, 
                                   base_prompt: str, 
                                   prompt_type: PromptType,
                                   context: ConversationContext) -> str:
        """
        Apply context-specific modifications to base prompt
        
        Interview Strategy: Walk through each modification and explain why
        """
        
        modified_prompt = base_prompt
        
        # Emergency handling
        if context.extracted_entities.get("urgency") == "emergency":
            modified_prompt = self.prompt_modifiers["emergency_modifier"] + modified_prompt
        
        # Bundle request handling
        if context.extracted_entities.get("bundle_request"):
            modified_prompt = modified_prompt + self.prompt_modifiers["bundle_modifier"]
        
        # Customer history integration
        if context.service_history:
            history_modifier = self.prompt_modifiers["repeat_customer_modifier"].format(
                service_history=json.dumps(context.service_history, indent=2)
            )
            modified_prompt = history_modifier + modified_prompt
        
        # Complex request handling
        if len(context.messages) > 3:  # Multi-turn conversation
            modified_prompt = modified_prompt + self.prompt_modifiers["complex_request_modifier"]
        
        return modified_prompt
    
    def _inject_parameters(self, prompt: str, params: Dict) -> str:
        """
        Inject specific parameters into prompt template
        
        Interview Tip: Show parameter validation and error handling
        """
        try:
            # Replace all parameter placeholders
            for key, value in params.items():
                placeholder = "{" + key + "}"
                if placeholder in prompt:
                    # Handle different value types appropriately
                    if isinstance(value, (dict, list)):
                        formatted_value = json.dumps(value, indent=2)
                    else:
                        formatted_value = str(value)
                    
                    prompt = prompt.replace(placeholder, formatted_value)
            
            # Check for unfilled placeholders
            remaining_placeholders = re.findall(r'\{(\w+)\}', prompt)
            if remaining_placeholders:
                # Fill with default values or mark as missing
                for placeholder in remaining_placeholders:
                    prompt = prompt.replace(
                        "{" + placeholder + "}", 
                        f"[MISSING: {placeholder}]"
                    )
            
            return prompt
            
        except Exception as e:
            # Error handling for prompt injection
            return f"ERROR: Failed to inject parameters - {str(e)}\n\nOriginal prompt:\n{prompt}"
    
    def _optimize_prompt(self, prompt: str, context: ConversationContext) -> str:
        """
        Final prompt optimizations
        
        Interview Focus: Show attention to prompt quality and efficiency
        """
        
        # Remove excessive whitespace
        optimized = re.sub(r'\n\s*\n\s*\n', '\n\n', prompt)
        
        # Add conversation context summary if relevant
        if len(context.messages) > 1:
            context_summary = self._generate_context_summary(context)
            optimized = f"Conversation Context:\n{context_summary}\n\n{optimized}"
        
        # Add confidence tracking instruction
        optimized += """\n\nPlease provide your confidence level (0.0-1.0) and explain your reasoning."""
        
        return optimized.strip()
    
    def _generate_context_summary(self, context: ConversationContext) -> str:
        """Generate concise conversation context summary"""
        
        summary_parts = []
        
        # Service type
        if "service_type" in context.extracted_entities:
            summary_parts.append(f"Service: {context.extracted_entities['service_type']}")
        
        # Urgency
        if "urgency" in context.extracted_entities:
            summary_parts.append(f"Urgency: {context.extracted_entities['urgency']}")
        
        # Bundle request  
        if context.extracted_entities.get("bundle_request"):
            summary_parts.append("Bundle/Additional services requested")
        
        # Turn count
        summary_parts.append(f"Conversation turns: {len(context.messages)}")
        
        return " | ".join(summary_parts)
    
    def _adapt_for_time_sensitivity(self, prompt: str, context: ConversationContext) -> str:
        """Adapt prompt for time-sensitive requests"""
        if context.extracted_entities.get("urgency") in ["emergency", "soon"]:
            return f"TIME SENSITIVE REQUEST - PRIORITIZE SPEED\n\n{prompt}"
        return prompt
    
    def _adapt_for_multi_service(self, prompt: str, context: ConversationContext) -> str:
        """Adapt prompt for multi-service requests"""
        if context.extracted_entities.get("bundle_request"):
            return f"{prompt}\n\nMULTI-SERVICE OPTIMIZATION: Consider service bundling, technician efficiency, and cost optimization."
        return prompt
    
    def _adapt_for_customer_history(self, prompt: str, context: ConversationContext) -> str:
        """Adapt prompt based on customer history"""
        if context.service_history:
            history_context = json.dumps(context.service_history, indent=2)
            return f"CUSTOMER HISTORY AVAILABLE:\n{history_context}\n\n{prompt}"
        return prompt
    
    def _adapt_for_geographic_factors(self, prompt: str, context: ConversationContext) -> str:
        """Adapt prompt for geographic considerations"""
        location_type = context.extracted_entities.get("location_type")
        if location_type:
            return f"{prompt}\n\nGEOGRAPHIC CONTEXT: Service location type: {location_type}"
        return prompt

# ============================================================================
# INTERVIEW DEMONSTRATION CLASS
# ============================================================================

class InterviewPromptDemo:
    """
    Demonstration class for interview scenarios
    
    Interview Strategy: Use this to walk through different prompt scenarios
    """
    
    def __init__(self):
        self.composer = PromptComposer()
        
    def demo_basic_ac_request(self):
        """Demo: Basic AC repair request"""
        
        print("=== DEMO: Basic AC Repair Request ===\n")
        
        # Create context
        context = ConversationContext()
        context.add_message("user", "My AC is broken. Can someone fix it this week?")
        
        # Generate reasoning prompt
        reasoning_prompt = self.composer.compose_prompt(
            PromptType.REASONING,
            context,
            {
                "customer_message": "My AC is broken. Can someone fix it this week?",
                "context_info": json.dumps(context.extracted_entities, indent=2)
            }
        )
        
        print("GENERATED REASONING PROMPT:")
        print("-" * 50)
        print(reasoning_prompt)
        print("\n")
        
        return reasoning_prompt
    
    def demo_bundle_request(self):
        """Demo: Bundle service request with followup"""
        
        print("=== DEMO: Bundle Service Request ===\n")
        
        # Create conversation context
        context = ConversationContext()
        context.add_message("user", "My AC is broken. Can someone fix it this week?")
        context.add_message("assistant", "I can help schedule AC repair. We have availability this week.")
        context.add_message("user", "Can you add thermostat installation too and bundle it?")
        
        # Generate bundle analysis prompt
        bundle_prompt = self.composer.compose_prompt(
            PromptType.BUNDLE_ANALYSIS,
            context,
            {
                "services_list": ["AC repair", "thermostat installation"],
                "individual_costs": {"ac_repair": 150, "thermostat_install": 200},
                "bundle_options": {"hvac_bundle": {"discount": 0.15, "services": ["ac_repair", "thermostat_install"]}},
                "scheduling_info": "Same technician can handle both services in single visit"
            }
        )
        
        print("GENERATED BUNDLE ANALYSIS PROMPT:")
        print("-" * 50)
        print(bundle_prompt)
        print("\n")
        
        return bundle_prompt
    
    def demo_emergency_request(self):
        """Demo: Emergency service request"""
        
        print("=== DEMO: Emergency Service Request ===\n")
        
        context = ConversationContext()
        context.add_message("user", "URGENT: My AC just broke and it's 95 degrees outside. I need someone NOW!")
        
        # Generate urgency assessment prompt
        urgency_prompt = self.composer.compose_prompt(
            PromptType.URGENCY_ASSESSMENT,
            context,
            {
                "customer_message": "URGENT: My AC just broke and it's 95 degrees outside. I need someone NOW!",
                "service_type": "ac",
                "context_clues": "High temperature, urgent language, immediate need expressed"
            }
        )
        
        print("GENERATED URGENCY ASSESSMENT PROMPT:")
        print("-" * 50) 
        print(urgency_prompt)
        print("\n")
        
        return urgency_prompt

# ============================================================================
# INTERVIEW PREP UTILITIES
# ============================================================================

def run_interview_demo():
    """
    Run complete interview demonstration
    
    Interview Strategy: Use this as your main demo script
    """
    
    print("🎯 OnePath Interview - Prompt Engineering Demonstration")
    print("=" * 60)
    
    demo = InterviewPromptDemo()
    
    # Demo 1: Basic request
    demo.demo_basic_ac_request()
    
    # Demo 2: Bundle request
    demo.demo_bundle_request()
    
    # Demo 3: Emergency request
    demo.demo_emergency_request()
    
    print("✅ Prompt Engineering Demo Complete")
    print("\nKey Interview Points Demonstrated:")
    print("- Dynamic prompt composition based on context")
    print("- Context-aware modifications and optimizations")
    print("- Parameter injection and error handling")
    print("- Multi-turn conversation handling")
    print("- Emergency and bundle request specialization")

if __name__ == "__main__":
    run_interview_demo()