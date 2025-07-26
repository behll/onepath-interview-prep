"""
ReACT Architecture Guide for OnePath Interview

ReACT = Reasoning + Acting
Core Pattern: Thought → Action → Observation → Thought → Action...

Key Components:
1. Agent Reasoning: Analyze situation and plan next steps
2. Action Execution: Call tools/APIs/functions 
3. Observation: Process results and update understanding
4. Loop: Continue until goal achieved
"""

from typing import Dict, List, Optional, Any
from enum import Enum
import json

class ActionType(Enum):
    REASON = "reason"
    CALENDAR_CHECK = "calendar_check" 
    PRICING_QUERY = "pricing_query"
    DISPATCH_SCHEDULE = "dispatch_schedule"
    CUSTOMER_FOLLOWUP = "customer_followup"

class ReACTAgent:
    """
    Core ReACT agent for service dispatch workflows
    """
    
    def __init__(self, name: str):
        self.name = name
        self.conversation_history = []
        self.current_context = {}
        
    def reason(self, situation: str, context: Dict) -> Dict[str, Any]:
        """
        Core reasoning step - analyze situation and decide next action
        
        Interview Tip: Always explain your reasoning process aloud:
        "I'm analyzing the customer request to determine if this is a scheduling 
         question or a pricing question..."
        """
        
        reasoning_prompt = f"""
        Situation: {situation}
        Context: {json.dumps(context, indent=2)}
        
        Analyze:
        1. What is the customer really asking for?
        2. What information do I need to gather?
        3. Which action should I take next?
        4. What are potential edge cases?
        
        Decision Logic:
        - If asking about timing/availability → CALENDAR_CHECK
        - If asking about cost/pricing → PRICING_QUERY  
        - If ready to book → DISPATCH_SCHEDULE
        - If need clarification → CUSTOMER_FOLLOWUP
        """
        
        # This is where you'd call an LLM in real implementation
        # For interview, explain your reasoning process clearly
        
        return {
            "reasoning": reasoning_prompt,
            "next_action": self._determine_action(situation, context),
            "confidence": 0.85,
            "assumptions": self._identify_assumptions(situation)
        }
    
    def _determine_action(self, situation: str, context: Dict) -> ActionType:
        """
        Decision logic for next action
        
        Interview Strategy: Walk through your decision tree:
        "The customer said 'broken AC this week', so I need to check:
         1. Is this urgent? (broken = urgent)
         2. Timeline specified? (this week = yes) 
         3. Next step: Check calendar availability for urgent AC repair"
        """
        
        situation_lower = situation.lower()
        
        # Emergency/urgent keywords
        if any(word in situation_lower for word in ['broken', 'emergency', 'urgent', 'not working']):
            if any(word in situation_lower for word in ['week', 'today', 'tomorrow', 'asap']):
                return ActionType.CALENDAR_CHECK
        
        # Pricing keywords  
        if any(word in situation_lower for word in ['cost', 'price', 'how much', 'quote', 'estimate']):
            return ActionType.PRICING_QUERY
            
        # Bundle/add-on requests
        if any(word in situation_lower for word in ['add', 'bundle', 'also', 'too']):
            return ActionType.PRICING_QUERY
            
        # Default to customer followup for clarification
        return ActionType.CUSTOMER_FOLLOWUP
    
    def _identify_assumptions(self, situation: str) -> List[str]:
        """
        Interview Gold: Always identify and state your assumptions
        """
        assumptions = []
        
        if 'broken' in situation.lower():
            assumptions.append("Assuming this is urgent/high priority repair")
            
        if 'this week' in situation.lower():
            assumptions.append("Customer wants service within 7 days")
            
        if 'AC' in situation:
            assumptions.append("Air conditioning repair - likely residential")
            
        return assumptions

    def execute_action(self, action_type: ActionType, params: Dict) -> Dict[str, Any]:
        """
        Execute the chosen action and return observations
        
        Interview Tip: Explain what each action would do in real system:
        "In production, this would call our calendar microservice API..."
        """
        
        if action_type == ActionType.CALENDAR_CHECK:
            return self._check_calendar_availability(params)
        elif action_type == ActionType.PRICING_QUERY:
            return self._get_pricing_info(params)  
        elif action_type == ActionType.DISPATCH_SCHEDULE:
            return self._schedule_dispatch(params)
        elif action_type == ActionType.CUSTOMER_FOLLOWUP:
            return self._generate_followup_questions(params)
        
        return {"error": "Unknown action type"}
    
    def _check_calendar_availability(self, params: Dict) -> Dict[str, Any]:
        """Mock calendar API call"""
        # Interview: Explain this would integrate with real calendar system
        return {
            "available_slots": [
                {"date": "2024-01-25", "time": "09:00", "technician": "John"},
                {"date": "2024-01-25", "time": "14:00", "technician": "Sarah"},
                {"date": "2024-01-26", "time": "10:00", "technician": "Mike"}
            ],
            "emergency_available": True,
            "earliest_slot": "2024-01-25 09:00"
        }
    
    def _get_pricing_info(self, params: Dict) -> Dict[str, Any]:
        """Mock pricing API call"""
        return {
            "base_service": {"ac_repair": 150, "diagnostic": 75},
            "additional_services": {"thermostat_install": 200, "filter_change": 25},
            "bundle_discount": 0.1,
            "emergency_surcharge": 50
        }
    
    def _schedule_dispatch(self, params: Dict) -> Dict[str, Any]:
        """Mock dispatch scheduling"""
        return {
            "booking_id": "BK-2024-001",
            "scheduled_time": params.get("selected_time"),
            "technician": params.get("technician"),
            "estimated_duration": "2-3 hours",
            "status": "confirmed"
        }
    
    def _generate_followup_questions(self, params: Dict) -> Dict[str, Any]:
        """Generate clarifying questions for customer"""
        return {  
            "questions": [
                "What type of AC system do you have? (central, window unit, etc.)",
                "When did you first notice the problem?",
                "Is this affecting the whole house or just certain rooms?",
                "Do you need same-day service or is within the week okay?"
            ],
            "intent": "gather_more_context"
        }

# Interview Demo Script
def demonstrate_react_cycle():
    """
    Show complete ReACT cycle for interview
    
    Interview Strategy:
    1. Start with this demo
    2. Walk through each step clearly  
    3. Explain your reasoning at each stage
    4. Show how you handle different scenarios
    """
    
    agent = ReACTAgent("ServiceDispatchAgent")
    
    # Initial customer request
    customer_request = "My AC is broken. Can someone fix it this week?"
    
    print("=== ReACT Cycle Demonstration ===")
    print(f"Customer Request: {customer_request}")
    print()
    
    # Step 1: Reasoning
    print("STEP 1: REASONING")
    reasoning_result = agent.reason(customer_request, {})
    print(f"Next Action: {reasoning_result['next_action']}")
    print(f"Assumptions: {reasoning_result['assumptions']}")
    print()
    
    # Step 2: Action  
    print("STEP 2: ACTION")
    action_result = agent.execute_action(reasoning_result['next_action'], {})
    print(f"Action Result: {json.dumps(action_result, indent=2)}")
    print()
    
    # Step 3: Observation & Next Reasoning
    print("STEP 3: OBSERVATION & NEXT CYCLE")
    followup_context = {
        "availability": action_result,
        "customer_needs": "urgent_ac_repair",
        "timeline": "this_week"
    }
    
    next_reasoning = agent.reason("Customer saw availability, needs to choose slot", followup_context)
    print(f"Next Action: {next_reasoning['next_action']}")

if __name__ == "__main__":
    demonstrate_react_cycle()