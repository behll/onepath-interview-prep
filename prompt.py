"""
Advanced Prompt Composition System for OnePath Agent
Implements ReACT and Chain-of-Thought (CoT) Prompting Strategies

Key Features:
- Dynamic prompt composition based on context
- ReACT prompting (Reasoning + Acting)  
- Chain-of-Thought reasoning prompts
- Context-aware modifications
- Multi-turn conversation handling
- Error recovery prompting
"""

import json
import re
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum
from service_models import ActionType, WorkflowContext


class PromptType(Enum):
    REACT_REASONING = "react_reasoning"
    COT_ANALYSIS = "cot_analysis"
    CALENDAR_OPTIMIZATION = "calendar_optimization"
    PRICING_CALCULATION = "pricing_calculation"
    BUNDLE_OPTIMIZATION = "bundle_optimization"
    CUSTOMER_COMMUNICATION = "customer_communication"
    ERROR_RECOVERY = "error_recovery"


class ConversationState:
    """
    Tracks conversation state for context-aware prompting
    """
    
    def __init__(self):
        self.messages = []
        self.extracted_entities = {}
        self.customer_preferences = {}
        self.confidence_history = []
        self.error_count = 0
        self.last_successful_action = None
        
    def add_message(self, role: str, content: str, metadata: Dict = None):
        """Add message to conversation history"""
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        self.messages.append(message)
        
        if role == "user":
            self._update_entities_from_message(content)
    
    def _update_entities_from_message(self, content: str):
        """Extract and update entities from user message"""
        content_lower = content.lower()
        
        # Service type detection
        service_patterns = {
            "ac_repair": ["ac", "air conditioning", "cooling", "hvac", "conditioner"],
            "heating": ["heat", "heating", "furnace", "boiler", "warm"],
            "plumbing": ["plumb", "water", "leak", "pipe", "drain", "toilet"],
            "electrical": ["electric", "power", "outlet", "wiring", "lights"]
        }
        
        for service, patterns in service_patterns.items():
            if any(pattern in content_lower for pattern in patterns):
                self.extracted_entities["service_type"] = service
                break
        
        # Urgency detection
        urgency_patterns = {
            "emergency": ["emergency", "urgent", "asap", "immediately", "broken", "not working"],
            "high": ["this week", "soon", "quickly", "today", "tomorrow"],
            "normal": ["convenient", "schedule", "when possible"],
            "low": ["whenever", "no rush", "flexible"]
        }
        
        for urgency, patterns in urgency_patterns.items():
            if any(pattern in content_lower for pattern in patterns):
                self.extracted_entities["urgency"] = urgency
                break
        
        # Bundle request detection
        bundle_indicators = ["add", "also", "too", "bundle", "package", "plus", "include"]
        if any(indicator in content_lower for indicator in bundle_indicators):
            self.extracted_entities["bundle_request"] = True
        
        # Location hints
        location_patterns = ["house", "home", "office", "building", "apartment", "condo"]
        for pattern in location_patterns:
            if pattern in content_lower:
                self.extracted_entities["location_type"] = pattern
                break


class PromptComposer:
    """
    Advanced prompt composition engine implementing ReACT and CoT strategies
    """
    
    def __init__(self):
        self.base_prompts = self._initialize_base_prompts()
        self.prompt_enhancers = self._initialize_prompt_enhancers()
        self.context_adapters = self._initialize_context_adapters()
    
    def compose_react_prompt(self, 
                           context: WorkflowContext, 
                           current_step: str,
                           specific_goal: str = None) -> str:
        """
        Compose a ReACT (Reasoning + Acting) prompt
        
        ReACT prompting structure:
        1. System context and role definition
        2. Current situation analysis
        3. Available actions and their purposes
        4. Reasoning framework
        5. Expected output format
        """
        
        base_prompt = self.base_prompts[PromptType.REACT_REASONING]
        
        # Context injection
        context_info = {
            "customer_message": context.customer_message,
            "extracted_entities": json.dumps(context.extracted_entities, indent=2),
            "conversation_history": self._format_conversation_history(context.conversation_history),
            "current_step": current_step,
            "specific_goal": specific_goal or "provide excellent customer service"
        }
        
        # Apply context-specific enhancements
        enhanced_prompt = self._apply_context_enhancements(
            base_prompt, 
            context, 
            PromptType.REACT_REASONING
        )
        
        # Inject parameters
        final_prompt = self._inject_parameters(enhanced_prompt, context_info)
        
        return final_prompt
    
    def compose_cot_prompt(self, 
                          analysis_focus: str,
                          context: WorkflowContext,
                          data_to_analyze: Dict[str, Any]) -> str:
        """
        Compose a Chain-of-Thought analysis prompt
        
        CoT prompting structure:
        1. Clear analysis objective
        2. Step-by-step thinking framework
        3. Relevant data presentation
        4. Guided reasoning process
        5. Conclusion and confidence assessment
        """
        
        base_prompt = self.base_prompts[PromptType.COT_ANALYSIS]
        
        # CoT-specific parameters
        cot_params = {
            "analysis_focus": analysis_focus,
            "step_by_step_framework": self._generate_cot_framework(analysis_focus),
            "relevant_data": json.dumps(data_to_analyze, indent=2),
            "conversation_context": self._create_context_summary(context)
        }
        
        # Apply CoT-specific enhancements
        enhanced_prompt = self._apply_cot_enhancements(base_prompt, analysis_focus, context)
        
        # Inject parameters
        final_prompt = self._inject_parameters(enhanced_prompt, cot_params)
        
        return final_prompt
    
    def compose_specialized_prompt(self, 
                                 prompt_type: PromptType,
                                 context: WorkflowContext,
                                 specific_data: Dict[str, Any]) -> str:
        """
        Compose specialized prompts for specific actions
        """
        
        if prompt_type not in self.base_prompts:
            raise ValueError(f"Unknown prompt type: {prompt_type}")
        
        base_prompt = self.base_prompts[prompt_type]
        
        # Apply type-specific enhancements
        enhanced_prompt = self._apply_type_specific_enhancements(
            base_prompt, 
            prompt_type, 
            context
        )
        
        # Inject specific data
        final_prompt = self._inject_parameters(enhanced_prompt, specific_data)
        
        return final_prompt
    
    def _initialize_base_prompts(self) -> Dict[PromptType, str]:
        """
        Initialize comprehensive base prompt templates
        """
        return {
            PromptType.REACT_REASONING: """
You are an expert service dispatch reasoning agent for OnePath, a premium home services company. Your role is to analyze customer requests using sophisticated reasoning and determine the optimal next action.

CURRENT SITUATION:
Customer Message: {customer_message}
Extracted Information: {extracted_entities}
Conversation History: {conversation_history}
Current Step: {current_step}
Specific Goal: {specific_goal}

REACT REASONING FRAMEWORK:
Follow this systematic approach to analyze and respond to the customer's needs:

THOUGHT PROCESS:
1. COMPREHENSION: What is the customer actually requesting? Look beyond the surface words to understand their true intent, urgency level, and underlying concerns.

2. CONTEXT ANALYSIS: What do we know about their situation? Consider their service type needs, timing requirements, budget implications, and any special circumstances that might affect service delivery.

3. INFORMATION ASSESSMENT: What critical information do we have, and what are we missing? Identify gaps that could impact our ability to provide excellent service.

4. CONSTRAINT EVALUATION: What limitations or constraints might affect our service delivery? Consider technician availability, parts requirements, seasonal factors, and customer preferences.

5. OPPORTUNITY IDENTIFICATION: Are there opportunities to add value through bundle services, preventive maintenance, or enhanced service options that benefit the customer?

ACTION SELECTION LOGIC:
Based on your analysis, choose the most appropriate next action:

- CALENDAR_CHECK: Use when customer has indicated timing preferences or urgency. This action queries technician availability and schedules appointments based on service requirements and customer preferences.

- PRICING_QUERY: Use when customer has asked about costs, wants to compare options, or when you need to provide transparent pricing information. This includes base service costs, additional options, and potential bundle savings.

- BUNDLE_ANALYSIS: Use when customer mentions multiple services or when you identify opportunities to provide enhanced value through service combinations. This optimizes both cost and scheduling efficiency.

- CUSTOMER_FOLLOWUP: Use when you need clarification, have additional questions, or want to ensure complete understanding of customer needs before proceeding.

CONFIDENCE ASSESSMENT:
Evaluate your confidence level (0.0 to 1.0) based on:
- Clarity of customer request
- Completeness of available information  
- Alignment between customer needs and available actions
- Your assessment of the optimal outcome likelihood

RESPONSE FORMAT:
Provide your analysis in this structure:
1. THOUGHT: [Your comprehensive reasoning process]
2. ACTION: [Selected action with specific parameters]
3. CONFIDENCE: [Numerical confidence score with explanation]
4. ASSUMPTIONS: [Key assumptions you're making]
5. ALTERNATIVE_APPROACHES: [Other viable options considered]
""",

            PromptType.COT_ANALYSIS: """
You are an analytical expert specializing in {analysis_focus} for home service operations. Use systematic Chain-of-Thought reasoning to analyze the provided data and generate actionable insights.

ANALYSIS OBJECTIVE: {analysis_focus}

RELEVANT DATA:
{relevant_data}

CONVERSATION CONTEXT:
{conversation_context}

CHAIN-OF-THOUGHT REASONING FRAMEWORK:
{step_by_step_framework}

ANALYTICAL APPROACH:
Apply rigorous step-by-step thinking to thoroughly examine the situation:

STEP 1 - DATA INTERPRETATION: Begin by carefully examining the provided data. What are the key facts, numbers, and constraints? Identify patterns, outliers, and critical data points that will influence your analysis.

STEP 2 - CONTEXT INTEGRATION: How does this data relate to the customer's broader service needs and preferences? Consider their stated requirements, implied needs, and any historical context that might be relevant.

STEP 3 - CONSTRAINT IDENTIFICATION: What limitations or restrictions must be considered? This includes technical constraints, scheduling limitations, budget considerations, and operational capacity.

STEP 4 - OPTION GENERATION: Based on your analysis, what are all the viable approaches or solutions? Consider both obvious options and creative alternatives that might provide superior value.

STEP 5 - COMPARATIVE EVALUATION: Systematically compare each option across multiple dimensions: cost, time, quality, customer satisfaction, operational efficiency, and risk factors.

STEP 6 - OPTIMIZATION IDENTIFICATION: Are there opportunities to enhance the solution through bundling, timing optimization, resource allocation, or other strategic approaches?

STEP 7 - RECOMMENDATION FORMULATION: Based on your comprehensive analysis, what is your recommended approach? Provide specific rationale for why this option best serves the customer's interests.

STEP 8 - CONFIDENCE AND RISK ASSESSMENT: Evaluate your confidence level in this recommendation and identify any risks or contingencies that should be considered.

OUTPUT REQUIREMENTS:
- Provide detailed reasoning for each step
- Show your work and logical progression
- Include numerical calculations where relevant
- Identify key assumptions and their validity
- Assess confidence level and potential risks
- Recommend specific next actions
""",

            PromptType.CALENDAR_OPTIMIZATION: """
You are a scheduling optimization specialist for OnePath services. Your goal is to find the optimal appointment slots that balance customer preferences, operational efficiency, and service quality.

SERVICE REQUIREMENTS:
Service Type: {service_type}
Estimated Duration: {estimated_duration}
Urgency Level: {urgency_level}
Special Requirements: {special_requirements}

CUSTOMER PREFERENCES:
Preferred Times: {preferred_times}
Location: {service_location}
Flexibility: {scheduling_flexibility}

OPERATIONAL CONSTRAINTS:
Available Technicians: {available_technicians}
Equipment Availability: {equipment_constraints}
Travel Time Considerations: {travel_optimization}

OPTIMIZATION CRITERIA:
1. CUSTOMER SATISFACTION: Prioritize slots that closely match customer preferences while ensuring adequate service time and minimal wait periods.

2. OPERATIONAL EFFICIENCY: Consider travel time between appointments, technician specialization alignment, and equipment utilization to minimize costs and maximize productivity.

3. SERVICE QUALITY: Ensure adequate time allocation for thorough service delivery, including diagnostic time, repair execution, and customer explanation.

4. RISK MITIGATION: Account for potential delays, complexity variations, and buffer time requirements to maintain schedule reliability.

SCHEDULING ANALYSIS:
Evaluate each potential slot across these dimensions:
- Customer preference alignment score
- Operational efficiency rating
- Service quality assurance level
- Schedule reliability assessment

RECOMMENDATION FORMAT:
1. OPTIMAL SLOT: [Primary recommendation with full justification]
2. ALTERNATIVE OPTIONS: [2-3 backup options with trade-off analysis]
3. EFFICIENCY GAINS: [Operational benefits of recommended scheduling]
4. CUSTOMER BENEFITS: [Value proposition for the customer]
5. RISK FACTORS: [Potential challenges and mitigation strategies]
""",

            PromptType.PRICING_CALCULATION: """
You are a pricing analysis expert for OnePath services. Your role is to calculate accurate, competitive, and fair pricing that provides value to customers while ensuring business sustainability.

SERVICE DETAILS:
Primary Service: {primary_service}
Additional Services: {additional_services}
Service Complexity: {complexity_assessment}
Urgency Factor: {urgency_factor}

CUSTOMER CONTEXT:
Customer Type: {customer_segment}
Service History: {service_history}
Location Factors: {location_considerations}

PRICING COMPONENTS TO ANALYZE:

1. BASE SERVICE COSTS: Calculate core service pricing including diagnostic fees, labor rates, and standard material costs. Consider skill level requirements and time estimates.

2. ADDITIONAL SERVICE EVALUATION: Assess each additional service request, considering both individual pricing and potential bundle synergies.

3. COMPLEXITY ADJUSTMENTS: Factor in any complexity premium or discounts based on job characteristics, access difficulties, or technical requirements.

4. URGENCY SURCHARGES: Apply appropriate urgency pricing when customer requires expedited service, considering both premium labor costs and scheduling impacts.

5. BUNDLE OPTIMIZATION: Identify opportunities for service bundling that provides customer savings while improving operational efficiency.

6. COMPETITIVE POSITIONING: Ensure pricing is competitive within local market while reflecting OnePath's premium service quality and customer experience.

7. VALUE PROPOSITION ANALYSIS: Calculate total customer value including service quality, warranty coverage, technician expertise, and long-term benefits.

PRICING CALCULATION FRAMEWORK:
- Base service cost calculation with detailed breakdown
- Additional service integration and bundle analysis
- Surcharge and discount application with justification
- Tax and fee calculation for total transparency
- Value comparison against market alternatives
- Payment option and financing availability

FINAL PRICING PRESENTATION:
Present pricing in clear, customer-friendly format with:
1. Service breakdown and costs
2. Bundle savings and value highlights
3. Total investment with payment options
4. Warranty and service guarantees
5. Competitive value proposition
""",

            PromptType.BUNDLE_OPTIMIZATION: """
You are a service bundle optimization specialist for OnePath. Your expertise lies in identifying service combinations that maximize customer value while improving operational efficiency and business profitability.

REQUESTED SERVICES:
Primary Service: {primary_service}
Additional Services Mentioned: {additional_services}
Customer Intent: {customer_intent}

OPTIMIZATION ANALYSIS:

1. SERVICE COMPATIBILITY ASSESSMENT: Analyze how well the requested services work together from technical, scheduling, and resource perspectives. Consider whether services can be performed by the same technician during a single visit.

2. CUSTOMER VALUE MAXIMIZATION: Identify how bundling creates value for the customer through cost savings, convenience benefits, comprehensive problem solving, and enhanced service guarantees.

3. OPERATIONAL EFFICIENCY GAINS: Calculate efficiency improvements through reduced travel time, optimized technician utilization, bulk material purchasing, and streamlined service delivery.

4. BUNDLE CONFIGURATION OPTIONS: Design multiple bundle configurations ranging from basic combinations to comprehensive service packages, each with distinct value propositions.

5. PRICING OPTIMIZATION: Structure bundle pricing to provide meaningful customer savings while maintaining healthy profit margins and competitive positioning.

6. SEASONAL AND PROMOTIONAL OPPORTUNITIES: Consider timing-related bundle benefits, seasonal service needs, and promotional opportunities that enhance customer value.

BUNDLE EVALUATION CRITERIA:
- Total customer savings potential
- Service delivery timeline optimization
- Technician skill and resource alignment
- Long-term customer relationship impact
- Competitive differentiation opportunity

COMPREHENSIVE BUNDLE ANALYSIS:
For each viable bundle option, provide:

BUNDLE COMPOSITION: Detailed service list with individual and bundled specifications

COST-BENEFIT ANALYSIS: Individual service costs vs. bundle pricing with savings calculation and value-add quantification

OPERATIONAL SYNERGIES: Scheduling efficiency, resource optimization, and service delivery streamlining benefits

CUSTOMER EXPERIENCE ENHANCEMENT: Convenience factors, comprehensive problem resolution, and service guarantee improvements

COMPETITIVE ADVANTAGES: How bundle positioning creates market differentiation and customer preference

RISK ASSESSMENT: Potential challenges in bundle delivery and mitigation strategies

RECOMMENDATION FRAMEWORK:
1. OPTIMAL BUNDLE CONFIGURATION: Primary recommendation with complete justification
2. ALTERNATIVE BUNDLE OPTIONS: Secondary options for different customer priorities
3. IMPLEMENTATION TIMELINE: Service scheduling and delivery sequence
4. VALUE COMMUNICATION STRATEGY: How to present bundle benefits to customer
5. SUCCESS METRICS: How to measure bundle effectiveness and customer satisfaction
""",

            PromptType.CUSTOMER_COMMUNICATION: """
You are a customer communication specialist for OnePath services. Your role is to craft clear, helpful, and professional communications that build trust, provide value, and guide customers toward optimal service decisions.

COMMUNICATION CONTEXT:
Customer Situation: {customer_situation}
Communication Purpose: {communication_purpose}
Customer Preferences: {customer_preferences}
Service Context: {service_context}

COMMUNICATION PRINCIPLES:

1. CLARITY AND TRANSPARENCY: Ensure all communication is easily understood, free from technical jargon unless necessary, and completely transparent about costs, timelines, and service expectations.

2. VALUE-FOCUSED MESSAGING: Emphasize the value and benefits customers receive, including service quality, expertise, warranties, and long-term problem resolution.

3. PROFESSIONAL EMPATHY: Acknowledge customer concerns and frustrations while maintaining professional confidence in OnePath's ability to resolve their service needs.

4. SOLUTION-ORIENTED APPROACH: Focus communication on solutions, options, and positive outcomes rather than problems or limitations.

5. PROACTIVE INFORMATION SHARING: Anticipate customer questions and provide relevant information before they need to ask.

COMMUNICATION FRAMEWORK:

OPENING: Acknowledge customer situation with empathy and establish OnePath's commitment to resolution

SITUATION ANALYSIS: Demonstrate understanding of their specific needs and circumstances

OPTIONS PRESENTATION: Clearly outline available solutions with benefits and considerations for each

VALUE PROPOSITION: Highlight unique advantages of OnePath service delivery and customer experience

NEXT STEPS: Provide clear, actionable next steps with timeline and expectations

SUPPORT ASSURANCE: Reinforce ongoing support availability and customer satisfaction commitment

COMMUNICATION TONE GUIDELINES:
- Professional yet approachable
- Confident in service capabilities
- Empathetic to customer concerns
- Solution-focused and positive
- Clear and jargon-free
- Respectful of customer time and priorities

RESPONSE STRUCTURE:
Organize communication to:
1. Address immediate customer concerns
2. Provide relevant service information
3. Present clear options and recommendations
4. Explain value and benefits
5. Outline next steps and timeline
6. Offer additional support and resources
""",

            PromptType.ERROR_RECOVERY: """
You are an error recovery specialist for OnePath service operations. Your role is to analyze service delivery challenges, identify recovery strategies, and implement solutions that restore customer confidence while improving future service delivery.

ERROR CONTEXT:
Error Type: {error_type}
Impact Assessment: {impact_level}
Customer Affected: {customer_impact}
Service Context: {service_situation}

RECOVERY STRATEGY FRAMEWORK:

1. IMMEDIATE IMPACT MITIGATION: Address the most pressing customer concerns and service delivery issues to prevent further negative impact on customer experience.

2. ROOT CAUSE ANALYSIS: Systematically identify the underlying causes of the service delivery error to prevent recurrence and improve operational processes.

3. CUSTOMER RECOVERY APPROACH: Develop comprehensive customer recovery strategy that not only resolves the immediate issue but strengthens the customer relationship.

4. OPERATIONAL CORRECTION: Implement operational changes needed to correct the current situation and establish preventive measures for similar future scenarios.

5. SERVICE DELIVERY ENHANCEMENT: Use the error as an opportunity to enhance overall service delivery quality and customer experience.

RECOVERY EXECUTION PRIORITIES:

CUSTOMER COMMUNICATION: Proactive, transparent communication that acknowledges the issue, explains resolution steps, and reinforces OnePath's commitment to excellence

SERVICE CORRECTION: Immediate actions to correct any service deficiencies, including re-service, additional work, or service enhancements at no additional cost

RELATIONSHIP RESTORATION: Strategies to restore and strengthen customer trust, including service guarantees, follow-up commitments, and value-added services

OPERATIONAL IMPROVEMENTS: Process enhancements, training requirements, or system improvements needed to prevent similar issues

QUALITY ASSURANCE: Enhanced quality control measures for this customer and similar future services

RECOVERY SUCCESS METRICS:
- Customer satisfaction restoration
- Service quality correction
- Relationship strength improvement
- Operational process enhancement
- Prevention effectiveness

RECOVERY PLAN COMPONENTS:
1. IMMEDIATE ACTIONS: What must be done right now to address customer concerns
2. SERVICE CORRECTIONS: Specific service delivery improvements or corrections needed
3. CUSTOMER RELATIONSHIP STRATEGY: How to restore and strengthen customer trust
4. OPERATIONAL ENHANCEMENTS: Process improvements to prevent recurrence
5. FOLLOW-UP COMMITMENTS: Ongoing support and quality assurance measures
6. SUCCESS VALIDATION: How to confirm recovery effectiveness and customer satisfaction
"""
        }
    
    def _initialize_prompt_enhancers(self) -> Dict[str, str]:
        """
        Initialize prompt enhancement templates for different scenarios
        """
        return {
            "urgency_enhancer": """
URGENT SITUATION PROTOCOL:
This is a high-priority service request requiring expedited handling. Apply emergency service protocols, consider after-hours availability, and prioritize rapid response while maintaining service quality standards.
""",
            "bundle_enhancer": """
BUNDLE OPPORTUNITY ENHANCEMENT:
Customer has indicated interest in multiple services. Focus on identifying synergies, cost savings opportunities, scheduling efficiencies, and comprehensive problem resolution through service bundling.
""",
            "repeat_customer_enhancer": """
VALUED CUSTOMER RECOGNITION:
This customer has previous service history with OnePath. Leverage relationship knowledge, apply loyalty considerations, and ensure service excellence that reinforces customer satisfaction and long-term relationship value.
""",
            "complex_service_enhancer": """
COMPLEX SERVICE SITUATION:
This request involves multiple factors requiring sophisticated analysis. Apply enhanced reasoning, consider interdependencies, and ensure comprehensive solution development that addresses all customer needs.
""",
            "error_recovery_enhancer": """
ERROR RECOVERY MODE:
Previous service delivery did not meet OnePath standards. Focus on relationship restoration, service excellence, and operational improvements that demonstrate OnePath's commitment to customer satisfaction.
"""
        }
    
    def _initialize_context_adapters(self) -> Dict[str, callable]:
        """
        Initialize context adaptation functions
        """
        return {
            "urgency_adapter": self._adapt_for_urgency,
            "bundle_adapter": self._adapt_for_bundle_request,
            "history_adapter": self._adapt_for_customer_history,
            "complexity_adapter": self._adapt_for_complexity
        }
    
    def _apply_context_enhancements(self, 
                                   base_prompt: str, 
                                   context: WorkflowContext, 
                                   prompt_type: PromptType) -> str:
        """
        Apply context-specific enhancements to base prompt
        """
        enhanced_prompt = base_prompt
        
        # Apply urgency enhancement
        if context.extracted_entities.get("urgency") in ["emergency", "high"]:
            enhanced_prompt = self.prompt_enhancers["urgency_enhancer"] + enhanced_prompt
        
        # Apply bundle enhancement
        if context.extracted_entities.get("bundle_request"):
            enhanced_prompt = enhanced_prompt + "\n" + self.prompt_enhancers["bundle_enhancer"]
        
        # Apply repeat customer enhancement
        if len(context.conversation_history) > 2:
            enhanced_prompt = self.prompt_enhancers["repeat_customer_enhancer"] + enhanced_prompt
        
        # Apply complexity enhancement for multi-step workflows
        if len(context.workflow_steps) > 3:
            enhanced_prompt = enhanced_prompt + "\n" + self.prompt_enhancers["complex_service_enhancer"]
        
        return enhanced_prompt
    
    def _apply_cot_enhancements(self, 
                               base_prompt: str, 
                               analysis_focus: str, 
                               context: WorkflowContext) -> str:
        """
        Apply Chain-of-Thought specific enhancements
        """
        enhanced_prompt = base_prompt
        
        # Add analysis-specific reasoning steps
        if analysis_focus == "pricing":
            enhanced_prompt += """
PRICING-SPECIFIC COT ENHANCEMENT:
- Consider all cost components systematically
- Evaluate bundle opportunities and savings
- Assess competitive positioning and value proposition
- Calculate total customer investment and payment options
"""
        elif analysis_focus == "scheduling":
            enhanced_prompt += """
SCHEDULING-SPECIFIC COT ENHANCEMENT:
- Analyze technician availability and specialization
- Consider customer timing preferences and constraints
- Evaluate operational efficiency and travel optimization
- Assess service quality and time allocation requirements
"""
        
        return enhanced_prompt
    
    def _apply_type_specific_enhancements(self, 
                                        base_prompt: str, 
                                        prompt_type: PromptType, 
                                        context: WorkflowContext) -> str:
        """
        Apply enhancements specific to prompt type
        """
        enhanced_prompt = base_prompt
        
        if prompt_type == PromptType.BUNDLE_OPTIMIZATION:
            if len(context.conversation_history) > 1:
                enhanced_prompt += """
MULTI-TURN CONVERSATION CONTEXT:
Customer has been engaged in detailed discussion about services. Focus on comprehensive solution development that addresses all expressed and implied needs while maximizing value delivery.
"""
        
        return enhanced_prompt
    
    def _generate_cot_framework(self, analysis_focus: str) -> str:
        """
        Generate analysis-specific Chain-of-Thought framework
        """
        frameworks = {
            "pricing": """
1. BASE COST ANALYSIS: Examine individual service costs and requirements
2. BUNDLE EVALUATION: Assess service combination opportunities and synergies  
3. VALUE CALCULATION: Determine total customer value and savings potential
4. COMPETITIVE COMPARISON: Position pricing against market alternatives
5. RECOMMENDATION FORMULATION: Develop optimal pricing strategy
""",
            "scheduling": """  
1. REQUIREMENT ANALYSIS: Understand service scope and time requirements
2. AVAILABILITY ASSESSMENT: Evaluate technician and resource availability
3. OPTIMIZATION EVALUATION: Consider efficiency and customer preference alignment
4. CONSTRAINT CONSIDERATION: Factor in operational and customer limitations
5. RECOMMENDATION DEVELOPMENT: Propose optimal scheduling solution
""",
            "bundle": """
1. SERVICE COMPATIBILITY: Assess technical and operational service alignment
2. VALUE OPPORTUNITY: Identify customer savings and convenience benefits
3. OPERATIONAL SYNERGY: Evaluate efficiency gains and resource optimization
4. PRICING STRATEGY: Develop competitive bundle pricing structure
5. IMPLEMENTATION PLANNING: Design service delivery and customer communication approach
"""
        }
        
        return frameworks.get(analysis_focus, "Standard step-by-step analytical framework")
    
    def _inject_parameters(self, prompt: str, parameters: Dict[str, Any]) -> str:
        """
        Inject parameters into prompt template with error handling
        """
        try:
            for key, value in parameters.items():
                placeholder = "{" + key + "}"
                if placeholder in prompt:
                    if isinstance(value, (dict, list)):
                        formatted_value = json.dumps(value, indent=2)
                    else:
                        formatted_value = str(value)
                    prompt = prompt.replace(placeholder, formatted_value)
            
            # Handle any remaining placeholders
            remaining_placeholders = re.findall(r'\{(\w+)\}', prompt)
            for placeholder in remaining_placeholders:
                prompt = prompt.replace(
                    "{" + placeholder + "}", 
                    f"[NOT_PROVIDED: {placeholder}]"
                )
            
            return prompt
            
        except Exception as e:
            return f"ERROR: Prompt parameter injection failed - {str(e)}\n\nOriginal prompt:\n{prompt}"
    
    def _format_conversation_history(self, history: List[Dict[str, Any]]) -> str:
        """
        Format conversation history for prompt inclusion
        """
        if not history:
            return "No previous conversation"
        
        formatted_history = []
        for msg in history[-5:]:  # Last 5 messages
            role = msg.get('role', 'unknown')
            content = msg.get('content', '')
            timestamp = msg.get('timestamp', '')
            formatted_history.append(f"{role.upper()}: {content}")
        
        return "\n".join(formatted_history)
    
    def _create_context_summary(self, context: WorkflowContext) -> str:
        """
        Create concise context summary for prompt inclusion
        """
        summary_parts = []
        
        if context.extracted_entities.get("service_type"):
            summary_parts.append(f"Service: {context.extracted_entities['service_type']}")
        
        if context.extracted_entities.get("urgency"):
            summary_parts.append(f"Urgency: {context.extracted_entities['urgency']}")
        
        if context.extracted_entities.get("bundle_request"):
            summary_parts.append("Bundle request detected")
        
        if len(context.workflow_steps) > 0:
            summary_parts.append(f"Workflow steps completed: {len(context.workflow_steps)}")
        
        return " | ".join(summary_parts) if summary_parts else "Initial customer contact"
    
    def _adapt_for_urgency(self, prompt: str, context: WorkflowContext) -> str:
        """Adapt prompt for urgent requests"""
        urgency = context.extracted_entities.get("urgency")
        if urgency in ["emergency", "high"]:
            return f"URGENT REQUEST - EXPEDITED PROCESSING REQUIRED\n\n{prompt}"
        return prompt
    
    def _adapt_for_bundle_request(self, prompt: str, context: WorkflowContext) -> str:
        """Adapt prompt for bundle requests"""
        if context.extracted_entities.get("bundle_request"):
            return f"{prompt}\n\nBUNDLE OPTIMIZATION FOCUS: Prioritize service combinations, cost savings, and scheduling efficiency."
        return prompt
    
    def _adapt_for_customer_history(self, prompt: str, context: WorkflowContext) -> str:
        """Adapt prompt based on conversation history"""
        if len(context.conversation_history) > 2:
            return f"ONGOING CONVERSATION CONTEXT: Customer is engaged in detailed service discussion.\n\n{prompt}"
        return prompt
    
    def _adapt_for_complexity(self, prompt: str, context: WorkflowContext) -> str:
        """Adapt prompt for complex service situations"""
        if len(context.workflow_steps) > 2 or len(context.extracted_entities) > 4:
            return f"{prompt}\n\nCOMPLEX SERVICE SITUATION: Apply enhanced analysis and comprehensive solution development."
        return prompt
