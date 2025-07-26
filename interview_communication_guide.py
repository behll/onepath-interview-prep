"""
Interview Communication & Thought Process Guide for OnePath

Critical Success Factor: Being vocal, explaining reasoning clearly, 
and asking great clarifying questions about customer behavior and context.

This guide helps you practice the communication aspects that make or break the interview.
"""

from typing import List, Dict, Any
import json

class InterviewCommunicationGuide:
    """
    Guide for mastering interview communication
    
    The interview feedback specifically mentioned:
    - Being vocal during the interview
    - Confidently explaining your thoughts
    - Asking lots of clarifying questions about customer needs
    - Being curious about customer behavior and context
    """
    
    def __init__(self):
        self.thought_process_templates = self._create_thought_process_templates()
        self.clarifying_questions = self._create_clarifying_questions()
        self.explanation_frameworks = self._create_explanation_frameworks()
    
    def _create_thought_process_templates(self) -> Dict[str, List[str]]:
        """
        Templates for explaining your thought process during coding
        
        Interview Gold: Always verbalize your reasoning
        """
        return {
            "analysis_phase": [
                "Let me start by analyzing what the customer is really asking for...",
                "I'm breaking this down into several key components:",
                "My reasoning process here is to first understand...",
                "The first thing I need to determine is...",
                "I'm thinking through this step-by-step because..."
            ],
            
            "decision_making": [
                "I'm choosing this approach because...",
                "The reason I'm going with [X] over [Y] is...",
                "This decision is based on my assumption that...",
                "Let me explain why I think this is the right path...",
                "I'm prioritizing [X] because of [Y] requirement..."
            ],
            
            "code_explanation": [
                "What I'm building here is...",
                "This function handles the case where...",
                "I'm structuring it this way because...",
                "The key logic here is...",
                "This pattern allows us to..."
            ],
            
            "prompt_design": [
                "The prompt I'm crafting here needs to...",
                "I'm including this context because...",
                "The reason this prompt is structured this way is...",
                "I'm optimizing for [clarity/specificity/context] because...",
                "This prompt technique helps the agent..."
            ],
            
            "architecture_decisions": [
                "I'm designing the system this way because...",
                "The benefit of this architectural choice is...",
                "This pattern scales well when...",
                "I'm separating these concerns because...",
                "This approach handles the requirement for..."
            ]
        }
    
    def _create_clarifying_questions(self) -> Dict[str, List[str]]:
        """
        Great clarifying questions to ask during the interview
        
        Interview Strategy: Show curiosity about customer behavior and business context
        """
        return {
            "customer_behavior": [
                "What's the typical customer journey for service requests like this?",
                "How do customers usually express urgency? Are there common patterns?",
                "Do customers often add services mid-conversation, or is this rare?",
                "What's the most common followup question customers ask?",
                "How do customers typically react to pricing information?",
                "Are there seasonal patterns in how customers request services?"
            ],
            
            "business_context": [
                "What's the business priority - speed of response or cost optimization?",
                "How important is same-day service capability to the business model?",
                "Are there certain service combinations that are particularly profitable?",
                "What's the target customer segment - residential, commercial, or both?",
                "How does pricing strategy differ for emergency vs. scheduled services?",
                "What's the typical conversion rate from quote to booking?"
            ],
            
            "technical_requirements": [
                "Should the system handle multiple concurrent customers?",
                "What's the expected response time for agent reasoning?",
                "Are there external APIs I should assume exist (calendar, pricing, CRM)?",
                "How should the system handle API failures or timeouts?",
                "What level of conversation context should be maintained?",
                "Are there compliance or data privacy requirements I should consider?"
            ],
            
            "system_constraints": [
                "What's the acceptable latency for agent responses?",
                "Should I assume real-time or batch processing for certain operations?",
                "Are there budget constraints on API calls (like LLM tokens)?",
                "How many agents might be running simultaneously?",
                "What's the expected scale - hundreds or thousands of requests per hour?",
                "Are there geographical constraints on service availability?"
            ],
            
            "edge_cases": [
                "How should the system handle ambiguous customer requests?",
                "What happens if a customer requests a service type we don't offer?",
                "How do we handle customers who change their mind multiple times?",
                "What if the customer's location is outside the service area?",
                "How should we handle requests during non-business hours?",
                "What's the fallback if automated reasoning fails?"
            ]
        }
    
    def _create_explanation_frameworks(self) -> Dict[str, Dict[str, str]]:
        """
        Frameworks for structuring explanations during the interview
        """
        return {
            "feature_explanation": {
                "what": "What I'm building is...",
                "why": "The reason this is important is...",
                "how": "The way this works is...",
                "alternatives": "I considered [X] but chose [Y] because...",
                "benefits": "This approach gives us..."
            },
            
            "code_walkthrough": {
                "purpose": "This function/class is responsible for...",
                "inputs": "It takes these parameters...",
                "logic": "The core logic works by...",
                "outputs": "It returns/produces...",
                "integration": "This fits into the larger system by..."
            },
            
            "design_decision": {
                "context": "Given the requirement for...",
                "options": "I had several options: [A, B, C]...",
                "choice": "I chose [X] because...",
                "tradeoffs": "The tradeoff is [benefit] vs [cost]...",
                "future": "This decision allows us to later..."
            }
        }

class InterviewPracticeSession:
    """
    Practice session for interview communication
    
    Use this to rehearse explaining your thought process
    """
    
    def __init__(self):
        self.guide = InterviewCommunicationGuide()
        self.practice_scenarios = self._create_practice_scenarios()
    
    def _create_practice_scenarios(self) -> List[Dict[str, Any]]:
        """Create practice scenarios for rehearsal"""
        return [
            {
                "scenario": "Customer says: 'My AC is making weird noises and it's not cooling properly. I have guests coming this weekend.'",
                "practice_points": [
                    "Explain how you'd analyze the urgency",
                    "Describe what clarifying questions you'd ask",
                    "Walk through your reasoning for next steps",
                    "Justify your prompt design choices"
                ]
            },
            {
                "scenario": "Mid-interview requirement change: 'Actually, let's also handle heating system requests, not just AC.'",
                "practice_points": [
                    "Show how you'd adapt your existing code",
                    "Explain what would need to change in your prompts",
                    "Discuss architectural implications",
                    "Demonstrate thinking through edge cases"
                ]
            },
            {
                "scenario": "Interviewer asks: 'How would you handle a customer who keeps changing their service request?'",
                "practice_points": [
                    "Think through conversation state management",
                    "Consider user experience implications",
                    "Discuss business logic for handling changes",
                    "Explain technical implementation approach"
                ]
            }
        ]
    
    def practice_thought_articulation(self, scenario_index: int = 0):
        """
        Practice articulating thoughts for a specific scenario
        
        Interview Prep: Use this to rehearse your verbal explanations
        """
        
        if scenario_index >= len(self.practice_scenarios):
            print("Invalid scenario index")
            return
        
        scenario = self.practice_scenarios[scenario_index]
        
        print("🎯 PRACTICE SCENARIO")
        print("=" * 40)
        print(f"Scenario: {scenario['scenario']}")
        print()
        print("Practice Points:")
        for i, point in enumerate(scenario['practice_points'], 1):
            print(f"{i}. {point}")
        print()
        
        print("🗣️  PRACTICE FRAMEWORK:")
        print("Use these templates to structure your explanations:")
        print()
        
        for phase, templates in self.guide.thought_process_templates.items():
            print(f"{phase.upper().replace('_', ' ')}:")
            for template in templates[:2]:  # Show first 2 templates
                print(f"  • {template}")
            print()
        
        print("❓ CLARIFYING QUESTIONS TO ASK:")
        for category, questions in self.guide.clarifying_questions.items():
            print(f"{category.upper().replace('_', ' ')}:")
            for question in questions[:2]:  # Show first 2 questions
                print(f"  • {question}")
            print()
    
    def practice_requirement_adaptation(self):
        """
        Practice adapting to changing requirements mid-interview
        
        Interview Critical: They WILL change requirements during the task
        """
        
        print("🔄 REQUIREMENT ADAPTATION PRACTICE")
        print("=" * 45)
        print()
        
        adaptation_scenarios = [
            {
                "original": "Build agent for AC repair requests",
                "change": "Also handle plumbing emergencies",
                "response_framework": [
                    "Acknowledge the change: 'Great point, let me adapt the system for plumbing...'",
                    "Analyze impact: 'This affects my [prompt/routing/pricing] logic because...'",
                    "Show adaptability: 'I can extend this by...'",
                    "Ask clarifying questions: 'For plumbing emergencies, should I prioritize...?'"
                ]
            },
            {
                "original": "Handle single customer conversations",
                "change": "Support multiple concurrent customers",
                "response_framework": [
                    "Acknowledge: 'Ah, that's a scalability requirement I should address...'",
                    "Think aloud: 'For concurrent customers, I need to consider...'",
                    "Show architecture thinking: 'This means I need to modify my state management...'",
                    "Ask questions: 'What's the expected concurrent load?'"
                ]
            },
            {
                "original": "Focus on scheduling and pricing",
                "change": "Add inventory management for parts",
                "response_framework": [
                    "Acknowledge: 'Interesting, that adds a supply chain dimension...'",
                    "Expand thinking: 'For inventory, I'd need to consider...'",
                    "Show system thinking: 'This would require additional agents for...'",
                    "Clarify scope: 'Should the system check part availability before quoting?'"
                ]
            }
        ]
        
        for i, scenario in enumerate(adaptation_scenarios, 1):
            print(f"SCENARIO {i}:")
            print(f"Original: {scenario['original']}")
            print(f"Change: {scenario['change']}")
            print("Response Framework:")
            for step in scenario['response_framework']:
                print(f"  • {step}")
            print()

def create_interview_cheat_sheet():
    """
    Create a quick reference cheat sheet for the interview
    """
    
    cheat_sheet = """
    🎯 ONEPATH INTERVIEW CHEAT SHEET
    ================================
    
    VERBAL COMMUNICATION STARTERS:
    □ "Let me think through this step by step..."
    □ "My reasoning here is..."
    □ "I'm making this assumption because..."
    □ "A clarifying question I have is..."
    □ "The prompt I would design is..."
    □ "To handle this edge case..."
    □ "This architectural choice allows..."
    
    MUST-ASK CLARIFYING QUESTIONS:
    □ "What's the typical customer behavior pattern here?"
    □ "How do customers usually express urgency?"
    □ "What's the business priority - speed or cost optimization?"
    □ "Should I assume external APIs for calendar/pricing exist?"
    □ "What's the expected scale and concurrent load?"
    □ "How should the system handle API failures?"
    
    TECHNICAL CONCEPTS TO EMPHASIZE:
    □ ReACT reasoning loops (Thought → Action → Observation)
    □ Agent specialization and orchestration
    □ Dynamic prompt composition based on context
    □ Error handling and graceful degradation
    □ Microservice architecture patterns
    □ Context management across conversation turns
    
    ADAPTATION PHRASES FOR REQUIREMENT CHANGES:
    □ "Great point, let me adapt the system for..."
    □ "This affects my [component] because..."
    □ "I can extend this architecture by..."
    □ "That's an interesting constraint that changes..."
    
    DEMONSTRATION FLOW:
    1. Explain overall approach first
    2. Walk through ReACT reasoning step-by-step
    3. Show prompt composition in action
    4. Demonstrate agent chaining
    5. Handle the bundle followup scenario
    6. Discuss error handling and edge cases
    7. Show adaptability to new requirements
    
    RED FLAGS TO AVOID:
    ⚠️  Silent coding without explanation
    ⚠️  Not asking clarifying questions
    ⚠️  Rigid thinking when requirements change
    ⚠️  Focusing on perfect code over business logic
    ⚠️  Not explaining prompt design choices
    ⚠️  Missing the "why" behind decisions
    """
    
    return cheat_sheet

# ============================================================================
# PRACTICE SESSIONS
# ============================================================================

def run_communication_practice():
    """
    Run a full communication practice session
    """
    
    print("🗣️  ONEPATH INTERVIEW COMMUNICATION PRACTICE")
    print("=" * 50)
    print()
    
    practice = InterviewPracticeSession()
    
    print("STEP 1: Thought Articulation Practice")
    print("-" * 30)
    practice.practice_thought_articulation(0)
    
    input("\nPress Enter to continue to requirement adaptation practice...")
    print()
    
    print("STEP 2: Requirement Adaptation Practice")
    print("-" * 30)
    practice.practice_requirement_adaptation()
    
    input("\nPress Enter to see the interview cheat sheet...")
    print()
    
    print("STEP 3: Interview Cheat Sheet")
    print("-" * 30)
    print(create_interview_cheat_sheet())

if __name__ == "__main__":
    print("🎤 Ready to practice interview communication?")
    print("This will help you rehearse:")
    print("• Explaining your thought process clearly")
    print("• Asking great clarifying questions")
    print("• Adapting to changing requirements")
    print()
    
    choice = input("Start practice session? (y/n): ").lower()
    if choice == 'y':
        run_communication_practice()
    else:
        print("Practice ready when you are!")
        print("Command: python interview_communication_guide.py")