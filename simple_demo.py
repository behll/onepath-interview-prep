"""
OnePath Interview Demo - Simplified Version (No Dependencies)
===========================================================

Bu versiyon herhangi bir kütüphane gerektirmeden çalışır.
Interview sırasında sisteminizi göstermek için kullanabilirsiniz.
"""

import json
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

class SimpleAgentDemo:
    """
    Simplified agent demo for interview without external dependencies
    
    Interview Strategy: Show your understanding of agent patterns
    """
    
    def __init__(self):
        self.conversation_history = []
        self.active_sessions = {}
        
    def analyze_customer_request(self, message: str) -> Dict[str, Any]:
        """
        Analyze customer request (ReACT: Reasoning step)
        
        Interview Point: Show business logic understanding
        """
        
        print("🧠 ANALYZING CUSTOMER REQUEST...")
        print(f"Input: '{message}'")
        
        message_lower = message.lower()
        
        # Service type detection
        service_type = "ac_repair"  # default
        if any(word in message_lower for word in ["ac", "air conditioning", "cooling"]):
            service_type = "ac_repair"
        elif any(word in message_lower for word in ["heat", "heating", "furnace"]):
            service_type = "heating"
        elif any(word in message_lower for word in ["plumb", "water", "leak"]):
            service_type = "plumbing"
        elif any(word in message_lower for word in ["electric", "power", "outlet"]):
            service_type = "electrical"
        
        # Urgency detection
        urgency = "normal"
        if any(word in message_lower for word in ["emergency", "urgent", "asap", "broken"]):
            urgency = "emergency"
        elif any(word in message_lower for word in ["this week", "soon", "today"]):
            urgency = "high"
        elif any(word in message_lower for word in ["whenever", "flexible"]):
            urgency = "low"
        
        # Additional services
        additional_services = []
        if "thermostat" in message_lower:
            additional_services.append("thermostat_install")
        if "filter" in message_lower:
            additional_services.append("filter_replacement")
        
        analysis = {
            "service_type": service_type,
            "urgency": urgency,
            "additional_services": additional_services,
            "requires_scheduling": any(word in message_lower for word in ["week", "today", "tomorrow"]),
            "requires_pricing": any(word in message_lower for word in ["cost", "price", "how much"]),
            "bundle_request": any(word in message_lower for word in ["add", "bundle", "also", "too"])
        }
        
        print(f"📊 Analysis Result: {json.dumps(analysis, indent=2)}")
        return analysis
    
    def check_calendar_availability(self, service_type: str, urgency: str) -> Dict[str, Any]:
        """
        Check calendar availability (ReACT: Action step)
        
        Interview Point: Show external API integration patterns
        """
        
        print("📅 CHECKING CALENDAR AVAILABILITY...")
        print(f"Service: {service_type}, Urgency: {urgency}")
        
        # Mock calendar data
        base_date = datetime.now() + timedelta(days=1)
        
        if urgency == "emergency":
            slots = [
                {
                    "datetime": base_date.strftime("%Y-%m-%d %H:%M"),
                    "technician": "Emergency Tech Mike",
                    "duration": "2-3 hours",
                    "surcharge": 75
                }
            ]
        else:
            slots = [
                {
                    "datetime": (base_date + timedelta(days=i)).strftime("%Y-%m-%d %H:%M"),
                    "technician": f"Tech {['Sarah', 'John', 'Mike'][i]}",
                    "duration": "2-3 hours",
                    "surcharge": 0
                }
                for i in range(3)
            ]
        
        availability = {
            "available_slots": slots,
            "earliest_available": slots[0]["datetime"],
            "emergency_available": urgency == "emergency"
        }
        
        print(f"📊 Availability: {len(slots)} slots found")
        for slot in slots[:2]:  # Show first 2
            print(f"  - {slot['datetime']} with {slot['technician']}")
        
        return availability
    
    def calculate_pricing(self, service_type: str, additional_services: List[str], urgency: str) -> Dict[str, Any]:
        """
        Calculate service pricing (ReACT: Action step)
        
        Interview Point: Show business logic complexity
        """
        
        print("💰 CALCULATING PRICING...")
        print(f"Service: {service_type}, Add-ons: {additional_services}, Urgency: {urgency}")
        
        # Base pricing
        base_prices = {
            "ac_repair": 150,
            "heating": 175,
            "plumbing": 125,
            "electrical": 200
        }
        
        addon_prices = {
            "thermostat_install": 200,
            "filter_replacement": 25,
            "duct_cleaning": 300
        }
        
        base_cost = base_prices.get(service_type, 150)
        addon_cost = sum(addon_prices.get(service, 0) for service in additional_services)
        subtotal = base_cost + addon_cost
        
        # Bundle discount
        bundle_discount = 0.15 if additional_services else 0
        discount_amount = subtotal * bundle_discount
        
        # Urgency surcharge
        urgency_surcharge = {"emergency": 75, "high": 25}.get(urgency, 0)
        
        total = subtotal - discount_amount + urgency_surcharge
        tax = total * 0.08
        final_total = total + tax
        
        pricing = {
            "base_cost": base_cost,
            "addon_cost": addon_cost,
            "subtotal": subtotal,
            "bundle_discount": discount_amount,
            "urgency_surcharge": urgency_surcharge,
            "tax": tax,
            "total": final_total,
            "savings": discount_amount
        }
        
        print(f"💵 Pricing Breakdown:")
        print(f"  Base: ${base_cost}, Add-ons: ${addon_cost}")
        print(f"  Bundle Discount: ${discount_amount:.2f}")
        print(f"  Total: ${final_total:.2f}")
        
        return pricing
    
    def process_service_request(self, message: str, customer_id: str = "demo-001") -> Dict[str, Any]:
        """
        Main ReACT processing loop
        
        Interview Strategy: This is your core demonstration
        """
        
        print("🎯 PROCESSING SERVICE REQUEST")
        print("=" * 50)
        print(f"Customer ID: {customer_id}")
        print(f"Message: '{message}'")
        print()
        
        # Step 1: Reasoning - Analyze the request
        print("STEP 1: REASONING (Analysis)")
        print("-" * 30)
        analysis = self.analyze_customer_request(message)
        print()
        
        # Step 2: Action - Check calendar if scheduling needed
        if analysis["requires_scheduling"]:
            print("STEP 2: ACTION (Calendar Check)")
            print("-" * 30)
            availability = self.check_calendar_availability(
                analysis["service_type"], 
                analysis["urgency"]
            )
            print()
        else:
            availability = None
        
        # Step 3: Action - Calculate pricing if needed
        if analysis["requires_pricing"] or availability:
            print("STEP 3: ACTION (Pricing Calculation)")
            print("-" * 30)
            pricing = self.calculate_pricing(
                analysis["service_type"],
                analysis["additional_services"],
                analysis["urgency"]
            )
            print()
        else:
            pricing = None
        
        # Step 4: Observation - Generate response
        print("STEP 4: OBSERVATION (Response Generation)")
        print("-" * 30)
        response = self.generate_response(analysis, availability, pricing)
        print(f"📝 Generated Response:")
        print(response)
        print()
        
        # Store session for followups
        request_id = f"req_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.active_sessions[request_id] = {
            "analysis": analysis,
            "availability": availability,
            "pricing": pricing,
            "conversation": [message]
        }
        
        return {
            "request_id": request_id,
            "analysis": analysis,
            "availability": availability,
            "pricing": pricing,
            "response": response,
            "next_steps": self.determine_next_steps(analysis, availability, pricing)
        }
    
    def handle_followup(self, request_id: str, followup_message: str) -> Dict[str, Any]:
        """
        Handle followup requests with conversation context
        
        Interview Point: Show conversation continuity
        """
        
        print("🔄 HANDLING FOLLOWUP REQUEST")
        print("=" * 50)
        print(f"Request ID: {request_id}")
        print(f"Followup: '{followup_message}'")
        print()
        
        if request_id not in self.active_sessions:
            return {"error": "Session not found"}
        
        session = self.active_sessions[request_id]
        session["conversation"].append(followup_message)
        
        # Analyze followup
        followup_analysis = self.analyze_customer_request(followup_message)
        
        # If it's a bundle request, recalculate
        if followup_analysis["bundle_request"]:
            print("🎁 BUNDLE REQUEST DETECTED")
            print("-" * 30)
            
            # Combine services
            original_services = session["analysis"]["additional_services"]
            new_services = followup_analysis["additional_services"]
            all_services = list(set(original_services + new_services))
            
            # Recalculate pricing
            updated_pricing = self.calculate_pricing(
                session["analysis"]["service_type"],
                all_services,
                session["analysis"]["urgency"]
            )
            
            response = f"""Great! I can add {', '.join(new_services)} to your {session['analysis']['service_type'].replace('_', ' ')} service.

Updated pricing with bundle discount:
• Total: ${updated_pricing['total']:.2f}
• You save: ${updated_pricing['savings']:.2f} with our bundle discount!

Would you like to proceed with this combined service package?"""
            
            session["pricing"] = updated_pricing
            session["analysis"]["additional_services"] = all_services
            
            return {
                "request_id": request_id,
                "updated_services": all_services,
                "updated_pricing": updated_pricing,
                "response": response,
                "bundle_savings": updated_pricing['savings']
            }
        
        return {"response": "I understand your followup. How else can I help you?"}
    
    def generate_response(self, analysis: Dict, availability: Dict = None, pricing: Dict = None) -> str:
        """Generate human-like response"""
        
        service_name = analysis["service_type"].replace("_", " ").title()
        urgency_text = {"emergency": "emergency", "high": "urgent", "normal": "", "low": "flexible"}[analysis["urgency"]]
        
        response_parts = []
        
        # Service acknowledgment
        if urgency_text:
            response_parts.append(f"I understand you need {urgency_text} {service_name.lower()} service.")
        else:
            response_parts.append(f"I can help you with your {service_name.lower()} request.")
        
        # Availability info
        if availability:
            earliest = availability["earliest_available"]
            response_parts.append(f"Good news! We have availability as early as {earliest}.")
        
        # Pricing info
        if pricing:
            total = pricing["total"]
            if pricing["savings"] > 0:
                response_parts.append(f"The total cost is ${total:.2f}, and you'll save ${pricing['savings']:.2f} with our service bundle!")
            else:
                response_parts.append(f"The estimated cost is ${total:.2f}.")
        
        # Next steps
        response_parts.append("Would you like me to schedule this service for you?")
        
        return " ".join(response_parts)
    
    def determine_next_steps(self, analysis: Dict, availability: Dict = None, pricing: Dict = None) -> List[str]:
        """Determine what customer can do next"""
        
        steps = []
        
        if availability:
            steps.append("Select preferred appointment time")
        if pricing:
            steps.append("Review pricing details")
        if not analysis["additional_services"]:
            steps.append("Consider additional services for bundle savings")
        
        steps.append("Confirm service booking")
        return steps

# ============================================================================
# INTERVIEW DEMO RUNNER
# ============================================================================

def run_interview_demo():
    """
    Run complete interview demonstration
    
    Interview Strategy: This is your main demo presentation
    """
    
    print("🎯 ONEPATH INTERVIEW DEMONSTRATION")
    print("Advanced Agent System - ReACT Architecture")
    print("=" * 60)
    print()
    
    demo = SimpleAgentDemo()
    
    # Demo Scenario 1: AC Repair Request
    print("SCENARIO 1: INITIAL SERVICE REQUEST")
    print("Customer: 'My AC is broken. Can someone fix it this week?'")
    print()
    
    result1 = demo.process_service_request(
        "My AC is broken. Can someone fix it this week?",
        "demo-customer-001"
    )
    
    print("✅ Scenario 1 Complete!")
    print()
    input("Press Enter to continue to followup scenario...")
    print()
    
    # Demo Scenario 2: Bundle Followup  
    print("SCENARIO 2: BUNDLE FOLLOWUP REQUEST")
    print("Customer: 'Can you add thermostat installation too and bundle it?'")
    print()
    
    result2 = demo.handle_followup(
        result1["request_id"],
        "Can you add thermostat installation too and bundle it?"
    )
    
    print("✅ Scenario 2 Complete!")
    print()
    
    # Summary
    print("🏆 DEMONSTRATION SUMMARY")
    print("=" * 30)
    print("✅ ReACT Architecture: Reasoning → Action → Observation")
    print("✅ Multi-step tool orchestration")
    print("✅ Business logic integration")
    print("✅ Conversation context management")
    print("✅ Bundle optimization")
    print("✅ Dynamic pricing calculations")
    print()
    print("Key Interview Points Demonstrated:")
    print("• Agent reasoning and decision making")
    print("• Tool selection based on customer intent")
    print("• Business process automation")
    print("• Customer experience optimization")
    print("• Error handling and edge cases")

def show_code_structure():
    """Show the code structure for interview"""
    
    structure = """
    🏗️ CODE STRUCTURE OVERVIEW
    ==========================
    
    📁 Core Components:
    ├── SimpleAgentDemo (Main orchestrator)
    │   ├── analyze_customer_request() - Business intelligence
    │   ├── check_calendar_availability() - External API simulation  
    │   ├── calculate_pricing() - Business logic
    │   ├── process_service_request() - ReACT loop
    │   └── handle_followup() - Conversation continuity
    │
    ├── ReACT Pattern Implementation:
    │   ├── Step 1: Reasoning (analyze request)
    │   ├── Step 2: Action (check calendar)
    │   ├── Step 3: Action (calculate pricing)
    │   └── Step 4: Observation (generate response)
    │
    └── Business Logic:
        ├── Service type detection (AC, heating, plumbing, electrical)
        ├── Urgency classification (emergency, high, normal, low)
        ├── Bundle optimization (automatic discount calculation)
        └── Conversation memory (session management)
    
    🎯 Interview Talking Points:
    • "This demonstrates ReACT architecture without frameworks"
    • "Each step shows clear reasoning and action patterns"
    • "Business logic is separated for maintainability"
    • "System handles multi-turn conversations naturally"
    • "Error handling and edge cases are considered"
    """
    
    print(structure)

if __name__ == "__main__":
    print("🎯 OnePath Interview Demo - Choose Option:")
    print("1. Run complete demonstration")
    print("2. Show code structure")
    print("3. Both")
    print()
    
    choice = input("Enter choice (1-3): ").strip()
    
    if choice == "1":
        run_interview_demo()
    elif choice == "2":
        show_code_structure()
    elif choice == "3":
        show_code_structure()
        print("\n" + "="*60 + "\n")
        run_interview_demo()
    else:
        print("Running complete demo...")
        run_interview_demo()