"""
Base tool class for OMANI Therapist Voice therapeutic tools.
Provides clinical safety, cultural sensitivity, and standardized interfaces.
"""

import json
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from loguru import logger
from pipecat.adapters.schemas.function_schema import FunctionSchema


class BaseTool(ABC):
    """
    Base class for all therapeutic tools in the OMANI Therapist Voice system.
    
    Provides:
    - Clinical safety protocols
    - Cultural sensitivity guidelines
    - Emergency escalation capabilities
    - Standardized tool interface
    """
    
    def __init__(self, rtvi_processor, task=None):
        """
        Initialize base therapeutic tool.
        
        Args:
            rtvi_processor: RTVI processor for client communication
            task: Pipeline task for system integration
        """
        self.rtvi_processor = rtvi_processor
        self.task = task
        self.tool_name = self.__class__.__name__.lower().replace('tool', '')
        self.clinical_data = {}
        
        # Clinical safety flags
        self.crisis_detected = False
        self.emergency_escalation_needed = False
        self.professional_referral_suggested = False
        
        logger.info(f"🏥 Initialized therapeutic tool: {self.tool_name}")
    
    @abstractmethod
    def get_tool_definition(self) -> FunctionSchema:
        """
        Define the tool schema for LLM function calling.
        Must be implemented by each therapeutic tool.
        """
        pass
    
    @abstractmethod
    async def execute(self, action: str, **kwargs) -> str:
        """
        Execute the therapeutic tool action.
        Must be implemented by each therapeutic tool.
        """
        pass
    
    def validate_action(self, action: str, valid_actions: list) -> bool:
        """
        Validate that the requested action is allowed for this tool.
        
        Args:
            action: The action to validate
            valid_actions: List of allowed actions
            
        Returns:
            bool: True if action is valid
        """
        if action not in valid_actions:
            logger.warning(f"🏥 Invalid action '{action}' for {self.tool_name}. Valid: {valid_actions}")
            return False
        return True
    
    async def send_client_command(self, command_type: str, data: Dict[Any, Any]):
        """
        Send command to client via WebSocket for UI updates with automatic cleanup.
        
        Args:
            command_type: Type of command to send
            data: Command data payload
        """
        try:
            from utils.tool_websocket_registry import broadcast_to_all_therapeutic_clients
            
            command = {
                "type": f"therapeutic_{command_type}",
                "tool": self.tool_name,
                "data": data,
                "timestamp": self._get_timestamp(),
                "clinical_context": self._get_clinical_context()
            }
            
            # Use the enhanced broadcast function with automatic cleanup
            sent_count = await broadcast_to_all_therapeutic_clients(command)
            
            if sent_count > 0:
                logger.debug(f"🏥 Therapeutic command '{command_type}' sent to {sent_count} clients")
            else:
                logger.warning(f"🏥 No clients available for therapeutic command '{command_type}'")
        
        except Exception as e:
            logger.error(f"🏥 Error sending therapeutic client command: {e}")
    
    def _get_timestamp(self) -> str:
        """Get current timestamp for clinical documentation."""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def _get_clinical_context(self) -> Dict[str, Any]:
        """Get current clinical context for documentation."""
        return {
            "crisis_detected": self.crisis_detected,
            "emergency_escalation": self.emergency_escalation_needed,
            "referral_suggested": self.professional_referral_suggested,
            "tool_active": self.tool_name
        }
    
    async def log_clinical_action(self, action: str, details: Dict[str, Any]):
        """
        Log clinical action for documentation and safety.
        
        Args:
            action: The clinical action taken
            details: Details of the action
        """
        clinical_log = {
            "timestamp": self._get_timestamp(),
            "tool": self.tool_name,
            "action": action,
            "details": details,
            "clinical_context": self._get_clinical_context(),
            "session_metadata": {
                "tool_version": "1.0.0",
                "cultural_adaptations": "omani_gulf_arabic",
                "therapeutic_approach": "culturally_integrated_therapy",
                "safety_protocols_active": True
            }
        }
        
        # Store in clinical data for session documentation
        if not hasattr(self, 'session_clinical_log'):
            self.session_clinical_log = []
        self.session_clinical_log.append(clinical_log)
        
        logger.info(f"🏥 Clinical action logged: {action} by {self.tool_name}")
        
        # Send clinical log to client for documentation
        await self.send_client_command("clinical_log", clinical_log)
        
        # If this is a crisis-related action, also log to crisis documentation
        if any(keyword in action.lower() for keyword in ['crisis', 'emergency', 'risk', 'escalation']):
            await self._log_crisis_documentation(clinical_log)
    
    async def _log_crisis_documentation(self, clinical_log: Dict[str, Any]):
        """Log crisis-related actions with enhanced documentation."""
        crisis_log = {
            **clinical_log,
            "crisis_documentation": {
                "protocol_activated": True,
                "cultural_considerations": "gulf_arabic_islamic_context",
                "family_notification_status": "pending_assessment",
                "emergency_resources_provided": True,
                "follow_up_required": True
            }
        }
        
        logger.critical(f"🚨 CRISIS DOCUMENTATION: {clinical_log['action']}")
        await self.send_client_command("crisis_documentation", crisis_log)
    
    def get_session_documentation(self) -> Dict[str, Any]:
        """Get comprehensive session documentation for clinical records."""
        return {
            "session_summary": {
                "tool_name": self.tool_name,
                "total_actions": len(getattr(self, 'session_clinical_log', [])),
                "crisis_flags": {
                    "crisis_detected": self.crisis_detected,
                    "emergency_escalation": self.emergency_escalation_needed,
                    "referral_suggested": self.professional_referral_suggested
                },
                "cultural_adaptations": "omani_gulf_arabic_islamic"
            },
            "clinical_actions": getattr(self, 'session_clinical_log', []),
            "safety_assessment": self._get_clinical_context(),
            "recommendations": self._generate_session_recommendations()
        }
    
    def _generate_session_recommendations(self) -> List[str]:
        """Generate clinical recommendations based on session data."""
        recommendations = []
        
        if self.crisis_detected:
            recommendations.append("Continue crisis monitoring and safety assessment")
            recommendations.append("Ensure 24-hour safety plan is in place")
            recommendations.append("Consider family involvement per cultural preferences")
        
        if self.emergency_escalation_needed:
            recommendations.append("Immediate professional intervention required")
            recommendations.append("Coordinate with local mental health services")
            recommendations.append("Provide emergency contact information")
        
        if self.professional_referral_suggested:
            recommendations.append("Schedule follow-up with licensed mental health professional")
            recommendations.append("Provide culturally appropriate referral options")
            recommendations.append("Ensure continuity of care documentation")
        
        # Always include cultural considerations
        recommendations.append("Maintain cultural sensitivity in all interventions")
        recommendations.append("Respect Islamic values and Gulf Arab customs")
        recommendations.append("Consider family dynamics in treatment planning")
        
        return recommendations
    
    def assess_cultural_sensitivity(self, content: str) -> Dict[str, Any]:
        """
        Assess content for cultural sensitivity (Gulf Arabic/Islamic context).
        
        Args:
            content: Content to assess
            
        Returns:
            Assessment results
        """
        # Handle None or empty content
        if not content:
            return {
                "religious_appropriate": True,
                "culturally_sensitive": True,
                "language_appropriate": True,
                "recommendations": []
            }
        
        # Basic cultural sensitivity assessment
        sensitive_indicators = {
            "religious_appropriate": True,
            "culturally_sensitive": True,
            "language_appropriate": True,
            "recommendations": []
        }
        
        # Check for potential cultural sensitivity issues
        content_lower = content.lower()
        
        # Religious sensitivity
        if any(word in content_lower for word in ["haram", "forbidden", "sin"]):
            sensitive_indicators["recommendations"].append("Consider religious context sensitivity")
        
        # Cultural terminology
        if any(word in content_lower for word in ["family", "marriage", "honor"]):
            sensitive_indicators["recommendations"].append("Apply Gulf cultural context")
        
        return sensitive_indicators
    
    async def check_crisis_indicators(self, user_input: str) -> bool:
        """
        Check for crisis indicators in user input.
        
        Args:
            user_input: User's input to analyze
            
        Returns:
            bool: True if crisis indicators detected
        """
        # Handle None or empty user_input
        if not user_input:
            return False
        
        crisis_keywords = [
            # English direct indicators
            "suicide", "kill myself", "end it all", "no point living", "hurt myself",
            "overdose", "jump", "cut myself", "die", "death", "can't go on",
            "better off dead", "want to disappear", "end my life", "not worth living",
            
            # Arabic direct indicators (العربية المباشرة)
            "انتحار", "اقتل نفسي", "لا يوجد امل", "اؤذي نفسي", "اموت", 
            "جرعة زائدة", "اقفز", "اجرح نفسي", "لا استطيع المتابعة", "اريد ان اختفي",
            "انهي حياتي", "لا استحق الحياة", "تعبت من الحياة", "ما فيه فايدة",
            
            # Gulf Arabic expressions of extreme distress
            "خلاص تعبت", "ما عاد فيني", "انطفيت", "مليت من الحياة", 
            "ودي اروح", "تعبت من كل شي", "ما اقدر اكمل", "خلاص كفيت",
            "حياتي ما لها معنى", "مو قادر", "تعبان نفسياً مره",
            
            # Cultural expressions of hopelessness
            "الله يا خذني", "ريحني يا رب", "تعبت يا رب", "ما عاد لي صبر",
            "يا ليتني ما انولدت", "ودي الموت", "الموت ارحم",
            
            # Omani/Gulf cultural distress expressions
            "ما عاد عندي امل", "خلاص انكسرت", "روحي تعبانة", "قلبي مات",
            "ما اقدر احتمل", "مو قادر على شي", "نفسيتي خربت خلاص"
        ]
        
        user_lower = user_input.lower()
        for keyword in crisis_keywords:
            if keyword in user_lower:
                self.crisis_detected = True
                await self.log_clinical_action("crisis_indicator_detected", {
                    "keyword": keyword,
                    "user_input_length": len(user_input),
                    "immediate_action": "crisis_protocol_activated",
                    "cultural_context": "gulf_arabic_expression" if any(arabic_char in keyword for arabic_char in "ابتثجحخدذرزسشصضطظعغفقكلمنهوي") else "english_expression"
                })
                return True
        
        return False
    
    async def trigger_emergency_protocol(self, reason: str, details: Dict[str, Any]):
        """
        Trigger emergency escalation protocol.
        
        Args:
            reason: Reason for emergency escalation
            details: Additional details
        """
        self.emergency_escalation_needed = True
        
        emergency_data = {
            "reason": reason,
            "details": details,
            "timestamp": self._get_timestamp(),
            "tool": self.tool_name,
            "severity": "high"
        }
        
        await self.log_clinical_action("emergency_protocol_activated", emergency_data)
        await self.send_client_command("emergency_escalation", emergency_data)
        
        logger.critical(f"🚨 EMERGENCY PROTOCOL ACTIVATED: {reason}")
    
    def suggest_professional_referral(self, reason: str) -> str:
        """
        Suggest professional referral with culturally appropriate messaging.
        
        Args:
            reason: Reason for referral
            
        Returns:
            Referral message
        """
        self.professional_referral_suggested = True
        
        # Culturally sensitive referral message in Arabic and English
        referral_message = f"""
        أعتقد أنه من المفيد لك التحدث مع معالج نفسي مختص. هذا أمر طبيعي وإيجابي.
        
        I believe it would be beneficial for you to speak with a licensed mental health professional. This is a normal and positive step.
        
        السبب: {reason}
        Reason: {reason}
        
        يمكنني مساعدتك في العثور على معالج يفهم ثقافتنا العربية.
        I can help you find a therapist who understands our Arab culture.
        """
        
        return referral_message
    
    def format_response_culturally(self, response: str, emotional_tone: str = "supportive") -> str:
        """
        Format response with cultural sensitivity for Gulf Arabic context.
        
        Args:
            response: Base response
            emotional_tone: Desired emotional tone
            
        Returns:
            Culturally formatted response
        """
        # Add appropriate Arabic greetings and cultural expressions
        if emotional_tone == "supportive":
            prefix = "الله يعطيك القوة، "  # "May Allah give you strength"
        elif emotional_tone == "encouraging":
            prefix = "إن شاء الله كل شيء سيكون بخير، "  # "God willing, everything will be fine"
        else:
            prefix = "أفهم مشاعرك، "  # "I understand your feelings"
        
        return f"{prefix}{response}" 