"""
Agent Orchestration System for OnePath Service Platform
Manages multi-agent workflows, dynamic decision making, and error handling

Key Features:
- Multi-agent coordination and chaining
- Dynamic workflow management
- Context-aware decision routing
- Error recovery and resilience
- Microservice pattern implementation
"""

import asyncio
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional
from service_models import (
    ServiceRequest, AgentResponse, WorkflowContext, WorkflowStep, 
    ActionType, FollowUpRequest
)
from react_agent import ReACTAgent
from prompt_composer import PromptComposer, PromptType, ConversationState


class AgentOrchestrator:
    """
    Central orchestrator managing agent workflows and service dispatch
    
    This class implements microservice patterns for:
    - Agent specialization and coordination
    - Dynamic workflow routing
    - Context preservation across agent handoffs
    - Error handling and recovery
    - Performance monitoring and optimization
    """
    
    def __init__(self):
        self.active_workflows = {}
        self.agent_registry = self._initialize_agents()
        self.prompt_composer = PromptComposer()
        self.conversation_states = {}
        self.performance_metrics = {
            "total_requests": 0,
            "successful_completions": 0,
            "error_count": 0,
            "average_confidence": 0.0
        }
    
    def _initialize_agents(self) -> Dict[str, ReACTAgent]:
        """
        Initialize specialized agents for different service aspects
        """
        return {
            "primary_dispatcher": ReACTAgent("PrimaryDispatcher", "general_service_analysis"),
            "calendar_specialist": ReACTAgent("CalendarSpecialist", "scheduling_optimization"),
            "pricing_analyst": ReACTAgent("PricingAnalyst", "cost_analysis_and_optimization"),
            "bundle_optimizer": ReACTAgent("BundleOptimizer", "multi_service_coordination"),
            "customer_relations": ReACTAgent("CustomerRelations", "communication_and_followup"),
            "error_recovery": ReACTAgent("ErrorRecovery", "issue_resolution_and_recovery")
        }
    
    async def process_service_request(self, request: ServiceRequest) -> AgentResponse:
        """
        Main entry point for service request processing
        
        Implements complete workflow orchestration:
        1. Request initialization and context creation
        2. Primary agent analysis and routing decision
        3. Specialized agent chain execution
        4. Result synthesis and response generation
        5. Context preservation for follow-ups
        """
        
        request_id = str(uuid.uuid4())
        print(f"\n🚀 ORCHESTRATOR: Processing service request {request_id}")
        print(f"Customer Message: '{request.message}'")
        
        try:
            # Initialize workflow context
            workflow_context = await self._initialize_workflow_context(request_id, request)
            
            # Store active workflow
            self.active_workflows[request_id] = workflow_context
            self.conversation_states[request_id] = ConversationState()
            self.conversation_states[request_id].add_message("user", request.message)
            
            # Update performance metrics
            self.performance_metrics["total_requests"] += 1
            
            # Primary agent analysis
            print("\n📋 PHASE 1: Primary Analysis")
            primary_result = await self._execute_primary_analysis(workflow_context)
            
            # Determine and execute agent chain
            print("\n🔗 PHASE 2: Agent Chain Execution")
            chain_result = await self._execute_agent_chain(workflow_context, primary_result)
            
            # Synthesize final response
            print("\n📊 PHASE 3: Response Synthesis")
            final_response = await self._synthesize_response(
                request_id, 
                workflow_context, 
                primary_result, 
                chain_result
            )
            
            # Update workflow status
            workflow_context.status = "completed"
            self.performance_metrics["successful_completions"] += 1
            
            print(f"✅ ORCHESTRATOR: Request {request_id} completed successfully")
            return final_response
            
        except Exception as e:
            print(f"❌ ORCHESTRATOR: Error processing request {request_id}: {str(e)}")
            return await self._handle_orchestration_error(request_id, request, str(e))
    
    async def handle_followup_request(self, followup: FollowUpRequest) -> AgentResponse:
        """
        Handle customer follow-up requests with context preservation
        
        This demonstrates conversation continuity and context-aware processing:
        1. Retrieve existing workflow context
        2. Update context with new information
        3. Determine appropriate agent for follow-up handling
        4. Execute follow-up processing with full context
        5. Update workflow state and preserve context
        """
        
        print(f"\n🔄 ORCHESTRATOR: Processing follow-up for {followup.request_id}")
        print(f"Follow-up Message: '{followup.message}'")
        
        if followup.request_id not in self.active_workflows:
            raise ValueError(f"Workflow {followup.request_id} not found")
        
        try:
            # Retrieve and update context
            workflow_context = self.active_workflows[followup.request_id]
            conversation_state = self.conversation_states[followup.request_id]
            
            # Add follow-up to conversation
            conversation_state.add_message("user", followup.message)
            workflow_context.conversation_history.append({
                "role": "user",
                "content": followup.message,
                "timestamp": datetime.now().isoformat()
            })
            
            # Analyze follow-up intent and requirements
            print("\n🧠 FOLLOWUP ANALYSIS: Determining intent and routing")
            followup_analysis = await self._analyze_followup_intent(workflow_context, followup.message)
            
            # Route to appropriate specialized agent
            agent_name = followup_analysis["recommended_agent"]
            specialized_agent = self.agent_registry[agent_name]
            
            print(f"🎯 FOLLOWUP ROUTING: Routing to {agent_name}")
            
            # Execute follow-up processing
            followup_result = await specialized_agent.think_and_act(
                workflow_context,
                specific_goal=followup_analysis["specific_goal"]
            )
            
            # Generate follow-up response
            response = AgentResponse(
                request_id=followup.request_id,
                agent_name="OrchestrationEngine",
                reasoning=f"Follow-up processed by {agent_name}: {followup_analysis['reasoning']}",
                actions_taken=[f"followup_analysis", f"{agent_name}_processing"],
                result={
                    "followup_analysis": followup_analysis,
                    "agent_result": followup_result,
                    "context_preserved": True
                },
                next_steps=self._determine_followup_next_steps(followup_result),
                confidence=followup_result.get("confidence", 0.8),
                timestamp=datetime.now()
            )
            
            # Update workflow context
            workflow_context.workflow_steps.append(WorkflowStep(
                step_id=str(uuid.uuid4()),
                agent_name=response.agent_name,
                action_type=ActionType.CUSTOMER_FOLLOWUP,
                input_data={"followup_message": followup.message},
                output_data=response.result,
                status="completed",
                confidence=response.confidence,
                timestamp=datetime.now()
            ))
            
            print(f"✅ ORCHESTRATOR: Follow-up {followup.request_id} processed successfully")
            return response
        
        except Exception as e:
            print(f"❌ ORCHESTRATOR: Error processing follow-up {followup.request_id}: {str(e)}")
            return await self._handle_followup_error(followup, str(e))
    
    async def _initialize_workflow_context(self, 
                                         request_id: str, 
                                         request: ServiceRequest) -> WorkflowContext:
        """
        Initialize comprehensive workflow context
        """
        
        # Extract entities from customer message
        extracted_entities = await self._extract_entities_from_message(request.message)
        
        context = WorkflowContext(
            request_id=request_id,
            customer_message=request.message,
            extracted_entities=extracted_entities,
            conversation_history=[{
                "role": "user",
                "content": request.message,
                "timestamp": datetime.now().isoformat(),
                "metadata": {
                    "customer_id": request.customer_id,
                    "location": request.location,
                    "preferred_time": request.preferred_time
                }
            }],
            workflow_steps=[],
            current_step=0,
            status="initializing"
        )
        
        print(f"🏗️ CONTEXT INITIALIZED: {len(extracted_entities)} entities extracted")
        return context
    
    async def _extract_entities_from_message(self, message: str) -> Dict[str, Any]:
        """
        Extract structured entities from customer message
        """
        
        entities = {}
        message_lower = message.lower()
        
        # Service type detection
        service_patterns = {
            "ac_repair": ["ac", "air conditioning", "cooling", "hvac", "conditioner"],
            "heating": ["heat", "heating", "furnace", "boiler", "warm"],
            "plumbing": ["plumb", "water", "leak", "pipe", "drain", "toilet"],
            "electrical": ["electric", "power", "outlet", "wiring", "lights"]
        }
        
        for service, patterns in service_patterns.items():
            if any(pattern in message_lower for pattern in patterns):
                entities["service_type"] = service
                break
        
        # Urgency level detection
        urgency_patterns = {
            "emergency": ["emergency", "urgent", "asap", "immediately", "broken", "not working", "dead"],
            "high": ["this week", "soon", "quickly", "today", "tomorrow"],
            "normal": ["convenient", "schedule", "when possible"],
            "low": ["whenever", "no rush", "flexible"]
        }
        
        for urgency, patterns in urgency_patterns.items():
            if any(pattern in message_lower for pattern in patterns):
                entities["urgency"] = urgency
                break
        
        # Bundle request detection
        bundle_indicators = ["add", "also", "too", "bundle", "package", "plus", "include"]
        if any(indicator in message_lower for indicator in bundle_indicators):
            entities["bundle_request"] = True
        
        # Pricing request detection
        pricing_indicators = ["cost", "price", "how much", "quote", "estimate", "expensive"]
        if any(indicator in message_lower for indicator in pricing_indicators):
            entities["pricing_request"] = True
        
        # Scheduling request detection
        schedule_indicators = ["when", "schedule", "appointment", "time", "available"]
        if any(indicator in message_lower for indicator in schedule_indicators):
            entities["scheduling_request"] = True
        
        return entities
    
    async def _execute_primary_analysis(self, context: WorkflowContext) -> Dict[str, Any]:
        """
        Execute primary agent analysis to determine workflow routing
        """
        
        primary_agent = self.agent_registry["primary_dispatcher"]
        
        # Generate context-aware reasoning prompt
        reasoning_prompt = self.prompt_composer.compose_react_prompt(
            context,
            "initial_analysis",
            "determine_optimal_service_workflow"
        )
        
        print("🤔 PRIMARY AGENT: Executing ReACT reasoning")
        print(f"Context: {list(context.extracted_entities.keys())}")
        
        # Execute primary reasoning
        primary_result = await primary_agent.think_and_act(
            context,
            "analyze_customer_request_and_determine_workflow"
        )
        
        # Update workflow context
        context.workflow_steps.append(WorkflowStep(
            step_id=str(uuid.uuid4()),
            agent_name="primary_dispatcher",
            action_type=ActionType.REASON,
            input_data={"customer_message": context.customer_message},
            output_data=primary_result,
            status="completed",
            confidence=primary_result.get("confidence", 0.7),
            timestamp=datetime.now()
        ))
        
        context.current_step += 1
        
        print(f"✅ PRIMARY ANALYSIS: Confidence {primary_result.get('confidence', 0.7):.2f}")
        return primary_result
    
    async def _execute_agent_chain(self, 
                                 context: WorkflowContext, 
                                 primary_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute specialized agent chain based on primary analysis
        """
        
        chain_results = {}
        
        # Determine required agent chain
        agent_chain = self._determine_agent_chain(primary_result, context.extracted_entities)
        
        print(f"🔗 AGENT CHAIN: {' → '.join(agent_chain)}")
        
        # Execute each agent in the chain
        for agent_name in agent_chain:
            print(f"\n🎯 EXECUTING: {agent_name}")
            
            try:
                specialized_agent = self.agent_registry[agent_name]
                agent_goal = self._determine_agent_goal(agent_name, context.extracted_entities)
                
                # Execute specialized agent
                agent_result = await specialized_agent.think_and_act(context, agent_goal)
                
                # Store result
                chain_results[agent_name] = agent_result
                
                # Update workflow context
                context.workflow_steps.append(WorkflowStep(
                    step_id=str(uuid.uuid4()),
                    agent_name=agent_name,
                    action_type=self._map_agent_to_action(agent_name),
                    input_data={"goal": agent_goal, "context": context.extracted_entities},
                    output_data=agent_result,
                    status="completed",
                    confidence=agent_result.get("confidence", 0.7),
                    timestamp=datetime.now()
                ))
                
                context.current_step += 1
                
                print(f"✅ {agent_name}: Completed with confidence {agent_result.get('confidence', 0.7):.2f}")
                
            except Exception as e:
                print(f"❌ {agent_name}: Failed with error {str(e)}")
                # Continue with other agents in chain
                chain_results[agent_name] = {"error": str(e), "confidence": 0.0}
        
        return chain_results
    
    def _determine_agent_chain(self, 
                             primary_result: Dict[str, Any], 
                             entities: Dict[str, Any]) -> List[str]:
        """
        Determine optimal agent chain based on analysis
        """
        
        chain = []
        
        # Always include customer relations for communication
        chain.append("customer_relations")
        
        # Add bundle optimizer if bundle request detected
        if entities.get("bundle_request"):
            chain.append("bundle_optimizer")
        
        # Add calendar specialist if scheduling needed
        if entities.get("scheduling_request") or entities.get("urgency") in ["emergency", "high"]:
            chain.append("calendar_specialist")
        
        # Add pricing analyst if pricing requested or bundle analysis done
        if entities.get("pricing_request") or "bundle_optimizer" in chain:
            chain.append("pricing_analyst")
        
        return chain
    
    def _determine_agent_goal(self, agent_name: str, entities: Dict[str, Any]) -> str:
        """
        Determine specific goal for each agent
        """
        
        goals = {
            "customer_relations": "generate_helpful_response_and_next_steps",
            "calendar_specialist": f"find_optimal_appointment_slots_for_{entities.get('service_type', 'general')}_service",
            "pricing_analyst": f"calculate_accurate_pricing_for_{entities.get('service_type', 'general')}_with_transparency",
            "bundle_optimizer": "identify_and_optimize_multi_service_opportunities"
        }
        
        return goals.get(agent_name, "provide_specialized_analysis")
    
    def _map_agent_to_action(self, agent_name: str) -> ActionType:
        """
        Map agent names to action types
        """
        
        mapping = {
            "customer_relations": ActionType.CUSTOMER_FOLLOWUP,
            "calendar_specialist": ActionType.CALENDAR_CHECK,
            "pricing_analyst": ActionType.PRICING_QUERY,
            "bundle_optimizer": ActionType.BUNDLE_ANALYSIS
        }
        
        return mapping.get(agent_name, ActionType.REASON)
    
    async def _synthesize_response(self, 
                                 request_id: str,
                                 context: WorkflowContext,
                                 primary_result: Dict[str, Any],
                                 chain_results: Dict[str, Any]) -> AgentResponse:
        """
        Synthesize final response from all agent results
        """
        
        print("🎯 SYNTHESIS: Combining agent results")
        
        # Aggregate actions taken
        actions_taken = ["primary_analysis"]
        for agent_name in chain_results.keys():
            actions_taken.append(f"{agent_name}_processing")
        
        # Combine results
        combined_result = {
            "primary_analysis": primary_result,
            "specialized_results": chain_results,
            "workflow_summary": {
                "total_steps": len(context.workflow_steps),
                "agents_involved": list(chain_results.keys()),
                "context_entities": context.extracted_entities
            }
        }
        
        # Calculate overall confidence
        confidences = [primary_result.get("confidence", 0.7)]
        for result in chain_results.values():
            if isinstance(result, dict) and "confidence" in result:
                confidences.append(result["confidence"])
        
        overall_confidence = sum(confidences) / len(confidences) if confidences else 0.5
        self.performance_metrics["average_confidence"] = overall_confidence
        
        # Determine next steps
        next_steps = self._synthesize_next_steps(chain_results, context.extracted_entities)
        
        # Generate reasoning summary
        reasoning_summary = self._generate_reasoning_summary(primary_result, chain_results)
        
        return AgentResponse(
            request_id=request_id,
            agent_name="OrchestrationEngine",
            reasoning=reasoning_summary,
            actions_taken=actions_taken,
            result=combined_result,
            next_steps=next_steps,
            confidence=overall_confidence,
            timestamp=datetime.now()
        )
    
    def _synthesize_next_steps(self, 
                             chain_results: Dict[str, Any], 
                             entities: Dict[str, Any]) -> List[str]:
        """
        Determine comprehensive next steps from all agent results
        """
        
        next_steps = []
        
        # From calendar specialist
        if "calendar_specialist" in chain_results:
            calendar_result = chain_results["calendar_specialist"]
            if calendar_result.get("action_result", {}).get("available_slots"):
                next_steps.append("Select preferred appointment time from available slots")
        
        # From pricing analyst
        if "pricing_analyst" in chain_results:
            pricing_result = chain_results["pricing_analyst"]
            if pricing_result.get("action_result", {}).get("total"):
                next_steps.append("Review service pricing and confirm booking")
        
        # From bundle optimizer
        if "bundle_optimizer" in chain_results:
            bundle_result = chain_results["bundle_optimizer"]
            if bundle_result.get("action_result", {}).get("savings", 0) > 0:
                next_steps.append("Consider bundle services for additional savings")
        
        # Default next steps
        if not next_steps:
            next_steps = [
                "Provide any additional requirements",
                "Confirm service details and preferences",
                "Schedule appointment when ready"
            ]
        
        return next_steps
    
    def _generate_reasoning_summary(self, 
                                  primary_result: Dict[str, Any], 
                                  chain_results: Dict[str, Any]) -> str:
        """
        Generate comprehensive reasoning summary
        """
        
        summary_parts = []
        
        # Primary analysis
        if "reasoning" in primary_result:
            summary_parts.append(f"Primary Analysis: {primary_result['reasoning'].get('analysis', 'Completed')}")
        
        # Specialized agent contributions
        for agent_name, result in chain_results.items():
            if isinstance(result, dict) and "reasoning" in result:
                summary_parts.append(f"{agent_name}: {result['reasoning'].get('analysis', 'Processed')}")
        
        return " | ".join(summary_parts)
    
    async def _analyze_followup_intent(self, 
                                     context: WorkflowContext, 
                                     followup_message: str) -> Dict[str, Any]:
        """
        Analyze follow-up message intent and determine routing
        """
        
        followup_lower = followup_message.lower()
        
        # Intent analysis
        intent_patterns = {
            "bundle_request": ["add", "also", "too", "bundle", "include", "plus"],
            "pricing_query": ["cost", "price", "how much", "quote", "expensive"],
            "scheduling_change": ["reschedule", "change time", "different day", "earlier", "later"],
            "service_modification": ["change", "different", "instead", "modify"],
            "clarification": ["what", "how", "when", "why", "explain"]
        }
        
        detected_intent = "general_followup"
        for intent, patterns in intent_patterns.items():
            if any(pattern in followup_lower for pattern in patterns):
                detected_intent = intent
                break
        
        # Agent routing logic
        agent_routing = {
            "bundle_request": "bundle_optimizer",
            "pricing_query": "pricing_analyst", 
            "scheduling_change": "calendar_specialist",
            "service_modification": "primary_dispatcher",
            "clarification": "customer_relations",
            "general_followup": "customer_relations"
        }
        
        recommended_agent = agent_routing[detected_intent]
        
        # Goal determination
        goal_mapping = {
            "bundle_request": "analyze_additional_service_bundle_opportunities",
            "pricing_query": "provide_detailed_pricing_breakdown_and_options",
            "scheduling_change": "find_alternative_appointment_slots",
            "service_modification": "reassess_service_requirements_and_options",
            "clarification": "provide_clear_explanation_and_guidance",
            "general_followup": "address_customer_concerns_and_provide_assistance"
        }
        
        specific_goal = goal_mapping[detected_intent]
        
        return {
            "detected_intent": detected_intent,
            "recommended_agent": recommended_agent,
            "specific_goal": specific_goal,
            "reasoning": f"Followup analysis detected {detected_intent}, routing to {recommended_agent}",
            "confidence": 0.85
        }
    
    def _determine_followup_next_steps(self, followup_result: Dict[str, Any]) -> List[str]:
        """
        Determine next steps from follow-up processing
        """
        
        if followup_result.get("needs_continuation"):
            return [
                "Review updated information and options",
                "Confirm preferences and requirements",
                "Proceed with service booking when ready"
            ]
        else:
            return [
                "All requirements addressed",
                "Ready to proceed with service booking",
                "Contact us for any additional questions"
            ]
    
    async def _handle_orchestration_error(self, 
                                        request_id: str, 
                                        request: ServiceRequest, 
                                        error_message: str) -> AgentResponse:
        """
        Handle orchestration-level errors with graceful recovery
        """
        
        print(f"🚨 ERROR RECOVERY: Handling orchestration error for {request_id}")
        
        # Update error metrics
        self.performance_metrics["error_count"] += 1
        
        try:
            # Use error recovery agent
            error_recovery_agent = self.agent_registry["error_recovery"]
            
            # Create minimal context for error recovery
            error_context = WorkflowContext(
                request_id=request_id,
                customer_message=request.message,
                extracted_entities={"error_occurred": True},
                conversation_history=[],
                workflow_steps=[],
                current_step=0,
                status="error_recovery",
                error_message=error_message
            )
            
            # Execute error recovery
            recovery_result = await error_recovery_agent.think_and_act(
                error_context,
                "recover_from_orchestration_error_and_assist_customer"
            )
            
            return AgentResponse(
                request_id=request_id,
                agent_name="ErrorRecoverySystem",
                reasoning=f"Error recovery executed: {recovery_result.get('reasoning', {}).get('analysis', 'System error handled')}",
                actions_taken=["error_detection", "recovery_processing", "customer_assistance"],
                result={
                    "error_recovery": recovery_result,
                    "original_error": error_message,
                    "recovery_status": "partial_recovery_achieved"
                },
                next_steps=[
                    "Contact customer service for additional assistance",
                    "Retry request with simplified requirements",
                    "Provide direct contact information for immediate help"
                ],
                confidence=0.6,
                timestamp=datetime.now()
            )
            
        except Exception as recovery_error:
            # Fallback error response
            return AgentResponse(
                request_id=request_id,
                agent_name="FallbackErrorHandler",
                reasoning=f"System encountered an error: {error_message}. Recovery also failed: {str(recovery_error)}",
                actions_taken=["error_detection", "fallback_response"],
                result={
                    "error_message": error_message,
                    "recovery_error": str(recovery_error),
                    "status": "fallback_response_activated"
                },
                next_steps=[
                    "Please contact our customer service team directly",
                    "Provide your request details to our support staff",
                    "We apologize for the technical difficulty"
                ],
                confidence=0.3,
                timestamp=datetime.now()
            )
    
    async def _handle_followup_error(self, 
                                   followup: FollowUpRequest, 
                                   error_message: str) -> AgentResponse:
        """
        Handle follow-up processing errors
        """
        
        return AgentResponse(
            request_id=followup.request_id,
            agent_name="FollowupErrorHandler",
            reasoning=f"Follow-up processing error: {error_message}",
            actions_taken=["error_detection", "followup_error_handling"],
            result={
                "error_message": error_message,
                "followup_message": followup.message,
                "status": "followup_error_handled"
            },
            next_steps=[
                "Please rephrase your request",
                "Contact support for assistance",
                "Try again with simpler language"
            ],
            confidence=0.4,
            timestamp=datetime.now()
        )
    
    def get_workflow_status(self, request_id: str) -> Optional[Dict[str, Any]]:
        """
        Get current status of a workflow
        """
        
        if request_id not in self.active_workflows:
            return None
        
        context = self.active_workflows[request_id]
        
        return {
            "request_id": request_id,
            "status": context.status,
            "current_step": context.current_step,
            "total_steps": len(context.workflow_steps),
            "agents_involved": list(set(step.agent_name for step in context.workflow_steps)),
            "error_message": context.error_message,
            "last_updated": context.workflow_steps[-1].timestamp if context.workflow_steps else datetime.now()
        }
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """
        Get orchestrator performance metrics
        """
        
        success_rate = (
            self.performance_metrics["successful_completions"] / 
            max(1, self.performance_metrics["total_requests"])
        ) * 100
        
        error_rate = (
            self.performance_metrics["error_count"] / 
            max(1, self.performance_metrics["total_requests"])
        ) * 100
        
        return {
            **self.performance_metrics,
            "success_rate": round(success_rate, 2),
            "error_rate": round(error_rate, 2),
            "active_workflows": len(self.active_workflows),
            "available_agents": list(self.agent_registry.keys())
        }
