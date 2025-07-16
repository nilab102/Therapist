"""
Therapy Agent Manager for OMANI Therapist Voice.
Manages different therapeutic agents with cultural sensitivity and clinical protocols.
"""

from typing import Dict, Any, List, Optional, Callable
from loguru import logger


# Speaking tone and cultural foundation for all therapy agents
Speaking_tone='''
Speaking style:
____________________
Must Follow this instructions:
____________________    
1. You must speak English exactly the way a native Omani Arab would. This includes:

2. Using a gentle Omani Arabic accent while speaking English.

3. Following Omani speech rhythms — slower pace, soft consonants, stretched vowels.

4. Occasionally using Arabic expressions like ‘insha’Allah’, ‘habibi’, ‘masha’Allah’, or ‘ya akhi’ where appropriate.

Every English sentence must be delivered with the intonation, emotion, and voice tone of an Omani Arab therapist — calm, caring, grounded.

⚠️ Important: No matter what you say in English, you must always maintain the Omani Arabic dialect and accent. This is not optional.
Mimic the cultural softness, hospitality, and wisdom in tone that native Omanis naturally express in both Arabic and English.

🎧 Goal: The listener should feel like they're hearing a real Omani therapist — reassuring, respectful, and deeply human."
'''

# General Therapy Agent - Primary therapeutic interface
GENERAL_THERAPY_INSTRUCTION =  """
🎯 ROLE: Primary Therapeutic Support Agent

You are the main therapeutic interface, providing comprehensive mental health support with cultural sensitivity. You can address a wide range of emotional and psychological concerns while maintaining clinical safety.

CAPABILITIES:
- General mental health support and counseling
- Emotional regulation and coping strategies
- Stress and anxiety management
- Depression and mood support
- Relationship and family dynamics (culturally adapted)
- Islamic psychology integration when appropriate
- Crisis detection and appropriate escalation

THERAPEUTIC TOOLS AVAILABLE:
- Crisis detection and safety planning
- CBT techniques adapted for Islamic/Arab culture
- Emotional analysis and pattern recognition
- Session management and documentation

CULTURAL ADAPTATIONS:
- Integrate Islamic concepts (sabr, tawakkul, qadar) when user indicates religious preference
- Respect family dynamics and community expectations
- Understand gender considerations and cultural modesty
- Appreciate the role of extended family and community support
- Recognize cultural stigma around mental health and address it sensitively

CONVERSATION APPROACH:
1. Begin with warm, culturally appropriate greeting
2. Assess immediate safety and emotional state
3. Listen actively with cultural understanding
4. Provide appropriate therapeutic interventions
5. Monitor for crisis indicators throughout
6. Document progress while respecting privacy


Always remember: You're not just providing therapy - you're providing culturally-informed, religiously-sensitive care that honors the user's complete identity. When speaking English, always use authentic Arabic accent and speech patterns.

"""+Speaking_tone

# Crisis Intervention Agent - Specialized for emergency situations
CRISIS_INTERVENTION_INSTRUCTION = """
🚨 ROLE: Crisis Intervention Specialist

You are activated when crisis indicators are detected or when immediate safety concerns arise. Your primary focus is ensuring user safety while providing culturally-sensitive crisis support.

IMMEDIATE PRIORITIES:
1. Assess immediate safety and suicide risk
2. Activate appropriate crisis protocols
3. Provide immediate emotional stabilization
4. Guide user to appropriate emergency resources
5. Involve family/community support when culturally appropriate and safe

CRISIS ASSESSMENT AREAS:
- Suicidal ideation or planning
- Self-harm behaviors or intentions
- Severe emotional distress
- Psychotic symptoms or reality distortion
- Substance abuse emergencies
- Domestic violence or abuse situations

CULTURAL CRISIS CONSIDERATIONS:
- Family involvement: Balance cultural expectations with individual safety
- Religious support: Integrate appropriate Islamic crisis counseling
- Community resources: Know culturally-appropriate local support
- Gender considerations: Respect cultural preferences for same-gender support
- Honor/shame dynamics: Address cultural factors that might prevent help-seeking

CRISIS INTERVENTION TOOLS:
- Risk assessment and safety planning
- Emergency contact activation
- Professional referral protocols
- Cultural family crisis consultation
- Religious/spiritual crisis support

CRISIS RESPONSE PROTOCOL:
1. Immediate safety assessment: "Are you safe right now?"
2. Crisis symptom evaluation: Use crisis detection tools
3. Cultural context assessment: Family, religious, community factors
4. Safety planning: Culturally-adapted crisis plan
5. Resource activation: Emergency services, family, community
6. Follow-up planning: Immediate and ongoing support

EXAMPLE CRISIS OPENING:
"أستطيع أن أسمع أنك تمر بشيء صعب جداً الآن. I can hear that you are going through something very difficult right now, my dear. سلامتك أهم شيء عندي - your safety is my highest priority, ya'ani. أنت لست وحدك، حبيبي/حبيبتي - you are not alone, habibi/habibti. دعنا نعمل سوياً للتأكد من سلامتك. Let's work together to make sure you are safe, wallah. هل أنت في خطر فوري الآن؟ Can you tell me if you are in immediate danger now?"

EMERGENCY RESOURCES TO REFERENCE:
- Omani Emergency Services: 999 (الطوارئ)
- Royal Oman Police: 9999 (شرطة عمان السلطانية)
- Mental Health Services - Ministry of Health Oman
- Islamic counseling through local mosques (الإرشاد الإسلامي)
- Family and tribal support networks (شبكات الدعم العائلية والقبلية)
- Private mental health clinics in Muscat and major cities

CULTURAL CRISIS MESSAGING:
"الله معك في هذه اللحظة الصعبة - Allah is with you in this difficult moment. طلب المساعدة ليس عيباً، بل علامة قوة وحكمة - Seeking help is not shameful, but a sign of strength and wisdom. الرسول (صلى الله عليه وسلم) قال: 'من فرج عن مؤمن كربة من كرب الدنيا فرج الله عنه كربة من كرب يوم القيامة' - The Prophet (peace be upon him) said whoever relieves a believer's distress, Allah will relieve their distress."
"""+Speaking_tone

# CBT Specialist Agent - Focused on cognitive-behavioral interventions
CBT_SPECIALIST_INSTRUCTION = """
🧠 ROLE: Cognitive Behavioral Therapy Specialist

You specialize in providing evidence-based CBT techniques adapted for Islamic and Gulf Arab cultural contexts. You help users identify and change negative thought patterns and behaviors.

CBT SPECIALIZATION AREAS:
- Cognitive restructuring and thought challenging
- Behavioral activation and activity scheduling
- Anxiety and panic management
- Depression treatment using CBT approaches
- Islamic CBT integration (I-CBT)
- Worry and rumination management

ISLAMIC CBT INTEGRATION:
- Tawakkul (trust in Allah) as anxiety management
- Sabr (patience) for distress tolerance
- Shukr (gratitude) for mood improvement
- Istighfar (seeking forgiveness) for guilt and shame
- Qadar (divine decree) for acceptance and peace
- Dhikr (remembrance) for mindfulness and grounding

CULTURAL CBT ADAPTATIONS:
- Family-centered behavioral experiments
- Community-based behavioral activation
- Religious thought challenging that respects faith
- Cultural values integration in goal setting
- Islamic mindfulness and meditation practices

CBT TOOLS AVAILABLE:
- Thought records with cultural questions
- Behavioral activation planning
- Cognitive restructuring worksheets
- Islamic coping strategies
- Gratitude and dhikr practices
- Cultural behavioral experiments

STRUCTURED CBT APPROACH:
1. Psychoeducation about thoughts-feelings-behaviors connection
2. Identification of negative thought patterns (with cultural sensitivity)
3. Cognitive restructuring using Islamic and secular approaches
4. Behavioral experiments and activity scheduling
5. Relapse prevention and coping strategy development

EXAMPLE CBT INTERVENTION:
"تعال نفحص هذه الفكرة سوياً، حبيبي/حبيبتي. Let's examine this thought together. في العلاج المعرفي السلوكي، نتطلع إلى كيف تؤثر أفكارنا على مشاعرنا وأفعالنا. In CBT, we look at how our thoughts affect our feelings and actions. لاحظت أنك قلت [thought]. I notice you said [thought]. دعنا نستكشف هذا: Let's explore this: ما الدليل الذي يدعم هذه الفكرة؟ What evidence supports this thought? ماذا كنت ستقول لأخ مسلم لديه نفس هذه الفكرة؟ What would you tell a fellow Muslim who had this same thought? كيف تتماشى هذه الفكرة مع التعاليم الإسلامية حول حسن الظن بالله؟ How does this thought align with Islamic teachings about having good thoughts about Allah's wisdom?"

ISLAMIC CBT TECHNIQUES (تقنيات العلاج المعرفي الإسلامي):
- Replace catastrophic thoughts with "قدر الله وما شاء فعل" (Allah's decree and what He wills happens) 
- Use "حسبنا الله ونعم الوكيل" for anxiety and worry management
- Apply "الحمد لله رب العالمين" for daily gratitude practice
- Integrate "لا حول ولا قوة إلا بالله" when feeling powerless or overwhelmed
- Use prayer times (أوقات الصلاة) for behavioral activation scheduling
- Practice "استغفار" (seeking forgiveness) for guilt and shame processing
- Use "التوكل على الله" (trust in Allah) as ultimate anxiety management
- Incorporate "الصبر" (patience) training for distress tolerance

OMANI CULTURAL CBT ADAPTATIONS:
- Use majlis (مجلس) discussions as model for thought examination
- Reference Omani proverbs: "الصبر مفتاح الفرج" (patience is the key to relief)
- Integrate family consultation (مشورة العائلة) in goal setting
- Use Omani hospitality customs for behavioral activation
- Reference traditional Omani pearl diving for resilience metaphors
- Incorporate wadi (valley) metaphors for navigating life's ups and downs

Remember: CBT is most effective when it resonates with the user's worldview. Integrate Islamic principles naturally while maintaining therapeutic effectiveness.
"""+Speaking_tone


class TherapyAgentManager:
    """
    Manages different therapeutic agents with cultural sensitivity and clinical protocols.
    
    Provides specialized therapeutic responses based on user needs while maintaining
    cultural appropriateness and clinical safety.
    """
    
    def __init__(self):
        """Initialize the therapy agent manager."""
        self.current_agent = "general_therapy"
        self.agents = {}
        self.agent_instructions = {}
        self.agent_tools = {}
        self.agent_history = []
        self.cultural_context = {}
        self.clinical_state = {}
        
        # Callbacks for system integration
        self.llm_recreate_callback = None
        self.task = None
        
        logger.info("🏥 TherapyAgentManager initialized")
    
    def register_agent(self, agent_name: str, instructions: str, tools: List[Dict], tool_instances: Dict[str, Any]):
        """
        Register a therapeutic agent with its instructions and tools.
        
        Args:
            agent_name: Unique name for the therapeutic agent
            instructions: System instructions for the agent
            tools: List of tool definitions for the agent
            tool_instances: Dictionary of tool instances
        """
        self.agents[agent_name] = {
            "instructions": instructions,
            "tools": tools,
            "tool_instances": tool_instances,
            "specialization": self._get_agent_specialization(agent_name),
            "cultural_adaptations": self._get_cultural_adaptations(agent_name)
        }
        
        self.agent_instructions[agent_name] = instructions
        self.agent_tools[agent_name] = tool_instances
        
        logger.info(f"🏥 Registered therapeutic agent: {agent_name}")
    
    def _get_agent_specialization(self, agent_name: str) -> str:
        """Get the specialization description for an agent."""
        specializations = {
            "general_therapy": "Comprehensive mental health support with cultural sensitivity",
            "crisis_intervention": "Emergency crisis intervention and safety management",
            "cbt_specialist": "Cognitive Behavioral Therapy with Islamic integration"
        }
        return specializations.get(agent_name, "Specialized therapeutic support")
    
    def _get_cultural_adaptations(self, agent_name: str) -> List[str]:
        """Get cultural adaptations for an agent."""
        adaptations = {
            "general_therapy": [
                "Gulf Arabic cultural understanding",
                "Islamic values integration",
                "Family dynamics consideration",
                "Community support recognition"
            ],
            "crisis_intervention": [
                "Cultural crisis protocols",
                "Family involvement in emergencies",
                "Religious crisis support",
                "Community resource activation"
            ],
            "cbt_specialist": [
                "Islamic CBT (I-CBT) techniques",
                "Religious thought integration",
                "Cultural behavioral experiments",
                "Community-based interventions"
            ]
        }
        return adaptations.get(agent_name, ["Cultural sensitivity"])
    
    async def switch_agent(self, target_agent: str, reason: str = "", cultural_context: Dict[str, Any] = None) -> str:
        """
        Switch to a different therapeutic agent based on clinical needs.
        
        Args:
            target_agent: Name of the agent to switch to
            reason: Reason for the switch
            cultural_context: Cultural context for the switch
            
        Returns:
            Response message about the agent switch
        """
        if target_agent not in self.agents:
            available_agents = list(self.agents.keys())
            return f"Therapeutic agent '{target_agent}' not available. Available: {', '.join(available_agents)}"
        
        if target_agent == self.current_agent:
            return f"Already using {target_agent} agent."
        
        # Store agent history
        switch_record = {
            "timestamp": self._get_timestamp(),
            "from_agent": self.current_agent,
            "to_agent": target_agent,
            "reason": reason,
            "cultural_context": cultural_context or {},
            "clinical_state": self.clinical_state.copy()
        }
        self.agent_history.append(switch_record)
        
        # Update cultural context
        if cultural_context:
            self.cultural_context.update(cultural_context)
        
        previous_agent = self.current_agent
        self.current_agent = target_agent
        
        # Get agent configuration
        agent_config = self.agents[target_agent]
        
        logger.info(f"🏥 Switching from {previous_agent} to {target_agent} agent. Reason: {reason}")
        
        # Recreate LLM with new agent instructions if callback available
        if self.llm_recreate_callback:
            try:
                await self.llm_recreate_callback(
                    agent_config["instructions"],
                    agent_config["tools"]
                )
                logger.info(f"✅ LLM recreated for {target_agent} agent")
            except Exception as e:
                logger.error(f"❌ Error recreating LLM for {target_agent}: {e}")
        
        # Generate culturally appropriate switch message
        switch_message = await self._generate_agent_switch_message(
            previous_agent, target_agent, reason, cultural_context
        )
        
        return switch_message
    
    async def _generate_agent_switch_message(self, from_agent: str, to_agent: str, reason: str, cultural_context: Dict[str, Any]) -> str:
        """Generate culturally appropriate agent switch message."""
        
        agent_descriptions = {
            "general_therapy": "your primary therapist",
            "crisis_intervention": "crisis intervention specialist", 
            "cbt_specialist": "cognitive behavioral therapy specialist"
        }
        
        from_desc = agent_descriptions.get(from_agent, from_agent)
        to_desc = agent_descriptions.get(to_agent, to_agent)
        
        # Base message
        if cultural_context and cultural_context.get("preferred_language") == "arabic":
            base_message = f"سأقوم بتحويلك إلى {to_desc} للحصول على الدعم المتخصص."
            base_message += f"\nI'm connecting you with {to_desc} for specialized support."
        else:
            base_message = f"I'm connecting you with {to_desc} for specialized support."
        
        # Add reason if provided
        if reason:
            base_message += f"\n\nReason for this change: {reason}"
        
        # Add cultural comfort
        if cultural_context and cultural_context.get("religious_considerations"):
            base_message += "\n\nإن شاء الله، ستجد الدعم المناسب مع هذا التخصص."
            base_message += "\nInsha'Allah, you will find the appropriate support with this specialization."
        
        # Agent-specific transitions
        if to_agent == "crisis_intervention":
            base_message += "\n\n🚨 Crisis support activated. Your safety is the priority."
            base_message += "\nأنت لست وحدك. نحن هنا لمساعدتك. (You are not alone. We are here to help you.)"
        
        elif to_agent == "cbt_specialist":
            base_message += "\n\n🧠 CBT specialist ready to help with thought patterns and coping strategies."
            if cultural_context and cultural_context.get("religious_considerations"):
                base_message += "\nWe'll integrate Islamic principles with evidence-based therapy techniques."
        
        elif to_agent == "general_therapy":
            base_message += "\n\n💬 Back to general therapeutic support for comprehensive care."
        
        return base_message
    
    async def handle_function_call(self, function_call) -> str:
        """
        Handle function calls from the current therapeutic agent.
        
        Args:
            function_call: Function call object with name and arguments
            
        Returns:
            Result of the function call
        """
        try:
            function_name = function_call.name
            arguments = function_call.arguments
            
            logger.info(f"🏥 Handling function call: {function_name} for agent: {self.current_agent}")
            logger.debug(f"🏥 Function arguments: {arguments}")
            
            # Get current agent's tools
            current_tools = self.agent_tools.get(self.current_agent, {})
            
            # Route function calls to appropriate tools with proper parameter mapping
            if function_name == "detect_crisis":
                if "crisis_detection" in current_tools:
                    action = arguments.get("action", "assess_risk")
                    filtered_args = {k: v for k, v in arguments.items() if k != "action"}
                    return await current_tools["crisis_detection"].execute(action, **filtered_args)
                else:
                    return "Crisis detection tool not available for current agent"
            
            elif function_name == "apply_cbt_technique":
                if "cbt_techniques" in current_tools:
                    technique = arguments.get("technique", arguments.get("action", "thought_challenging"))
                    filtered_args = {k: v for k, v in arguments.items() if k not in ["technique", "action"]}
                    return await current_tools["cbt_techniques"].execute(technique, **filtered_args)
                else:
                    return "CBT techniques tool not available for current agent"
            
            elif function_name == "analyze_emotion":
                if "emotional_analysis" in current_tools:
                    analysis_type = arguments.get("analysis_type", arguments.get("action", "detect_emotions"))
                    filtered_args = {k: v for k, v in arguments.items() if k not in ["analysis_type", "action"]}
                    return await current_tools["emotional_analysis"].execute(analysis_type, **filtered_args)
                else:
                    return "Emotional analysis tool not available for current agent"
            
            elif function_name == "manage_session":
                if "session_management" in current_tools:
                    action = arguments.get("action", "update_progress")
                    filtered_args = {k: v for k, v in arguments.items() if k != "action"}
                    return await current_tools["session_management"].execute(action, **filtered_args)
                else:
                    return "Session management tool not available for current agent"
            
            else:
                logger.warning(f"🏥 Unknown function call: {function_name}")
                return f"Unknown therapeutic function: {function_name}. Available functions: detect_crisis, apply_cbt_technique, analyze_emotion, manage_session"
        
        except Exception as e:
            logger.error(f"🏥 Error handling function call {function_call.name}: {e}")
            return f"Error executing therapeutic function: {str(e)}"
    
    async def handle_crisis_escalation(self, crisis_type: str, crisis_data: Dict[str, Any]) -> str:
        """
        Handle crisis escalation by switching to crisis intervention agent.
        
        Args:
            crisis_type: Type of crisis detected
            crisis_data: Crisis-related data
            
        Returns:
            Crisis response message
        """
        # Update clinical state
        self.clinical_state.update({
            "crisis_active": True,
            "crisis_type": crisis_type,
            "crisis_data": crisis_data,
            "crisis_timestamp": self._get_timestamp()
        })
        
        # Switch to crisis intervention agent if not already active
        if self.current_agent != "crisis_intervention":
            switch_reason = f"Crisis escalation: {crisis_type}"
            return await self.switch_agent("crisis_intervention", switch_reason, self.cultural_context)
        
        return "Crisis intervention agent already active and handling the situation."
    
    def get_current_agent_info(self) -> Dict[str, Any]:
        """Get information about the current therapeutic agent."""
        if self.current_agent not in self.agents:
            return {"error": "No current agent set"}
        
        agent_config = self.agents[self.current_agent]
        return {
            "current_agent": self.current_agent,
            "specialization": agent_config["specialization"],
            "cultural_adaptations": agent_config["cultural_adaptations"],
            "available_tools": list(agent_config["tool_instances"].keys()),
            "clinical_state": self.clinical_state,
            "cultural_context": self.cultural_context
        }
    
    def get_agent_history(self) -> List[Dict[str, Any]]:
        """Get the history of agent switches."""
        return self.agent_history.copy()
    
    def update_cultural_context(self, cultural_updates: Dict[str, Any]):
        """Update cultural context for all agents."""
        self.cultural_context.update(cultural_updates)
        logger.info(f"🏥 Updated cultural context: {cultural_updates}")
    
    def update_clinical_state(self, clinical_updates: Dict[str, Any]):
        """Update clinical state information."""
        self.clinical_state.update(clinical_updates)
        logger.info(f"🏥 Updated clinical state: {clinical_updates}")
    
    def get_recommended_agent(self, user_input: str, current_state: Dict[str, Any]) -> str:
        """
        Recommend the most appropriate therapeutic agent based on user input and state.
        
        Args:
            user_input: User's recent input
            current_state: Current therapeutic state
            
        Returns:
            Recommended agent name
        """
        # Handle None or empty user_input
        if not user_input:
            return "general_therapy"
        
        # Crisis indicators - prioritize crisis intervention
        crisis_keywords = [
            "suicide", "kill myself", "end it all", "hurt myself", "انتحار", "اقتل نفسي"
        ]
        
        input_lower = user_input.lower()
        if any(keyword in input_lower for keyword in crisis_keywords):
            return "crisis_intervention"
        
        # High anxiety/panic - might benefit from CBT
        anxiety_keywords = [
            "panic", "anxiety", "worried", "stressed", "overthinking", "قلق", "متوتر", "خايف"
        ]
        
        if any(keyword in input_lower for keyword in anxiety_keywords):
            # If already in crisis mode, stay there
            if current_state.get("crisis_active"):
                return "crisis_intervention"
            else:
                return "cbt_specialist"
        
        # Thought patterns and cognitive issues - CBT specialist
        cognitive_keywords = [
            "thoughts", "thinking", "can't stop", "ruminating", "negative thoughts", "أفكار"
        ]
        
        if any(keyword in input_lower for keyword in cognitive_keywords):
            return "cbt_specialist"
        
        # Default to general therapy for comprehensive support
        return "general_therapy"
    
    def _get_timestamp(self) -> str:
        """Get current timestamp for logging."""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status for therapeutic agents."""
        return {
            "current_agent": self.current_agent,
            "available_agents": list(self.agents.keys()),
            "agent_switches_count": len(self.agent_history),
            "crisis_active": self.clinical_state.get("crisis_active", False),
            "cultural_context_set": bool(self.cultural_context),
            "total_registered_agents": len(self.agents),
            "clinical_state": self.clinical_state,
            "cultural_adaptations_active": self.cultural_context
        } 