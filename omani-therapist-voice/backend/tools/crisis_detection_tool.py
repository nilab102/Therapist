"""
Crisis Detection Tool for OMANI Therapist Voice.
Monitors for suicide risk, self-harm, and mental health emergencies.
"""

import re
from typing import Dict, Any, List
from loguru import logger
from pipecat.adapters.schemas.function_schema import FunctionSchema
from .base_tool import BaseTool


class CrisisDetectionTool(BaseTool):
    """
    Crisis detection and intervention tool for therapeutic sessions.
    
    Features:
    - Suicide risk assessment
    - Self-harm detection
    - Emergency escalation protocols
    - Cultural sensitivity for Gulf Arabic context
    - Immediate safety planning
    """
    
    def __init__(self, rtvi_processor, task=None):
        """Initialize crisis detection tool."""
        super().__init__(rtvi_processor, task)
        
        # Crisis severity levels
        self.SEVERITY_LEVELS = {
            "low": 1,
            "moderate": 2,
            "high": 3,
            "imminent": 4
        }
        
        # Crisis tracking
        self.current_risk_level = "low"
        self.crisis_indicators = []
        self.safety_plan_created = False
        self.emergency_contacts_available = False
        
        # Cultural context
        self.cultural_adaptations = {
            "family_involvement": False,
            "religious_considerations": False,
            "community_support": False
        }
        
        logger.info("🚨 Crisis Detection Tool initialized")
    
    def get_tool_definition(self) -> FunctionSchema:
        """Define the crisis detection tool for LLM function calling."""
        return FunctionSchema(
            name="detect_crisis",
            description="Monitor and respond to mental health crises, suicide risk, and emergency situations with cultural sensitivity",
            properties={
                "action": {
                    "type": "string",
                    "enum": [
                        "assess_risk",
                        "monitor_indicators", 
                        "create_safety_plan",
                        "escalate_emergency",
                        "provide_immediate_support",
                        "activate_cultural_protocols"
                    ],
                    "description": "Crisis detection action to perform"
                },
                "user_input": {
                    "type": "string",
                    "description": "User's recent input to analyze for crisis indicators"
                },
                "risk_factors": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Identified risk factors (hopelessness, isolation, suicidal ideation, etc.)"
                },
                "cultural_context": {
                    "type": "object",
                    "properties": {
                        "family_dynamics": {"type": "string"},
                        "religious_beliefs": {"type": "string"},
                        "social_support": {"type": "string"}
                    },
                    "description": "Cultural context for appropriate intervention"
                },
                "urgency_level": {
                    "type": "string",
                    "enum": ["low", "moderate", "high", "imminent"],
                    "description": "Assessed urgency level for intervention"
                }
            },
            required=["action"]
        )
    
    async def execute(self, action: str, **kwargs) -> str:
        """Execute crisis detection actions."""
        valid_actions = [
            "assess_risk", "monitor_indicators", "create_safety_plan",
            "escalate_emergency", "provide_immediate_support", "activate_cultural_protocols"
        ]
        
        if not self.validate_action(action, valid_actions):
            return f"Invalid crisis action. Use: {', '.join(valid_actions)}"
        
        user_input = kwargs.get("user_input", "")
        risk_factors = kwargs.get("risk_factors", [])
        cultural_context = kwargs.get("cultural_context", {})
        urgency_level = kwargs.get("urgency_level", "low")
        
        # Log the crisis detection action
        await self.log_clinical_action(f"crisis_detection_{action}", {
            "user_input_length": len(user_input),
            "risk_factors": risk_factors,
            "urgency_level": urgency_level,
            "cultural_context": cultural_context
        })
        
        if action == "assess_risk":
            return await self._assess_suicide_risk(user_input, risk_factors)
        elif action == "monitor_indicators":
            return await self._monitor_crisis_indicators(user_input)
        elif action == "create_safety_plan":
            return await self._create_safety_plan(cultural_context)
        elif action == "escalate_emergency":
            return await self._escalate_emergency(urgency_level, risk_factors)
        elif action == "provide_immediate_support":
            return await self._provide_immediate_support(user_input, cultural_context)
        elif action == "activate_cultural_protocols":
            return await self._activate_cultural_protocols(cultural_context)
    
    async def _assess_suicide_risk(self, user_input: str, risk_factors: List[str]) -> str:
        """Assess suicide risk level based on input and factors."""
        
        # Check for crisis indicators in the input
        crisis_detected = await self.check_crisis_indicators(user_input)
        
        # Analyze risk factors
        high_risk_factors = [
            "previous_attempts", "substance_abuse", "social_isolation", 
            "recent_loss", "access_to_means", "specific_plan"
        ]
        
        moderate_risk_factors = [
            "hopelessness", "depression", "anxiety", "family_conflict",
            "financial_stress", "health_problems"
        ]
        
        risk_score = 0
        for factor in risk_factors:
            if factor in high_risk_factors:
                risk_score += 3
            elif factor in moderate_risk_factors:
                risk_score += 1
        
        # Determine risk level
        if risk_score >= 6 or crisis_detected:
            self.current_risk_level = "imminent"
        elif risk_score >= 4:
            self.current_risk_level = "high"
        elif risk_score >= 2:
            self.current_risk_level = "moderate"
        else:
            self.current_risk_level = "low"
        
        # Store in clinical data
        self.clinical_data["risk_assessment"] = {
            "risk_level": self.current_risk_level,
            "risk_score": risk_score,
            "factors": risk_factors,
            "crisis_indicators_detected": crisis_detected
        }
        
        # Send risk assessment to client
        await self.send_client_command("risk_assessment", {
            "risk_level": self.current_risk_level,
            "risk_score": risk_score,
            "requires_immediate_action": self.current_risk_level in ["high", "imminent"]
        })
        
        # Auto-escalate if imminent risk
        if self.current_risk_level == "imminent":
            await self._escalate_emergency("imminent", risk_factors)
        
        return self.format_response_culturally(
            f"Risk assessment completed. Risk level: {self.current_risk_level}. "
            f"{'Immediate intervention protocols activated.' if self.current_risk_level in ['high', 'imminent'] else 'Monitoring and support initiated.'}"
        )
    
    async def _monitor_crisis_indicators(self, user_input: str) -> str:
        """Monitor ongoing conversation for crisis indicators."""
        
        # Arabic and English crisis keywords
        crisis_patterns = {
            "suicidal_ideation": [
                r"(?i)\b(suicide|kill\s+myself|end\s+it\s+all|no\s+point\s+living)\b",
                r"انتحار|اقتل\s+نفسي|انهي\s+حياتي|لا\s+يوجد\s+أمل"
            ],
            "self_harm": [
                r"(?i)\b(cut\s+myself|hurt\s+myself|self\s+harm|overdose)\b",
                r"اجرح\s+نفسي|اؤذي\s+نفسي|جرعة\s+زائدة"
            ],
            "hopelessness": [
                r"(?i)\b(hopeless|nothing\s+matters|give\s+up|no\s+future)\b",
                r"لا\s+أمل|لا\s+يهم\s+شيء|استسلم|لا\s+مستقبل"
            ],
            "isolation": [
                r"(?i)\b(nobody\s+cares|all\s+alone|no\s+friends|isolated)\b",
                r"لا\s+يهتم\s+أحد|وحيد|لا\s+أصدقاء|معزول"
            ]
        }
        
        detected_indicators = []
        for category, patterns in crisis_patterns.items():
            for pattern in patterns:
                if re.search(pattern, user_input):
                    detected_indicators.append(category)
                    break
        
        if detected_indicators:
            self.crisis_indicators.extend(detected_indicators)
            self.crisis_detected = True
            
            await self.send_client_command("crisis_indicators_detected", {
                "indicators": detected_indicators,
                "total_indicators": len(self.crisis_indicators),
                "alert_level": "high" if len(detected_indicators) > 1 else "moderate"
            })
            
            return self.format_response_culturally(
                f"Crisis indicators detected: {', '.join(detected_indicators)}. "
                "Activating enhanced monitoring and support protocols.",
                "supportive"
            )
        
        return "Monitoring continues. No immediate crisis indicators detected."
    
    async def _create_safety_plan(self, cultural_context: Dict[str, Any]) -> str:
        """Create a culturally appropriate safety plan."""
        
        safety_plan = {
            "warning_signs": [
                "Feeling overwhelmed",
                "Thoughts of hopelessness", 
                "Strong urges to harm oneself"
            ],
            "coping_strategies": [],
            "support_contacts": [],
            "professional_resources": [],
            "environmental_safety": []
        }
        
        # Add culturally appropriate coping strategies
        if cultural_context.get("religious_beliefs"):
            safety_plan["coping_strategies"].extend([
                "Prayer and dhikr (remembrance of Allah)",
                "Reading Quran for comfort",
                "Seeking guidance from religious counsel"
            ])
        
        safety_plan["coping_strategies"].extend([
            "Deep breathing exercises",
            "Call a trusted family member",
            "Go to a public place",
            "Listen to calming music"
        ])
        
        # Family and community support (culturally important)
        if cultural_context.get("family_dynamics") == "supportive":
            safety_plan["support_contacts"].extend([
                "Immediate family members",
                "Extended family elders",
                "Close family friends"
            ])
        
        # Professional resources in Gulf Arabic context
        safety_plan["professional_resources"].extend([
            "Mental health hotline: [Local emergency number]",
            "Nearest hospital emergency room",
            "Culturally sensitive therapist",
            "Community mental health center"
        ])
        
        # Environmental safety measures
        safety_plan["environmental_safety"].extend([
            "Remove access to harmful objects",
            "Stay with trusted family/friends",
            "Avoid isolation",
            "Create calming environment"
        ])
        
        self.safety_plan_created = True
        self.clinical_data["safety_plan"] = safety_plan
        
        # Send safety plan to client
        await self.send_client_command("safety_plan_created", {
            "safety_plan": safety_plan,
            "cultural_adaptations": cultural_context
        })
        
        return self.format_response_culturally(
            "Safety plan created with your cultural and family context in mind. "
            "This plan will help you stay safe during difficult moments. "
            "Keep important contact numbers easily accessible.",
            "encouraging"
        )
    
    async def _escalate_emergency(self, urgency_level: str, risk_factors: List[str]) -> str:
        """Escalate to emergency protocols."""
        
        emergency_data = {
            "urgency_level": urgency_level,
            "risk_factors": risk_factors,
            "immediate_actions_required": True,
            "professional_intervention_needed": True
        }
        
        # Trigger emergency protocol
        await self.trigger_emergency_protocol(
            f"Crisis escalation - {urgency_level} risk",
            emergency_data
        )
        
        # Cultural sensitivity in emergency messaging
        emergency_message = """
        🚨 EMERGENCY PROTOCOL ACTIVATED 🚨
        
        الله معك في هذه اللحظة الصعبة. أنت لست وحدك، حبيبي/حبيبتي.
        Allah is with you in this difficult moment. You are not alone, dear.
        
        اتصل فوراً بـ:
        Call immediately:
        
        📞 Emergency Services: 999 (الطوارئ العمانية)
        📞 Royal Oman Police: 9999 (شرطة عمان السلطانية)  
        📞 Mental Health Services: Ministry of Health Oman
        📞 Trusted family member or close friend (فرد من العائلة أو صديق مقرب)
        📞 Local mosque imam for spiritual support (إمام المسجد للدعم الروحي)
        
        طلب المساعدة ليس عيباً، بل علامة قوة وحكمة، كما علمنا ديننا الحنيف.
        Seeking help is not shameful, but a sign of strength and wisdom, as our religion teaches us.
        
        الرسول (صلى الله عليه وسلم) قال: "من فرج عن مؤمن كربة فرج الله عنه كربة من كرب يوم القيامة"
        The Prophet (peace be upon him) said: "Whoever relieves a believer's distress, Allah will relieve their distress."
        """
        
        await self.send_client_command("emergency_activated", {
            "urgency": urgency_level,
            "message": emergency_message,
            "immediate_actions": [
                "Call emergency services if in immediate danger",
                "Go to nearest emergency room",
                "Call trusted family member",
                "Do not be alone"
            ]
        })
        
        return emergency_message
    
    async def _provide_immediate_support(self, user_input: str, cultural_context: Dict[str, Any]) -> str:
        """Provide immediate crisis support."""
        
        # Assess emotional state from input
        emotional_indicators = self._assess_emotional_state(user_input)
        
        # Provide culturally appropriate immediate support
        support_message = self.format_response_culturally(
            "I can hear that you're going through a very difficult time right now. "
            "Your feelings are valid, and you deserve support and care.",
            "supportive"
        )
        
        # Add Islamic/cultural comfort if appropriate
        if cultural_context.get("religious_beliefs"):
            support_message += "\n\nاللهم اشفه شفاءً لا يغادر سقماً (May Allah grant you complete healing). "
            support_message += "Remember that seeking help is encouraged in Islam, and taking care of your mental health is part of taking care of the trust Allah has given you."
        
        # Immediate coping techniques
        support_message += "\n\nLet's try some immediate techniques to help you feel safer right now:"
        support_message += "\n1. Take deep, slow breaths with me"
        support_message += "\n2. Look around and name 5 things you can see"
        support_message += "\n3. Feel your feet on the ground"
        support_message += "\n4. Remember: This feeling will pass"
        
        await self.send_client_command("immediate_support", {
            "emotional_state": emotional_indicators,
            "support_message": support_message,
            "coping_techniques": ["breathing", "grounding", "mindfulness"]
        })
        
        return support_message
    
    async def _activate_cultural_protocols(self, cultural_context: Dict[str, Any]) -> str:
        """Activate cultural sensitivity protocols."""
        
        protocols_activated = []
        
        # Family involvement protocol
        if cultural_context.get("family_dynamics") == "supportive":
            self.cultural_adaptations["family_involvement"] = True
            protocols_activated.append("family_support_integration")
        
        # Religious considerations
        if cultural_context.get("religious_beliefs"):
            self.cultural_adaptations["religious_considerations"] = True
            protocols_activated.append("islamic_spiritual_support")
        
        # Community support
        if cultural_context.get("social_support") == "available":
            self.cultural_adaptations["community_support"] = True
            protocols_activated.append("community_resource_activation")
        
        await self.send_client_command("cultural_protocols_activated", {
            "protocols": protocols_activated,
            "cultural_adaptations": self.cultural_adaptations
        })
        
        return self.format_response_culturally(
            f"Cultural sensitivity protocols activated: {', '.join(protocols_activated)}. "
            "Support will be provided in a way that respects your cultural values and family context."
        )
    
    def _assess_emotional_state(self, user_input: str) -> Dict[str, Any]:
        """Assess emotional state from user input."""
        
        emotional_patterns = {
            "despair": [r"(?i)\b(hopeless|despair|worthless|pointless)\b", r"يأس|لا\s+قيمة|لا\s+فائدة"],
            "anger": [r"(?i)\b(angry|mad|furious|rage)\b", r"غاضب|متضايق|غضب"],
            "sadness": [r"(?i)\b(sad|depressed|down|empty)\b", r"حزين|مكتئب|فارغ"],
            "fear": [r"(?i)\b(scared|afraid|terrified|anxious)\b", r"خائف|قلق|مرعوب"],
            "numbness": [r"(?i)\b(numb|empty|nothing|void)\b", r"مخدر|فارغ|لا\s+شيء"]
        }
        
        detected_emotions = []
        for emotion, patterns in emotional_patterns.items():
            for pattern in patterns:
                if re.search(pattern, user_input):
                    detected_emotions.append(emotion)
                    break
        
        return {
            "detected_emotions": detected_emotions,
            "intensity": "high" if len(detected_emotions) > 2 else "moderate" if detected_emotions else "low",
            "requires_immediate_attention": "despair" in detected_emotions or "numbness" in detected_emotions
        } 