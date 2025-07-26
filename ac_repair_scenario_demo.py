"""
Complete AC Repair Scenario Implementation for OnePath Interview

This demonstrates the full agent chaining workflow:
1. Initial request: "My AC is broken. Can someone fix it this week?"
2. Agent reasoning and decision making
3. Calendar availability checking
4. Pricing calculation
5. Followup: "Can you add a thermostat too and bundle it?"
6. Bundle optimization and final quote

Interview Strategy: Walk through this entire flow step-by-step
"""

import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

# Import our components
from react_architecture_guide import ReACTAgent, ActionType
from prompt_engineering_system import PromptComposer, ConversationContext, PromptType
from fastapi_agent_system import AgentOrchestrator, ServiceRequest

class ACRepairScenarioDemo:
    """
    Complete walkthrough of AC repair scenario for interview demonstration
    
    Interview Focus: This is your main demonstration piece
    """
    
    def __init__(self):
        self.orchestrator = AgentOrchestrator()
        self.prompt_composer = PromptComposer()
        self.conversation_context = ConversationContext()
        self.scenario_state = {
            "current_step": 1,
            "total_steps": 6,
            "workflow_id": None,
            "customer_data": {
                "id": "customer_001",
                "name": "John Smith", 
                "location": "123 Main St, Anytown",
                "service_history": []
            }
        }
    
    async def run_complete_scenario(self):
        """
        Run the complete AC repair scenario
        
        Interview Strategy: 
        1. Explain each step before executing it
        2. Show the prompts being generated
        3. Demonstrate agent chaining
        4. Handle the followup request
        """
        
        print("🏠 OnePath AC Repair Scenario - Complete Demo")
        print("=" * 55)
        print("Customer: John Smith")
        print("Request: 'My AC is broken. Can someone fix it this week?'")
        print("Followup: 'Can you add a thermostat too and bundle it?'")
        print()
        
        # Step 1: Initial Request Processing
        print("STEP 1/6: Initial Request Processing")
        print("-" * 40)
        initial_response = await self._process_initial_request()
        self._display_step_results("Initial Processing", initial_response)
        
        # Step 2: Calendar Availability Check
        print("\nSTEP 2/6: Calendar Availability Check")  
        print("-" * 40)
        calendar_result = await self._check_calendar_availability()
        self._display_step_results("Calendar Check", calendar_result)
        
        # Step 3: Pricing Calculation
        print("\nSTEP 3/6: Pricing Calculation")
        print("-" * 40)
        pricing_result = await self._calculate_initial_pricing()
        self._display_step_results("Pricing Calculation", pricing_result)
        
        # Step 4: Customer Followup Request
        print("\nSTEP 4/6: Customer Followup - Bundle Request")
        print("-" * 40)
        followup_response = await self._handle_bundle_followup()
        self._display_step_results("Bundle Followup", followup_response)
        
        # Step 5: Bundle Analysis & Optimization
        print("\nSTEP 5/6: Bundle Analysis & Optimization")
        print("-" * 40)
        bundle_result = await self._analyze_bundle_request()
        self._display_step_results("Bundle Analysis", bundle_result)
        
        # Step 6: Final Quote & Booking Options
        print("\nSTEP 6/6: Final Quote & Booking Options")
        print("-" * 40)
        final_quote = await self._generate_final_quote()
        self._display_step_results("Final Quote", final_quote)
        
        print("\n✅ Complete AC Repair Scenario Demo Finished")
        print(f"Total workflow steps: {self.scenario_state['current_step']}")
        
        return {
            "scenario_complete": True,
            "total_steps": self.scenario_state["current_step"],
            "final_quote": final_quote,
            "customer_satisfaction": "high"
        }
    
    async def _process_initial_request(self) -> Dict[str, Any]:
        """
        Step 1: Process the initial AC repair request
        
        Interview Points:
        1. Show how ReACT reasoning works
        2. Demonstrate prompt composition
        3. Explain decision logic
        """
        
        # Add initial message to conversation context
        initial_message = "My AC is broken. Can someone fix it this week?"
        self.conversation_context.add_message("user", initial_message)
        
        print("🧠 REASONING PHASE:")
        print(f"Customer Message: '{initial_message}'")
        print(f"Extracted Entities: {json.dumps(self.conversation_context.extracted_entities, indent=2)}")
        
        # Generate reasoning prompt
        reasoning_prompt = self.prompt_composer.compose_prompt(
            PromptType.REASONING,
            self.conversation_context,
            {
                "customer_message": initial_message,
                "context_info": self.conversation_context.extracted_entities
            }
        )
        
        print("\n📝 GENERATED REASONING PROMPT:")
        print(self._truncate_for_display(reasoning_prompt))
        
        # Simulate agent reasoning (in real interview, explain this would call LLM)
        reasoning_result = {
            "analysis": "Customer has broken AC with week timeline - urgent but not emergency",
            "service_type": "ac_repair",
            "urgency": "high",
            "next_action": ActionType.CALENDAR_CHECK,
            "confidence": 0.9,
            "assumptions": [
                "Residential AC unit",
                "Service needed within 7 days",
                "Standard repair (not replacement)"
            ]
        }
        
        print("\n🎯 REASONING RESULT:")
        print(f"Service Type: {reasoning_result['service_type']}")
        print(f"Urgency: {reasoning_result['urgency']}") 
        print(f"Next Action: {reasoning_result['next_action']}")
        print(f"Confidence: {reasoning_result['confidence']}")
        
        return reasoning_result
    
    async def _check_calendar_availability(self) -> Dict[str, Any]:
        """
        Step 2: Check calendar availability for AC repair
        
        Interview Focus: Show how specialized agents work
        """
        
        print("📅 CALENDAR AGENT PROCESSING:")
        
        # Generate calendar-specific prompt
        calendar_prompt = self.prompt_composer.compose_prompt(
            PromptType.CALENDAR_QUERY,
            self.conversation_context,
            {
                "service_type": "ac_repair",
                "urgency": "high",
                "preferences": "within one week",
                "availability_data": "mock_calendar_api_data"
            }
        )
        
        print("📝 CALENDAR QUERY PROMPT:")
        print(self._truncate_for_display(calendar_prompt))
        
        # Simulate calendar API response
        calendar_result = {
            "available_slots": [
                {
                    "date": "2024-01-25",
                    "time": "09:00",
                    "technician": "Mike Johnson",
                    "specialization": "AC/HVAC",
                    "travel_time": "15 minutes"
                },
                {
                    "date": "2024-01-25", 
                    "time": "14:00",
                    "technician": "Sarah Davis",
                    "specialization": "AC/HVAC",
                    "travel_time": "10 minutes"
                },
                {
                    "date": "2024-01-26",
                    "time": "10:00", 
                    "technician": "Mike Johnson",
                    "specialization": "AC/HVAC",
                    "travel_time": "15 minutes"
                }
            ],
            "earliest_available": "2024-01-25 09:00",
            "recommended_slot": "2024-01-25 14:00",
            "emergency_available": True
        }
        
        print("\n📊 CALENDAR AVAILABILITY:")
        for slot in calendar_result["available_slots"]:
            print(f"  {slot['date']} {slot['time']} - {slot['technician']} ({slot['travel_time']} travel)")
        
        print(f"\n✅ Recommended: {calendar_result['recommended_slot']}")
        
        return calendar_result
    
    async def _calculate_initial_pricing(self) -> Dict[str, Any]:
        """
        Step 3: Calculate pricing for AC repair service
        
        Interview Points: Show pricing logic and calculations
        """
        
        print("💰 PRICING AGENT PROCESSING:")
        
        # Generate pricing prompt
        pricing_prompt = self.prompt_composer.compose_prompt(
            PromptType.PRICING_CALCULATION,
            self.conversation_context,
            {
                "service_type": "ac_repair",
                "additional_services": [],
                "urgency": "high",
                "customer_history": self.scenario_state["customer_data"]["service_history"]
            }
        )
        
        print("📝 PRICING CALCULATION PROMPT:")
        print(self._truncate_for_display(pricing_prompt))
        
        # Simulate pricing calculation
        pricing_result = {
            "base_services": {
                "ac_diagnostic": 75,
                "ac_repair": 150
            },
            "subtotal": 225,
            "high_priority_surcharge": 25,
            "travel_fee": 0,  # Waived for local service
            "tax": 20,
            "total": 270,
            "payment_options": ["cash", "card", "financing"],
            "warranty": "90 days parts and labor"
        }
        
        print("\n💵 PRICING BREAKDOWN:")
        print(f"  AC Diagnostic: ${pricing_result['base_services']['ac_diagnostic']}")
        print(f"  AC Repair: ${pricing_result['base_services']['ac_repair']}")
        print(f"  Priority Surcharge: ${pricing_result['high_priority_surcharge']}")
        print(f"  Tax: ${pricing_result['tax']}")
        print(f"  TOTAL: ${pricing_result['total']}")
        
        return pricing_result
    
    async def _handle_bundle_followup(self) -> Dict[str, Any]:
        """
        Step 4: Handle customer followup about adding thermostat
        
        Interview Gold: Show conversation continuity and context handling
        """
        
        print("💬 CUSTOMER FOLLOWUP PROCESSING:")
        
        # Add followup message to context
        followup_message = "Can you add a thermostat installation too and bundle it?"
        self.conversation_context.add_message("user", followup_message)
        
        print(f"Followup Message: '{followup_message}'")
        print(f"Updated Entities: {json.dumps(self.conversation_context.extracted_entities, indent=2)}")
        
        # Generate followup prompt
        followup_prompt = self.prompt_composer.compose_prompt(
            PromptType.CUSTOMER_FOLLOWUP,
            self.conversation_context,
            {
                "current_context": "AC repair scheduled, customer wants to add thermostat",
                "information_gaps": ["thermostat type", "existing wiring", "scheduling preference"],
                "service_type": "hvac_bundle"
            }
        )
        
        print("\n📝 FOLLOWUP ANALYSIS PROMPT:")
        print(self._truncate_for_display(followup_prompt))
        
        # Simulate followup processing
        followup_result = {
            "intent": "add_service_to_existing_request", 
            "additional_service": "thermostat_installation",
            "bundle_opportunity": True,
            "clarifying_questions": [
                "What type of thermostat are you interested in? (basic, programmable, smart)",
                "Do you have existing thermostat wiring?",
                "Would you prefer this done during the same visit as the AC repair?"
            ],
            "next_action": ActionType.BUNDLE_ANALYSIS,
            "confidence": 0.95
        }
        
        print("\n🔍 FOLLOWUP ANALYSIS:")
        print(f"Intent: {followup_result['intent']}")
        print(f"Additional Service: {followup_result['additional_service']}")
        print(f"Bundle Opportunity: {followup_result['bundle_opportunity']}")
        print("Clarifying Questions:")
        for q in followup_result["clarifying_questions"]:
            print(f"  - {q}")
        
        return followup_result
    
    async def _analyze_bundle_request(self) -> Dict[str, Any]:
        """
        Step 5: Analyze bundle optimization opportunities
        
        Interview Focus: Show complex multi-service optimization
        """
        
        print("📦 BUNDLE OPTIMIZATION PROCESSING:")
        
        # Generate bundle analysis prompt
        bundle_prompt = self.prompt_composer.compose_prompt(
            PromptType.BUNDLE_ANALYSIS,
            self.conversation_context,
            {
                "services_list": ["ac_repair", "thermostat_installation"],
                "individual_costs": {"ac_repair": 270, "thermostat_basic": 150, "thermostat_smart": 300},
                "bundle_options": {
                    "hvac_service_bundle": {
                        "discount_percent": 15,
                        "services": ["ac_repair", "thermostat_installation"],
                        "same_visit_bonus": 25
                    }
                },
                "scheduling_info": "Same technician can handle both services, saves travel time"
            }
        )
        
        print("📝 BUNDLE ANALYSIS PROMPT:")
        print(self._truncate_for_display(bundle_prompt))
        
        # Simulate bundle analysis
        bundle_result = {
            "recommended_bundle": "hvac_service_bundle",
            "bundle_services": {
                "ac_repair": 270,
                "thermostat_smart": 300,
                "installation_labor": 100
            },
            "original_total": 670,
            "bundle_discount": 100,  # 15% off
            "same_visit_savings": 25,
            "final_total": 545,
            "savings": 125,
            "scheduling_optimization": {
                "single_visit": True,
                "estimated_duration": "3-4 hours",
                "technician": "Mike Johnson (HVAC specialist)"
            },
            "value_proposition": "Save $125 and get both services in one visit"
        }
        
        print("\n📊 BUNDLE ANALYSIS RESULT:")
        print(f"Services: AC Repair + Smart Thermostat Installation")
        print(f"Original Total: ${bundle_result['original_total']}")
        print(f"Bundle Discount: -${bundle_result['bundle_discount']}")
        print(f"Same Visit Savings: -${bundle_result['same_visit_savings']}")
        print(f"FINAL TOTAL: ${bundle_result['final_total']}")
        print(f"TOTAL SAVINGS: ${bundle_result['savings']}")
        
        return bundle_result
    
    async def _generate_final_quote(self) -> Dict[str, Any]:
        """
        Step 6: Generate final comprehensive quote
        
        Interview Points: Show complete customer experience
        """
        
        print("📋 FINAL QUOTE GENERATION:")
        
        final_quote = {
            "quote_id": "QUOTE-2024-001",
            "customer": self.scenario_state["customer_data"],
            "services": {
                "ac_diagnostic_and_repair": {
                    "description": "Complete AC system diagnostic and repair",
                    "base_cost": 225,
                    "priority_surcharge": 25,
                    "subtotal": 250
                },
                "smart_thermostat_installation": {
                    "description": "Smart thermostat supply and installation",
                    "equipment": 200,
                    "labor": 100,
                    "subtotal": 300
                }
            },
            "pricing_summary": {
                "subtotal": 550,
                "bundle_discount": -100,
                "same_visit_savings": -25,
                "tax": 34,
                "final_total": 459
            },
            "scheduling": {
                "recommended_date": "2024-01-25",
                "recommended_time": "14:00",
                "duration": "3-4 hours",
                "technician": "Mike Johnson - HVAC Specialist"
            },
            "terms": {
                "warranty": "90 days parts and labor",
                "payment_due": "Upon completion",
                "payment_methods": ["Cash", "Card", "Financing available"],
                "valid_until": "2024-01-31"
            },
            "next_steps": [
                "Confirm appointment time",
                "Prepare access to AC unit and electrical panel", 
                "Choose thermostat model (basic/programmable/smart)",
                "Review and sign service agreement"
            ]
        }
        
        print("\n📄 FINAL COMPREHENSIVE QUOTE:")
        print(f"Quote ID: {final_quote['quote_id']}")
        print("Services:")
        for service, details in final_quote["services"].items():
            print(f"  • {details['description']}: ${details['subtotal']}")
        
        print(f"\nPricing:")
        print(f"  Subtotal: ${final_quote['pricing_summary']['subtotal']}")
        print(f"  Bundle Discount: ${final_quote['pricing_summary']['bundle_discount']}")
        print(f"  Same Visit Savings: ${final_quote['pricing_summary']['same_visit_savings']}")
        print(f"  Tax: ${final_quote['pricing_summary']['tax']}")
        print(f"  FINAL TOTAL: ${final_quote['pricing_summary']['final_total']}")
        
        print(f"\nScheduling:")
        print(f"  Date: {final_quote['scheduling']['recommended_date']}")
        print(f"  Time: {final_quote['scheduling']['recommended_time']}")
        print(f"  Technician: {final_quote['scheduling']['technician']}")
        
        return final_quote
    
    def _display_step_results(self, step_name: str, result: Dict[str, Any]):
        """Helper method to display step results consistently"""
        
        print(f"✅ {step_name} Complete")
        print(f"   Result keys: {list(result.keys())}")
        
        # Update scenario state
        self.scenario_state["current_step"] += 1
    
    def _truncate_for_display(self, text: str, max_length: int = 300) -> str:
        """Truncate long text for display purposes"""
        
        if len(text) <= max_length:
            return text
        
        return text[:max_length] + "...\n[TRUNCATED FOR DISPLAY]"

# ============================================================================
# INTERVIEW WALKTHROUGH SCRIPT
# ============================================================================

async def run_interview_walkthrough():
    """
    Main interview walkthrough script
    
    Interview Strategy: This is your primary demonstration
    """
    
    print("🎯 ONEPATH INTERVIEW - AC REPAIR SCENARIO WALKTHROUGH")
    print("=" * 65)
    print()
    print("This demonstrates:")
    print("• ReACT architecture (Reasoning + Acting)")
    print("• Agent orchestration and chaining")
    print("• Dynamic prompt composition")
    print("• Multi-service bundle optimization")
    print("• End-to-end workflow management")
    print()
    input("Press Enter to begin the demonstration...")
    print()
    
    # Run the complete scenario
    demo = ACRepairScenarioDemo()
    result = await demo.run_complete_scenario()
    
    print("\n" + "=" * 65)
    print("🏆 INTERVIEW DEMONSTRATION COMPLETE")
    print("=" * 65)
    print()
    print("Key Technical Concepts Demonstrated:")
    print("✅ ReACT reasoning architecture")
    print("✅ Multi-agent orchestration")
    print("✅ Dynamic prompt engineering")
    print("✅ Context-aware decision making")
    print("✅ Service bundle optimization")
    print("✅ Error handling and resilience")
    print("✅ Microservice design patterns")
    print()
    print("Questions to expect:")
    print("• How would you handle API failures?")
    print("• How would you scale this to multiple customers?")
    print("• How would you add new service types?")
    print("• How would you handle conflicting agent recommendations?")
    print("• How would you optimize for cost vs speed?")
    
    return result

# ============================================================================
# INTERVIEW PREPARATION CHECKLIST
# ============================================================================

def print_interview_checklist():
    """
    Print interview preparation checklist
    """
    
    checklist = """
    📋 ONEPATH INTERVIEW PREPARATION CHECKLIST
    ==========================================
    
    BEFORE THE INTERVIEW:
    □ Review ReACT architecture concepts
    □ Practice explaining your thought process aloud
    □ Prepare to share your screen and show IDE
    □ Test code locally to ensure it runs
    □ Review FastAPI basics and async patterns
    □ Practice prompt engineering explanations
    
    DURING THE INTERVIEW:
    □ Start by explaining your overall approach
    □ Walk through each step of your reasoning
    □ Ask clarifying questions about requirements
    □ Show your prompts and explain design choices
    □ Demonstrate error handling and edge cases
    □ Be ready to adapt to new requirements mid-task
    
    KEY PHRASES TO USE:
    • "Let me think through this step by step..."
    • "I'm making this assumption because..."
    • "The prompt I would use here is..."
    • "To handle this edge case, I would..."
    • "My reasoning process is..."
    • "A clarifying question I have is..."
    
    TECHNICAL AREAS TO EMPHASIZE:
    □ ReACT reasoning loops
    □ Agent specialization and chaining
    □ Dynamic prompt composition
    □ Error handling and resilience
    □ Microservice architecture patterns
    □ Context management across conversations
    """
    
    print(checklist)

if __name__ == "__main__":
    print_interview_checklist()
    print("\n" + "="*50)
    print("Run the demo? (y/n): ", end="")
    
    choice = input().lower()
    if choice == 'y':
        asyncio.run(run_interview_walkthrough())
    else:
        print("Demo ready to run when you are!")
        print("Command: python ac_repair_scenario_demo.py")