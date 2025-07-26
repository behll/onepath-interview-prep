"""
Real-Time Requirement Adaptation System for OnePath Interview

Critical Interview Requirement: "Expect new requirements mid-task—be ready to adapt"

This module demonstrates how to gracefully handle changing requirements during 
the live interview, showing flexibility and real-world engineering skills.
"""

from typing import Dict, List, Any, Optional, Callable
from enum import Enum
from dataclasses import dataclass, field
import json
from datetime import datetime

class RequirementChangeType(Enum):
    SCOPE_EXPANSION = "scope_expansion"          # Add new service types
    COMPLEXITY_INCREASE = "complexity_increase"  # Add multi-tenant support
    CONSTRAINT_ADDITION = "constraint_addition"  # Add performance requirements
    FEATURE_MODIFICATION = "feature_modification" # Change existing behavior
    INTEGRATION_REQUIREMENT = "integration_requirement" # Add external systems

@dataclass
class RequirementChange:
    """Represents a mid-interview requirement change"""
    change_type: RequirementChangeType
    description: str
    impact_areas: List[str]
    urgency: str  # "immediate", "before_completion", "nice_to_have"
    business_justification: str
    technical_implications: List[str]

class AdaptationStrategy:
    """
    Framework for adapting to requirement changes gracefully
    
    Interview Strategy: Show structured thinking under pressure
    """
    
    def __init__(self):
        self.adaptation_patterns = self._initialize_adaptation_patterns()
        self.impact_assessment_framework = self._create_impact_framework()
        
    def _initialize_adaptation_patterns(self) -> Dict[RequirementChangeType, Dict[str, Any]]:
        """
        Define patterns for handling different types of requirement changes
        
        Interview Gold: Show you have frameworks for handling change
        """
        return {
            RequirementChangeType.SCOPE_EXPANSION: {
                "approach": "extend_existing_architecture",
                "key_steps": [
                    "Identify reusable components",
                    "Define new service-specific logic",
                    "Update routing and orchestration",
                    "Extend prompt templates",
                    "Test integration points"
                ],
                "risk_factors": ["complexity explosion", "performance impact"],
                "mitigation_strategies": ["modular design", "service isolation"]
            },
            
            RequirementChangeType.COMPLEXITY_INCREASE: {
                "approach": "refactor_for_scalability",
                "key_steps": [
                    "Analyze current single-user assumptions",
                    "Introduce session/context management",
                    "Add concurrency controls",
                    "Update data models",
                    "Implement resource isolation"
                ],
                "risk_factors": ["breaking existing functionality", "performance bottlenecks"],
                "mitigation_strategies": ["phased implementation", "backward compatibility"]
            },
            
            RequirementChangeType.CONSTRAINT_ADDITION: {
                "approach": "optimize_within_constraints",
                "key_steps": [
                    "Benchmark current performance",
                    "Identify optimization opportunities",
                    "Implement caching strategies",
                    "Add monitoring and alerting",
                    "Create fallback mechanisms"
                ],
                "risk_factors": ["over-optimization", "reduced functionality"],
                "mitigation_strategies": ["performance budgets", "graceful degradation"]
            },
            
            RequirementChangeType.FEATURE_MODIFICATION: {
                "approach": "refactor_existing_components",
                "key_steps": [
                    "Identify affected components",
                    "Design backward-compatible changes",
                    "Update business logic",
                    "Modify prompts and responses",
                    "Test edge cases"
                ],
                "risk_factors": ["regression bugs", "user experience disruption"],
                "mitigation_strategies": ["feature flags", "A/B testing capability"]
            },
            
            RequirementChangeType.INTEGRATION_REQUIREMENT: {
                "approach": "add_external_integrations",
                "key_steps": [
                    "Define integration interfaces",
                    "Implement adapter patterns",
                    "Add error handling for external failures",
                    "Create mock services for testing",
                    "Document API contracts"
                ],
                "risk_factors": ["external dependencies", "network failures"],
                "mitigation_strategies": ["circuit breakers", "fallback services"]
            }
        }
    
    def _create_impact_framework(self) -> Dict[str, List[str]]:
        """
        Framework for assessing impact of requirement changes
        
        Interview Focus: Show systematic thinking about change impact
        """
        return {
            "technical_impact": [
                "What components need modification?",
                "What new components need creation?",
                "How does this affect system architecture?",
                "What are the performance implications?",
                "What new dependencies are introduced?"
            ],
            
            "business_impact": [
                "How does this change user experience?",
                "What new business value does this provide?",
                "How does this affect operational complexity?",
                "What are the cost implications?",
                "How does this align with business goals?"
            ],
            
            "development_impact": [
                "How much additional development time is needed?",
                "What testing strategy changes are required?",
                "How does this affect deployment complexity?",
                "What documentation needs updating?",
                "What training might be needed?"
            ],
            
            "risk_assessment": [
                "What could go wrong with this change?",
                "How likely are these risks?",
                "What would be the impact if risks materialize?",
                "How can we mitigate these risks?",
                "What's our rollback strategy?"
            ]
        }

class LiveAdaptationDemo:
    """
    Demonstration of live requirement adaptation during interview
    
    Interview Strategy: Use this to show real-time adaptation skills
    """
    
    def __init__(self):
        self.strategy = AdaptationStrategy()
        self.current_system_state = self._initialize_system_state()
        self.adaptation_history = []
    
    def _initialize_system_state(self) -> Dict[str, Any]:
        """Initialize the current state of our system before changes"""
        return {
            "services_supported": ["ac_repair"],
            "agent_types": ["primary", "calendar", "pricing", "followup"],
            "conversation_model": "single_customer_single_session",
            "external_integrations": [],
            "performance_requirements": "standard",
            "deployment_model": "single_instance"
        }
    
    def handle_requirement_change(self, change: RequirementChange) -> Dict[str, Any]:
        """
        Main method for handling requirement changes during interview
        
        Interview Strategy: 
        1. Acknowledge the change positively
        2. Analyze the impact systematically  
        3. Propose a solution approach
        4. Ask clarifying questions
        5. Show adaptability and confidence
        """
        
        print(f"🔄 REQUIREMENT CHANGE DETECTED")
        print(f"Change: {change.description}")
        print(f"Type: {change.change_type.value}")
        print()
        
        # Step 1: Acknowledge positively
        print("💬 ACKNOWLEDGMENT:")
        acknowledgment = self._generate_positive_acknowledgment(change)
        print(f"'{acknowledgment}'")
        print()
        
        # Step 2: Impact Analysis
        print("🔍 IMPACT ANALYSIS:")
        impact_analysis = self._analyze_change_impact(change)
        self._display_impact_analysis(impact_analysis)
        
        # Step 3: Solution Approach
        print("💡 SOLUTION APPROACH:")
        solution_approach = self._design_solution_approach(change)
        self._display_solution_approach(solution_approach)
        
        # Step 4: Clarifying Questions
        print("❓ CLARIFYING QUESTIONS:")
        questions = self._generate_clarifying_questions(change)
        for i, question in enumerate(questions, 1):
            print(f"{i}. {question}")
        print()
        
        # Step 5: Implementation Plan
        print("📋 IMPLEMENTATION PLAN:")
        implementation_plan = self._create_implementation_plan(change, solution_approach)
        self._display_implementation_plan(implementation_plan)
        
        # Record the adaptation
        adaptation_record = {
            "timestamp": datetime.now().isoformat(),
            "change": change,
            "impact_analysis": impact_analysis,
            "solution_approach": solution_approach,
            "implementation_plan": implementation_plan
        }
        self.adaptation_history.append(adaptation_record)
        
        return adaptation_record
    
    def _generate_positive_acknowledgment(self, change: RequirementChange) -> str:
        """
        Generate positive acknowledgment of the requirement change
        
        Interview Tip: Always respond positively to show adaptability
        """
        
        acknowledgments = {
            RequirementChangeType.SCOPE_EXPANSION: [
                "Great point! Expanding to handle more service types makes the system much more valuable.",
                "Excellent idea! Adding more services will demonstrate the system's flexibility.",
                "That's a really good extension - it shows how the architecture can scale."
            ],
            
            RequirementChangeType.COMPLEXITY_INCREASE: [
                "Ah, that's an important scalability consideration I should address.",
                "Good thinking! Multi-user support is definitely a real-world requirement.",
                "That's a crucial production consideration - let me adapt the architecture for that."
            ],
            
            RequirementChangeType.CONSTRAINT_ADDITION: [
                "Absolutely, performance constraints are important for production systems.",
                "Good point about adding those constraints - that's very realistic.",
                "Yes, those performance requirements definitely change how I'd approach this."
            ],
            
            RequirementChangeType.FEATURE_MODIFICATION: [
                "That's a great refinement to the user experience.",
                "Good insight! That change would definitely improve the customer interaction.",
                "Excellent point - that modification makes the system more practical."
            ],
            
            RequirementChangeType.INTEGRATION_REQUIREMENT: [
                "Perfect! Integration with external systems is exactly how this would work in production.",
                "Great addition! External integrations make this much more realistic.",
                "Excellent - those integrations are crucial for a complete solution."
            ]
        }
        
        return acknowledgments[change.change_type][0]
    
    def _analyze_change_impact(self, change: RequirementChange) -> Dict[str, Any]:
        """
        Systematically analyze the impact of the requirement change
        
        Interview Gold: Show structured thinking about impact
        """
        
        pattern = self.strategy.adaptation_patterns[change.change_type]
        
        impact_analysis = {
            "affected_components": self._identify_affected_components(change),
            "architectural_changes": self._assess_architectural_changes(change),
            "complexity_increase": self._estimate_complexity_increase(change),
            "risk_factors": pattern["risk_factors"],
            "effort_estimate": self._estimate_effort(change),
            "dependencies": self._identify_new_dependencies(change)
        }
        
        return impact_analysis
    
    def _identify_affected_components(self, change: RequirementChange) -> List[str]:
        """Identify which system components are affected by the change"""
        
        affected_components = []
        
        if change.change_type == RequirementChangeType.SCOPE_EXPANSION:
            affected_components.extend([
                "Agent routing logic",
                "Prompt templates", 
                "Service-specific business logic",
                "API endpoints",
                "Error handling"
            ])
        elif change.change_type == RequirementChangeType.COMPLEXITY_INCREASE:
            affected_components.extend([
                "Session management",
                "Data models",
                "Concurrency handling",
                "Resource allocation",
                "Database schema"
            ])
        elif change.change_type == RequirementChangeType.CONSTRAINT_ADDITION:
            affected_components.extend([
                "Performance monitoring",
                "Caching layers",
                "Resource optimization",
                "Load balancing",
                "Fallback mechanisms" 
            ])
        
        return affected_components
    
    def _assess_architectural_changes(self, change: RequirementChange) -> List[str]:
        """Assess what architectural changes are needed"""
        
        if change.change_type == RequirementChangeType.SCOPE_EXPANSION:
            return [
                "Extend service registry pattern",
                "Add new agent specializations",
                "Update orchestration routing",
                "Expand prompt composition system"
            ]
        elif change.change_type == RequirementChangeType.COMPLEXITY_INCREASE:
            return [
                "Introduce session management layer",
                "Add multi-tenancy support",
                "Implement resource isolation",
                "Add distributed state management"
            ]
        else:
            return ["Refactor existing components", "Add new infrastructure layers"]
    
    def _estimate_complexity_increase(self, change: RequirementChange) -> str:
        """Estimate how much complexity the change adds"""
        
        complexity_map = {
            RequirementChangeType.SCOPE_EXPANSION: "Medium - extends existing patterns",
            RequirementChangeType.COMPLEXITY_INCREASE: "High - fundamental architecture changes",
            RequirementChangeType.CONSTRAINT_ADDITION: "Medium - optimization and monitoring",
            RequirementChangeType.FEATURE_MODIFICATION: "Low - targeted changes",
            RequirementChangeType.INTEGRATION_REQUIREMENT: "Medium - external dependencies"
        }
        
        return complexity_map.get(change.change_type, "Unknown")
    
    def _estimate_effort(self, change: RequirementChange) -> str:
        """Estimate development effort for the change"""
        
        effort_map = {
            RequirementChangeType.SCOPE_EXPANSION: "2-3 additional hours",
            RequirementChangeType.COMPLEXITY_INCREASE: "4-6 additional hours", 
            RequirementChangeType.CONSTRAINT_ADDITION: "3-4 additional hours",
            RequirementChangeType.FEATURE_MODIFICATION: "1-2 additional hours",
            RequirementChangeType.INTEGRATION_REQUIREMENT: "2-4 additional hours"
        }
        
        return effort_map.get(change.change_type, "Unknown")
    
    def _identify_new_dependencies(self, change: RequirementChange) -> List[str]:
        """Identify new dependencies introduced by the change"""
        
        if change.change_type == RequirementChangeType.INTEGRATION_REQUIREMENT:
            return ["External API clients", "Authentication systems", "Circuit breakers"]
        elif change.change_type == RequirementChangeType.COMPLEXITY_INCREASE:
            return ["Session stores", "Load balancers", "Distributed caching"]
        else:
            return ["Minimal new dependencies"]
    
    def _design_solution_approach(self, change: RequirementChange) -> Dict[str, Any]:
        """
        Design the solution approach for handling the change
        
        Interview Focus: Show how you think through solutions
        """
        
        pattern = self.strategy.adaptation_patterns[change.change_type]
        
        return {
            "approach": pattern["approach"],
            "key_principles": [
                "Maintain backward compatibility where possible",
                "Use existing patterns and extend them",
                "Minimize risk through incremental changes",
                "Ensure testability of new components"
            ],
            "implementation_strategy": pattern["key_steps"],
            "risk_mitigation": pattern["mitigation_strategies"]
        }
    
    def _generate_clarifying_questions(self, change: RequirementChange) -> List[str]:
        """
        Generate clarifying questions to ask about the requirement change
        
        Interview Critical: Always ask clarifying questions
        """
        
        base_questions = [
            f"What's the priority level for this change - must-have or nice-to-have?",
            f"Are there any constraints I should be aware of for implementing this?",
            f"How does this change affect the user experience we're aiming for?"
        ]
        
        specific_questions = {
            RequirementChangeType.SCOPE_EXPANSION: [
                "What other service types should I prioritize after this one?",
                "Are there service types that have special requirements or constraints?",
                "Should the new services share the same pricing and scheduling logic?"
            ],
            
            RequirementChangeType.COMPLEXITY_INCREASE: [
                "What's the expected number of concurrent users?",
                "Should users be able to see each other's data, or is this fully isolated?",
                "Are there any compliance requirements for multi-user data handling?"
            ],
            
            RequirementChangeType.CONSTRAINT_ADDITION: [
                "What's the target response time for agent reasoning?",
                "Are there budget constraints on external API calls?",
                "What's the acceptable error rate for the system?"
            ],
            
            RequirementChangeType.INTEGRATION_REQUIREMENT: [
                "Are there specific external systems I should design for?",
                "What's the expected reliability of these external services?",
                "Should the system work offline if external services are down?"
            ]
        }
        
        return base_questions + specific_questions.get(change.change_type, [])
    
    def _create_implementation_plan(self, change: RequirementChange, solution_approach: Dict[str, Any]) -> Dict[str, Any]:
        """Create a concrete implementation plan"""
        
        return {
            "immediate_steps": solution_approach["implementation_strategy"][:2],
            "next_steps": solution_approach["implementation_strategy"][2:],
            "testing_strategy": [
                "Unit tests for new components",
                "Integration tests for modified workflows",
                "End-to-end testing of new scenarios"
            ],
            "rollout_plan": [
                "Implement core changes",
                "Test with limited scenarios", 
                "Gradually expand coverage",
                "Monitor and optimize"
            ]
        }
    
    def _display_impact_analysis(self, impact_analysis: Dict[str, Any]):
        """Display impact analysis results"""
        
        print(f"  Affected Components: {', '.join(impact_analysis['affected_components'][:3])}...")
        print(f"  Complexity Increase: {impact_analysis['complexity_increase']}")
        print(f"  Effort Estimate: {impact_analysis['effort_estimate']}")
        print(f"  Key Risks: {', '.join(impact_analysis['risk_factors'])}")
        print()
    
    def _display_solution_approach(self, solution_approach: Dict[str, Any]):
        """Display the solution approach"""
        
        print(f"  Strategy: {solution_approach['approach']}")
        print("  Key Steps:")
        for i, step in enumerate(solution_approach['implementation_strategy'][:3], 1):
            print(f"    {i}. {step}")
        print(f"    ... (and {len(solution_approach['implementation_strategy']) - 3} more)")
        print()
    
    def _display_implementation_plan(self, plan: Dict[str, Any]):
        """Display the implementation plan"""
        
        print("  Immediate Steps:")
        for i, step in enumerate(plan['immediate_steps'], 1):
            print(f"    {i}. {step}")
        
        print("  Testing Strategy:")
        for i, test in enumerate(plan['testing_strategy'], 1):
            print(f"    {i}. {test}")
        print()

# ============================================================================
# INTERVIEW SCENARIOS - Practice different requirement changes
# ============================================================================

class InterviewScenarioRunner:
    """
    Run different requirement change scenarios for practice
    
    Interview Prep: Use this to rehearse different types of changes
    """
    
    def __init__(self):
        self.demo = LiveAdaptationDemo()
        self.scenarios = self._create_practice_scenarios()
    
    def _create_practice_scenarios(self) -> List[RequirementChange]:
        """Create realistic requirement change scenarios"""
        
        return [
            RequirementChange(
                change_type=RequirementChangeType.SCOPE_EXPANSION,
                description="Actually, let's also handle plumbing emergencies, not just AC repair",
                impact_areas=["agent_routing", "service_logic", "pricing", "scheduling"],
                urgency="immediate",
                business_justification="Plumbing emergencies are high-revenue, urgent services",
                technical_implications=["New service type enum", "Plumbing-specific prompts", "Emergency routing logic"]
            ),
            
            RequirementChange(
                change_type=RequirementChangeType.COMPLEXITY_INCREASE,
                description="The system needs to handle multiple customers simultaneously",
                impact_areas=["session_management", "data_isolation", "resource_allocation"],
                urgency="before_completion",
                business_justification="Production systems must support concurrent users",
                technical_implications=["Session storage", "Context isolation", "Resource pools"]
            ),
            
            RequirementChange(
                change_type=RequirementChangeType.CONSTRAINT_ADDITION,
                description="Agent responses must be under 2 seconds, and we have a budget limit on LLM API calls",
                impact_areas=["performance", "caching", "optimization"],
                urgency="immediate",
                business_justification="User experience and cost control requirements",
                technical_implications=["Response caching", "Prompt optimization", "Circuit breakers"]
            ),
            
            RequirementChange(
                change_type=RequirementChangeType.INTEGRATION_REQUIREMENT,
                description="Integrate with existing customer CRM system and real calendar API",
                impact_areas=["external_apis", "data_sync", "error_handling"],
                urgency="nice_to_have",
                business_justification="Seamless integration with existing business systems",
                technical_implications=["API adapters", "Auth handling", "Fallback services"]
            ),
            
            RequirementChange(
                change_type=RequirementChangeType.FEATURE_MODIFICATION,
                description="Customers should be able to modify their service request after initial quote",
                impact_areas=["conversation_flow", "state_management", "pricing_updates"],
                urgency="before_completion",
                business_justification="Improves customer satisfaction and reduces cancellations",
                technical_implications=["Request modification logic", "Price recalculation", "History tracking"]
            )
        ]
    
    def run_scenario(self, scenario_index: int = 0):
        """Run a specific adaptation scenario"""
        
        if scenario_index >= len(self.scenarios):
            print("Invalid scenario index")
            return
        
        scenario = self.scenarios[scenario_index]
        
        print(f"🎯 ADAPTATION SCENARIO {scenario_index + 1}")
        print("=" * 50)
        print()
        
        # Run the adaptation
        result = self.demo.handle_requirement_change(scenario)
        
        print("✅ ADAPTATION COMPLETE")
        print()
        print("Interview Tips for this scenario:")
        print("• Show confidence and adaptability")
        print("• Ask follow-up questions to clarify scope")
        print("• Explain your reasoning step-by-step")
        print("• Demonstrate understanding of business impact")
        
        return result
    
    def run_all_scenarios(self):
        """Run all adaptation scenarios for comprehensive practice"""
        
        print("🔄 COMPREHENSIVE ADAPTATION PRACTICE")
        print("=" * 50)
        print()
        
        for i, scenario in enumerate(self.scenarios):
            print(f"SCENARIO {i + 1}: {scenario.description}")
            print("-" * 40)
            self.run_scenario(i)
            
            if i < len(self.scenarios) - 1:
                input("\nPress Enter for next scenario...")
                print()
        
        print("🏆 ALL ADAPTATION SCENARIOS COMPLETE!")
        print()
        print("You're now prepared to handle:")
        print("✅ Scope expansion requests")
        print("✅ Complexity increases")
        print("✅ New constraints and requirements")
        print("✅ Integration requirements")
        print("✅ Feature modifications")

# ============================================================================
# MAIN DEMO RUNNER
# ============================================================================

def run_adaptation_demo():
    """
    Main demo runner for requirement adaptation practice
    """
    
    print("🔧 ONEPATH INTERVIEW - REQUIREMENT ADAPTATION DEMO")
    print("=" * 55)
    print()
    print("This demo prepares you for:")
    print("• Handling mid-interview requirement changes")
    print("• Showing adaptability and structured thinking")
    print("• Asking the right clarifying questions")
    print("• Maintaining confidence under changing requirements")
    print()
    
    runner = InterviewScenarioRunner()
    
    print("Choose practice mode:")
    print("1. Single scenario practice")
    print("2. All scenarios comprehensive practice")
    print()
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        print("\nAvailable scenarios:")
        for i, scenario in enumerate(runner.scenarios):
            print(f"{i + 1}. {scenario.description}")
        
        scenario_choice = input(f"\nSelect scenario (1-{len(runner.scenarios)}): ").strip()
        try:
            scenario_index = int(scenario_choice) - 1
            runner.run_scenario(scenario_index)
        except (ValueError, IndexError):
            print("Invalid choice. Running scenario 1.")
            runner.run_scenario(0)
    
    elif choice == "2":
        runner.run_all_scenarios()
    
    else:
        print("Invalid choice. Running single scenario demo.")
        runner.run_scenario(0)

if __name__ == "__main__":
    run_adaptation_demo()