"""
Emotional Analysis Tool for OMANI Therapist Voice.
Analyzes emotional states with cultural sensitivity for Gulf Arabic context.
"""

import re
from typing import Dict, Any, List, Tuple
from loguru import logger
from pipecat.adapters.schemas.function_schema import FunctionSchema
from .base_tool import BaseTool


class EmotionalAnalysisTool(BaseTool):
    """
    Emotional analysis tool for therapeutic sessions.
    
    Features:
    - Real-time emotion detection from speech and text
    - Cultural context awareness for Gulf Arabic expressions
    - Emotional pattern tracking over time
    - Therapeutic intervention recommendations
    - Cultural sensitivity for Islamic emotional expressions
    """
    
    def __init__(self, rtvi_processor, task=None):
        """Initialize emotional analysis tool."""
        super().__init__(rtvi_processor, task)
        
        # Emotion tracking
        self.emotion_history = []
        self.current_emotional_state = {}
        self.emotional_patterns = {}
        self.cultural_emotional_markers = {}
        
        # Arabic emotional expressions
        self.arabic_emotions = {
            "sadness": ["حزين", "مكتئب", "زعلان", "مهموم", "مغموم"],
            "anxiety": ["قلقان", "متوتر", "خايف", "مرتبك", "مضطرب"],
            "anger": ["غاضب", "زعلان", "متضايق", "غضبان", "مستاء"],
            "happiness": ["فرحان", "مبسوط", "سعيد", "مسرور", "راضي"],
            "fear": ["خايف", "مرعوب", "متخوف", "قلقان", "مهووس"],
            "shame": ["خجلان", "محرج", "مكسوف", "نادم", "أسف"],
            "guilt": ["مذنب", "نادم", "أسف", "محرج", "مكسوف"],
            "hope": ["متفائل", "راجي", "متوقع خير", "متطلع", "آمل"]
        }
        
        # Cultural emotional contexts
        self.cultural_contexts = {
            "family_honor": ["عيب", "حرام", "سمعة", "شرف", "كرامة"],
            "religious_guilt": ["ذنب", "حرام", "معصية", "تقصير", "استغفار"],
            "social_pressure": ["ناس", "مجتمع", "أهل", "عائلة", "أقارب"],
            "spiritual_comfort": ["الله", "دعاء", "صبر", "تسليم", "قدر"]
        }
        
        logger.info("💭 Emotional Analysis Tool initialized")
    
    def get_tool_definition(self) -> FunctionSchema:
        """Define the emotional analysis tool for LLM function calling."""
        return FunctionSchema(
            name="analyze_emotion",
            description="Analyze emotional states from speech and text with cultural sensitivity for Gulf Arabic context",
            properties={
                "analysis_type": {
                    "type": "string",
                    "enum": [
                        "detect_emotions",
                        "track_patterns",
                        "cultural_context_analysis",
                        "emotional_intensity_assessment",
                        "therapeutic_recommendations",
                        "crisis_emotional_indicators"
                    ],
                    "description": "Type of emotional analysis to perform"
                },
                "user_input": {
                    "type": "string",
                    "description": "User's speech or text input to analyze"
                },
                "voice_features": {
                    "type": "object",
                    "properties": {
                        "tone": {"type": "string"},
                        "pace": {"type": "string"},
                        "volume": {"type": "string"},
                        "pitch_variation": {"type": "string"}
                    },
                    "description": "Voice characteristics for audio emotion analysis"
                },
                "cultural_context": {
                    "type": "object",
                    "properties": {
                        "arabic_language_used": {"type": "boolean"},
                        "religious_expressions": {"type": "boolean"},
                        "family_context_mentioned": {"type": "boolean"},
                        "cultural_values_referenced": {"type": "boolean"}
                    },
                    "description": "Cultural context for emotion interpretation"
                },
                "session_context": {
                    "type": "object",
                    "properties": {
                        "session_duration": {"type": "integer"},
                        "previous_emotions": {"type": "array", "items": {"type": "string"}},
                        "therapeutic_goal": {"type": "string"}
                    },
                    "description": "Session context for pattern analysis"
                }
            },
            required=["analysis_type", "user_input"]
        )
    
    async def execute(self, analysis_type: str, **kwargs) -> str:
        """Execute emotional analysis."""
        valid_types = [
            "detect_emotions", "track_patterns", "cultural_context_analysis",
            "emotional_intensity_assessment", "therapeutic_recommendations",
            "crisis_emotional_indicators"
        ]
        
        if not self.validate_action(analysis_type, valid_types):
            return f"Invalid analysis type. Use: {', '.join(valid_types)}"
        
        user_input = kwargs.get("user_input", "")
        voice_features = kwargs.get("voice_features", {})
        cultural_context = kwargs.get("cultural_context", {})
        session_context = kwargs.get("session_context", {})
        
        # Log emotional analysis
        await self.log_clinical_action(f"emotional_analysis_{analysis_type}", {
            "user_input_length": len(user_input),
            "voice_features": voice_features,
            "cultural_context": cultural_context,
            "session_context": session_context
        })
        
        if analysis_type == "detect_emotions":
            return await self._detect_emotions(user_input, voice_features, cultural_context)
        elif analysis_type == "track_patterns":
            return await self._track_emotional_patterns(session_context)
        elif analysis_type == "cultural_context_analysis":
            return await self._analyze_cultural_context(user_input, cultural_context)
        elif analysis_type == "emotional_intensity_assessment":
            return await self._assess_emotional_intensity(user_input, voice_features)
        elif analysis_type == "therapeutic_recommendations":
            return await self._generate_therapeutic_recommendations()
        elif analysis_type == "crisis_emotional_indicators":
            return await self._analyze_crisis_emotional_indicators(user_input)
    
    async def _detect_emotions(self, user_input: str, voice_features: Dict[str, Any], cultural_context: Dict[str, Any]) -> str:
        """Detect emotions from text and voice with cultural sensitivity."""
        
        detected_emotions = {
            "primary_emotions": [],
            "secondary_emotions": [],
            "emotional_intensity": 0,
            "cultural_markers": [],
            "voice_indicators": {},
            "confidence_score": 0
        }
        
        # Text-based emotion detection
        text_emotions = self._analyze_text_emotions(user_input, cultural_context)
        detected_emotions["primary_emotions"] = text_emotions["primary"]
        detected_emotions["secondary_emotions"] = text_emotions["secondary"]
        detected_emotions["cultural_markers"] = text_emotions["cultural_markers"]
        
        # Voice-based emotion detection
        if voice_features:
            voice_emotions = self._analyze_voice_emotions(voice_features)
            detected_emotions["voice_indicators"] = voice_emotions
        
        # Calculate overall emotional intensity
        detected_emotions["emotional_intensity"] = self._calculate_emotional_intensity(
            text_emotions, voice_emotions if voice_features else {}
        )
        
        # Store in emotion history
        emotion_entry = {
            "timestamp": self._get_timestamp(),
            "emotions": detected_emotions,
            "user_input": user_input[:100],  # Store first 100 chars for context
            "cultural_context": cultural_context
        }
        self.emotion_history.append(emotion_entry)
        self.current_emotional_state = detected_emotions
        
        # Generate culturally sensitive response
        response = await self._generate_emotion_response(detected_emotions, cultural_context)
        
        # Send analysis to client
        await self.send_client_command("emotion_analysis", {
            "detected_emotions": detected_emotions,
            "cultural_interpretation": self._get_cultural_interpretation(detected_emotions, cultural_context),
            "therapeutic_implications": self._get_therapeutic_implications(detected_emotions)
        })
        
        return response
    
    def _analyze_text_emotions(self, text: str, cultural_context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze emotions from text with cultural awareness."""
        
        # Handle None or empty text
        if not text:
            return {
                "primary": [],
                "secondary": [],
                "cultural_markers": []
            }
        
        text_lower = text.lower()
        detected_emotions = {
            "primary": [],
            "secondary": [],
            "cultural_markers": []
        }
        
        # Check for Arabic emotional expressions
        for emotion, expressions in self.arabic_emotions.items():
            for expression in expressions:
                if expression in text_lower or expression in text:
                    detected_emotions["primary"].append(emotion)
                    break
        
        # Check for cultural emotional contexts
        for context, markers in self.cultural_contexts.items():
            for marker in markers:
                if marker in text_lower or marker in text:
                    detected_emotions["cultural_markers"].append(context)
                    break
        
        # English emotion detection
        english_patterns = {
            "sadness": r"(?i)\b(sad|depressed|down|blue|melancholy|heartbroken)\b",
            "anxiety": r"(?i)\b(anxious|worried|nervous|stressed|tense|panic)\b",
            "anger": r"(?i)\b(angry|mad|furious|irritated|annoyed|rage)\b",
            "happiness": r"(?i)\b(happy|joyful|excited|elated|cheerful|content)\b",
            "fear": r"(?i)\b(scared|afraid|terrified|frightened|fearful)\b",
            "shame": r"(?i)\b(ashamed|embarrassed|humiliated|disgrace)\b",
            "guilt": r"(?i)\b(guilty|remorse|regret|sorry|fault)\b",
            "hope": r"(?i)\b(hopeful|optimistic|confident|positive|encouraged)\b"
        }
        
        for emotion, pattern in english_patterns.items():
            if re.search(pattern, text):
                if emotion not in detected_emotions["primary"]:
                    detected_emotions["primary"].append(emotion)
        
        # Remove duplicates and limit to top emotions
        detected_emotions["primary"] = list(set(detected_emotions["primary"]))[:3]
        
        return detected_emotions
    
    def _analyze_voice_emotions(self, voice_features: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze emotions from voice characteristics."""
        
        voice_emotions = {
            "tone_emotion": "neutral",
            "intensity_from_voice": 0,
            "stress_indicators": [],
            "cultural_voice_patterns": []
        }
        
        tone = voice_features.get("tone", "").lower()
        pace = voice_features.get("pace", "").lower()
        volume = voice_features.get("volume", "").lower()
        pitch_variation = voice_features.get("pitch_variation", "").lower()
        
        # Tone analysis
        if tone in ["low", "flat", "monotone"]:
            voice_emotions["tone_emotion"] = "sadness"
            voice_emotions["intensity_from_voice"] += 2
        elif tone in ["high", "tense", "strained"]:
            voice_emotions["tone_emotion"] = "anxiety"
            voice_emotions["intensity_from_voice"] += 3
        elif tone in ["harsh", "sharp", "aggressive"]:
            voice_emotions["tone_emotion"] = "anger"
            voice_emotions["intensity_from_voice"] += 3
        
        # Pace analysis
        if pace in ["fast", "rapid", "rushed"]:
            voice_emotions["stress_indicators"].append("rapid_speech")
            voice_emotions["intensity_from_voice"] += 1
        elif pace in ["slow", "hesitant", "labored"]:
            voice_emotions["stress_indicators"].append("slow_speech")
            voice_emotions["intensity_from_voice"] += 1
        
        # Volume analysis
        if volume in ["quiet", "whisper", "low"]:
            voice_emotions["stress_indicators"].append("withdrawn_expression")
        elif volume in ["loud", "shouting", "raised"]:
            voice_emotions["stress_indicators"].append("agitated_expression")
        
        # Cultural voice patterns (specific to Gulf Arabic)
        if voice_features.get("cultural_expressions"):
            voice_emotions["cultural_voice_patterns"] = ["traditional_expression_style"]
        
        return voice_emotions
    
    def _calculate_emotional_intensity(self, text_emotions: Dict, voice_emotions: Dict) -> int:
        """Calculate overall emotional intensity (1-10 scale)."""
        
        intensity = 0
        
        # Base intensity from number of emotions detected
        intensity += len(text_emotions.get("primary", [])) * 2
        intensity += len(text_emotions.get("cultural_markers", []))
        
        # Voice-based intensity
        intensity += voice_emotions.get("intensity_from_voice", 0)
        intensity += len(voice_emotions.get("stress_indicators", []))
        
        # Cap at 10
        return min(intensity, 10)
    
    async def _track_emotional_patterns(self, session_context: Dict[str, Any]) -> str:
        """Track emotional patterns over time."""
        
        if len(self.emotion_history) < 2:
            return self.format_response_culturally(
                "I'm beginning to understand your emotional patterns. "
                "Let's continue our conversation to gain more insights."
            )
        
        # Analyze recent emotion history
        recent_emotions = self.emotion_history[-5:]  # Last 5 emotional states
        
        patterns = {
            "dominant_emotions": self._find_dominant_emotions(recent_emotions),
            "emotional_progression": self._analyze_emotional_progression(recent_emotions),
            "cultural_themes": self._identify_cultural_themes(recent_emotions),
            "intensity_trend": self._analyze_intensity_trend(recent_emotions)
        }
        
        self.emotional_patterns = patterns
        
        response = self.format_response_culturally(
            "I'm noticing some patterns in your emotional experience. "
            "Understanding these patterns can help us work together more effectively."
        )
        
        # Describe dominant emotions
        if patterns["dominant_emotions"]:
            dominant = patterns["dominant_emotions"][0]
            response += f"\n\nThe main emotion I'm sensing is {dominant}. "
            
            if dominant in ["sadness", "anxiety", "fear"]:
                response += "These feelings are completely valid and understandable."
            elif dominant in ["anger"]:
                response += "It's natural to feel this way, and we can work with these feelings constructively."
        
        # Describe progression
        if patterns["emotional_progression"] == "improving":
            response += "\n\nI notice your emotional state seems to be gradually improving as we talk."
        elif patterns["emotional_progression"] == "declining":
            response += "\n\nI'm noticing you might be feeling more distressed. Let's focus on some support techniques."
        
        # Cultural themes
        if patterns["cultural_themes"]:
            response += f"\n\nI also notice themes related to {', '.join(patterns['cultural_themes'])} in your expressions."
        
        await self.send_client_command("emotional_patterns", {
            "patterns": patterns,
            "recommendations": self._get_pattern_recommendations(patterns)
        })
        
        return response
    
    async def _analyze_cultural_context(self, user_input: str, cultural_context: Dict[str, Any]) -> str:
        """Analyze cultural context of emotional expressions."""
        
        cultural_analysis = {
            "cultural_emotional_style": "neutral",
            "religious_expressions": [],
            "family_dynamics_indicated": False,
            "social_expectations_pressure": False,
            "traditional_coping_mentioned": False
        }
        
        # Handle None or empty user_input
        if not user_input:
            return self.format_response_culturally(
                "I'm here to support you. Please share your thoughts and feelings when you're ready."
            )
        
        text_lower = user_input.lower()
        
        # Detect religious expressions
        religious_expressions = ["الله", "إن شاء الله", "الحمد لله", "استغفر الله", "صبر", "قدر"]
        for expr in religious_expressions:
            if expr in user_input:
                cultural_analysis["religious_expressions"].append(expr)
        
        # Family dynamics
        family_words = ["أهل", "عائلة", "والدي", "والدتي", "أخوي", "أختي", "زوج", "أطفال"]
        if any(word in user_input for word in family_words):
            cultural_analysis["family_dynamics_indicated"] = True
        
        # Social pressure indicators
        social_pressure_words = ["ناس", "مجتمع", "عيب", "حرام", "سمعة", "كلام الناس"]
        if any(word in user_input for word in social_pressure_words):
            cultural_analysis["social_expectations_pressure"] = True
        
        # Traditional coping
        traditional_coping = ["صبر", "دعاء", "صلاة", "قراءة القرآن", "ذكر"]
        if any(word in user_input for word in traditional_coping):
            cultural_analysis["traditional_coping_mentioned"] = True
        
        response = self.format_response_culturally(
            "I appreciate you sharing your feelings in a way that reflects your cultural background. "
            "Your cultural values and beliefs are important in how we approach healing."
        )
        
        if cultural_analysis["religious_expressions"]:
            response += "\n\nI notice you draw on your faith for strength. This is a beautiful source of resilience."
        
        if cultural_analysis["family_dynamics_indicated"]:
            response += "\n\nFamily connections seem important to your experience. In our culture, family support is indeed very valuable."
        
        if cultural_analysis["social_expectations_pressure"]:
            response += "\n\nI understand there may be social expectations affecting how you feel. Let's explore how to balance these with your personal wellbeing."
        
        await self.send_client_command("cultural_analysis", {
            "analysis": cultural_analysis,
            "cultural_strengths": self._identify_cultural_strengths(cultural_analysis),
            "cultural_adaptations_needed": self._suggest_cultural_adaptations(cultural_analysis)
        })
        
        return response
    
    async def _assess_emotional_intensity(self, user_input: str, voice_features: Dict[str, Any]) -> str:
        """Assess the intensity of emotional distress."""
        
        intensity_indicators = {
            "text_intensity": 0,
            "voice_intensity": 0,
            "overall_intensity": 0,
            "crisis_level": "low",
            "intervention_needed": False
        }
        
        # Handle None or empty user_input
        if not user_input:
            return self.format_response_culturally(
                "I'm listening and ready to support you. Please share what's on your mind."
            )
        
        # Text-based intensity indicators
        high_intensity_words = [
            "unbearable", "can't take it", "overwhelming", "desperate", "hopeless",
            "لا أستطيع", "محتمل", "مدمر", "يائس", "محطم"
        ]
        
        moderate_intensity_words = [
            "difficult", "hard", "struggling", "stressed", "worried",
            "صعب", "متعب", "قلقان", "مرهق", "متوتر"
        ]
        
        for word in high_intensity_words:
            if word.lower() in user_input.lower():
                intensity_indicators["text_intensity"] += 3
        
        for word in moderate_intensity_words:
            if word.lower() in user_input.lower():
                intensity_indicators["text_intensity"] += 1
        
        # Voice-based intensity
        if voice_features:
            voice_intensity = voice_features.get("intensity_from_voice", 0)
            intensity_indicators["voice_intensity"] = voice_intensity
        
        # Calculate overall intensity
        total_intensity = intensity_indicators["text_intensity"] + intensity_indicators["voice_intensity"]
        intensity_indicators["overall_intensity"] = min(total_intensity, 10)
        
        # Determine crisis level
        if total_intensity >= 8:
            intensity_indicators["crisis_level"] = "high"
            intensity_indicators["intervention_needed"] = True
        elif total_intensity >= 5:
            intensity_indicators["crisis_level"] = "moderate"
        else:
            intensity_indicators["crisis_level"] = "low"
        
        # Generate response based on intensity
        if intensity_indicators["crisis_level"] == "high":
            response = self.format_response_culturally(
                "I can hear that you're experiencing very intense feelings right now. "
                "Let's focus on immediate support and safety.",
                "supportive"
            )
            
            # Trigger crisis protocols if needed
            if intensity_indicators["intervention_needed"]:
                await self.trigger_emergency_protocol(
                    "High emotional intensity detected",
                    {"intensity_level": total_intensity, "user_input": user_input[:50]}
                )
        
        elif intensity_indicators["crisis_level"] == "moderate":
            response = self.format_response_culturally(
                "You're going through a challenging time with significant emotional intensity. "
                "Let's work together to find ways to manage these feelings.",
                "supportive"
            )
        
        else:
            response = self.format_response_culturally(
                "I'm hearing manageable levels of distress. "
                "This is a good space for us to work on understanding and growth."
            )
        
        await self.send_client_command("intensity_assessment", {
            "intensity_indicators": intensity_indicators,
            "support_level_needed": intensity_indicators["crisis_level"],
            "immediate_interventions": self._get_intensity_interventions(intensity_indicators["crisis_level"])
        })
        
        return response
    
    async def _generate_therapeutic_recommendations(self) -> str:
        """Generate therapeutic recommendations based on emotional analysis."""
        
        if not self.current_emotional_state:
            return "Let's continue our conversation so I can better understand your emotional needs."
        
        recommendations = {
            "immediate_techniques": [],
            "session_focus": "",
            "cultural_adaptations": [],
            "follow_up_priorities": []
        }
        
        primary_emotions = self.current_emotional_state.get("primary_emotions", [])
        intensity = self.current_emotional_state.get("emotional_intensity", 0)
        
        # Recommendations based on primary emotions
        if "sadness" in primary_emotions:
            recommendations["immediate_techniques"].extend([
                "Gentle self-compassion exercises",
                "Behavioral activation planning",
                "Gratitude practice adaptation"
            ])
            recommendations["session_focus"] = "mood_support_and_activation"
        
        if "anxiety" in primary_emotions:
            recommendations["immediate_techniques"].extend([
                "Grounding techniques",
                "Breathing exercises with dhikr",
                "Worry time scheduling"
            ])
            recommendations["session_focus"] = "anxiety_management"
        
        if "anger" in primary_emotions:
            recommendations["immediate_techniques"].extend([
                "Anger validation and exploration",
                "Islamic anger management techniques",
                "Assertiveness in cultural context"
            ])
            recommendations["session_focus"] = "anger_processing"
        
        # Cultural adaptations
        cultural_markers = self.current_emotional_state.get("cultural_markers", [])
        if "religious_guilt" in cultural_markers:
            recommendations["cultural_adaptations"].append("Islamic guilt processing")
        if "family_honor" in cultural_markers:
            recommendations["cultural_adaptations"].append("Family dynamics exploration")
        if "social_pressure" in cultural_markers:
            recommendations["cultural_adaptations"].append("Social expectations balance")
        
        # Intensity-based recommendations
        if intensity >= 7:
            recommendations["follow_up_priorities"].extend([
                "Crisis safety planning",
                "Professional referral consideration",
                "Family support activation"
            ])
        elif intensity >= 4:
            recommendations["follow_up_priorities"].extend([
                "Regular check-ins",
                "Coping skills practice",
                "Progress monitoring"
            ])
        
        response = self.format_response_culturally(
            "Based on what I'm understanding about your emotional experience, "
            "here are some approaches that might be helpful for you."
        )
        
        response += f"\n\nImmediate techniques to try:"
        for technique in recommendations["immediate_techniques"][:3]:
            response += f"\n• {technique}"
        
        if recommendations["cultural_adaptations"]:
            response += f"\n\nCultural considerations:"
            for adaptation in recommendations["cultural_adaptations"]:
                response += f"\n• {adaptation}"
        
        await self.send_client_command("therapeutic_recommendations", {
            "recommendations": recommendations,
            "emotional_basis": self.current_emotional_state
        })
        
        return response
    
    async def _analyze_crisis_emotional_indicators(self, user_input: str) -> str:
        """Analyze for crisis-level emotional indicators."""
        
        # Handle None or empty user_input
        if not user_input:
            return self.format_response_culturally(
                "I'm here to support you. Please share your thoughts and feelings when you're ready."
            )
        
        crisis_emotional_patterns = {
            "hopelessness": [
                r"(?i)\b(no\s+hope|hopeless|pointless|no\s+future|give\s+up)\b",
                r"لا\s+أمل|يائس|لا\s+فائدة|لا\s+مستقبل|استسلم"
            ],
            "worthlessness": [
                r"(?i)\b(worthless|useless|burden|no\s+value|waste)\b",
                r"لا\s+قيمة|عديم\s+الفائدة|عبء|لا\s+أستحق"
            ],
            "overwhelming_pain": [
                r"(?i)\b(unbearable|can't\s+take|too\s+much|overwhelming)\b",
                r"لا\s+أحتمل|أكثر\s+من\s+طاقتي|لا\s+أستطيع|مدمر"
            ],
            "isolation": [
                r"(?i)\b(all\s+alone|nobody\s+cares|no\s+one|isolated)\b",
                r"وحيد|لا\s+يهتم\s+أحد|لا\s+أحد|معزول"
            ]
        }
        
        detected_indicators = []
        for indicator, patterns in crisis_emotional_patterns.items():
            for pattern in patterns:
                if re.search(pattern, user_input):
                    detected_indicators.append(indicator)
                    break
        
        crisis_score = len(detected_indicators)
        
        if crisis_score >= 3:
            crisis_level = "severe"
            await self.trigger_emergency_protocol(
                "Multiple crisis emotional indicators detected",
                {"indicators": detected_indicators, "user_input": user_input[:100]}
            )
        elif crisis_score >= 2:
            crisis_level = "moderate"
        else:
            crisis_level = "low"
        
        # Store crisis analysis
        self.clinical_data["crisis_emotional_analysis"] = {
            "indicators": detected_indicators,
            "crisis_score": crisis_score,
            "crisis_level": crisis_level,
            "timestamp": self._get_timestamp()
        }
        
        response = await self._generate_crisis_response(crisis_level, detected_indicators)
        
        await self.send_client_command("crisis_emotional_analysis", {
            "crisis_level": crisis_level,
            "indicators": detected_indicators,
            "immediate_actions": self._get_crisis_actions(crisis_level)
        })
        
        return response
    
    async def _generate_crisis_response(self, crisis_level: str, indicators: List[str]) -> str:
        """Generate appropriate response for crisis emotional indicators."""
        
        if crisis_level == "severe":
            return self.format_response_culturally(
                "I can hear the deep pain you're experiencing right now. "
                "You are not alone, and your life has value and meaning. "
                "Let's focus on your immediate safety and getting you the support you need.",
                "supportive"
            ) + "\n\n🚨 If you're having thoughts of hurting yourself, please reach out for immediate help."
        
        elif crisis_level == "moderate":
            return self.format_response_culturally(
                "I hear that you're going through a very difficult time. "
                "These intense feelings can be overwhelming, but they will not last forever. "
                "Let's work together to find some relief and support.",
                "supportive"
            )
        
        else:
            return self.format_response_culturally(
                "I'm here to listen and support you through whatever you're experiencing. "
                "Your feelings are valid and important."
            )
    
    def _find_dominant_emotions(self, emotion_history: List[Dict]) -> List[str]:
        """Find the most frequent emotions in recent history."""
        emotion_counts = {}
        
        for entry in emotion_history:
            emotions = entry["emotions"]["primary_emotions"]
            for emotion in emotions:
                emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        # Return emotions sorted by frequency
        return sorted(emotion_counts.keys(), key=lambda x: emotion_counts[x], reverse=True)
    
    def _analyze_emotional_progression(self, emotion_history: List[Dict]) -> str:
        """Analyze how emotions are progressing over time."""
        if len(emotion_history) < 2:
            return "stable"
        
        intensities = [entry["emotions"]["emotional_intensity"] for entry in emotion_history]
        
        if intensities[-1] > intensities[0]:
            return "intensifying"
        elif intensities[-1] < intensities[0]:
            return "improving"
        else:
            return "stable"
    
    def _identify_cultural_themes(self, emotion_history: List[Dict]) -> List[str]:
        """Identify recurring cultural themes in emotional expressions."""
        theme_counts = {}
        
        for entry in emotion_history:
            markers = entry["emotions"]["cultural_markers"]
            for marker in markers:
                theme_counts[marker] = theme_counts.get(marker, 0) + 1
        
        # Return themes that appear more than once
        return [theme for theme, count in theme_counts.items() if count > 1]
    
    def _analyze_intensity_trend(self, emotion_history: List[Dict]) -> str:
        """Analyze the trend in emotional intensity."""
        if len(emotion_history) < 3:
            return "insufficient_data"
        
        intensities = [entry["emotions"]["emotional_intensity"] for entry in emotion_history[-3:]]
        
        if all(intensities[i] < intensities[i+1] for i in range(len(intensities)-1)):
            return "increasing"
        elif all(intensities[i] > intensities[i+1] for i in range(len(intensities)-1)):
            return "decreasing"
        else:
            return "fluctuating"
    
    async def _generate_emotion_response(self, emotions: Dict[str, Any], cultural_context: Dict[str, Any]) -> str:
        """Generate culturally sensitive response to detected emotions."""
        
        primary_emotions = emotions["primary_emotions"]
        intensity = emotions["emotional_intensity"]
        
        if not primary_emotions:
            return self.format_response_culturally(
                "I'm listening to understand how you're feeling. Please continue sharing with me."
            )
        
        main_emotion = primary_emotions[0]
        
        # Base empathetic response
        if main_emotion == "sadness":
            base_response = "I can hear the sadness in your voice. It's completely natural to feel this way."
        elif main_emotion == "anxiety":
            base_response = "I notice you're feeling anxious. These worries are understandable."
        elif main_emotion == "anger":
            base_response = "I can sense your frustration and anger. These feelings are valid."
        elif main_emotion == "fear":
            base_response = "I hear the fear in what you're sharing. It's okay to feel scared."
        else:
            base_response = f"I can sense that you're feeling {main_emotion}. Thank you for sharing this with me."
        
        # Add cultural comfort if appropriate
        if cultural_context.get("religious_expressions"):
            if main_emotion in ["sadness", "fear", "anxiety"]:
                base_response += " Remember that Allah is with you in this difficulty."
        
        return self.format_response_culturally(base_response, "supportive")
    
    def _get_cultural_interpretation(self, emotions: Dict[str, Any], cultural_context: Dict[str, Any]) -> Dict[str, Any]:
        """Get cultural interpretation of emotions."""
        return {
            "cultural_emotional_style": "expressive" if cultural_context.get("arabic_language_used") else "reserved",
            "religious_coping_indicated": len(emotions.get("cultural_markers", [])) > 0,
            "family_context_important": cultural_context.get("family_context_mentioned", False),
            "community_expectations_factor": "social_pressure" in emotions.get("cultural_markers", [])
        }
    
    def _get_therapeutic_implications(self, emotions: Dict[str, Any]) -> List[str]:
        """Get therapeutic implications of detected emotions."""
        implications = []
        
        primary_emotions = emotions["primary_emotions"]
        intensity = emotions["emotional_intensity"]
        
        if "sadness" in primary_emotions and intensity > 6:
            implications.append("Consider depression screening")
        
        if "anxiety" in primary_emotions and intensity > 7:
            implications.append("Anxiety management techniques needed")
        
        if len(primary_emotions) > 2:
            implications.append("Complex emotional state - needs careful exploration")
        
        if intensity > 8:
            implications.append("High intensity requires immediate support")
        
        return implications
    
    def _get_pattern_recommendations(self, patterns: Dict[str, Any]) -> List[str]:
        """Get recommendations based on emotional patterns."""
        recommendations = []
        
        dominant = patterns.get("dominant_emotions", [])
        progression = patterns.get("emotional_progression", "")
        
        if "sadness" in dominant:
            recommendations.append("Focus on behavioral activation and mood lifting")
        
        if "anxiety" in dominant:
            recommendations.append("Implement anxiety management techniques")
        
        if progression == "declining":
            recommendations.append("Increase support and monitoring")
        elif progression == "improving":
            recommendations.append("Reinforce positive progress")
        
        return recommendations
    
    def _identify_cultural_strengths(self, analysis: Dict[str, Any]) -> List[str]:
        """Identify cultural strengths from analysis."""
        strengths = []
        
        if analysis["religious_expressions"]:
            strengths.append("Strong spiritual foundation")
        
        if analysis["family_dynamics_indicated"]:
            strengths.append("Family support system")
        
        if analysis["traditional_coping_mentioned"]:
            strengths.append("Traditional coping mechanisms")
        
        return strengths
    
    def _suggest_cultural_adaptations(self, analysis: Dict[str, Any]) -> List[str]:
        """Suggest cultural adaptations for therapy."""
        adaptations = []
        
        if analysis["social_expectations_pressure"]:
            adaptations.append("Address social pressure in therapy")
        
        if analysis["family_dynamics_indicated"]:
            adaptations.append("Consider family involvement in treatment")
        
        if analysis["religious_expressions"]:
            adaptations.append("Integrate spiritual coping in treatment")
        
        return adaptations
    
    def _get_intensity_interventions(self, crisis_level: str) -> List[str]:
        """Get interventions based on intensity level."""
        if crisis_level == "high":
            return [
                "Immediate crisis intervention",
                "Safety planning",
                "Professional referral",
                "Emergency contacts activation"
            ]
        elif crisis_level == "moderate":
            return [
                "Enhanced coping techniques",
                "Increased session frequency",
                "Support system activation",
                "Stress reduction techniques"
            ]
        else:
            return [
                "Standard therapeutic techniques",
                "Regular monitoring",
                "Skill building",
                "Prevention strategies"
            ]
    
    def _get_crisis_actions(self, crisis_level: str) -> List[str]:
        """Get immediate actions for crisis level."""
        if crisis_level == "severe":
            return [
                "Activate emergency protocols",
                "Ensure immediate safety",
                "Contact emergency services if needed",
                "Notify emergency contacts"
            ]
        elif crisis_level == "moderate":
            return [
                "Implement safety plan",
                "Increase monitoring",
                "Activate support system",
                "Consider professional consultation"
            ]
        else:
            return [
                "Continue regular support",
                "Monitor for changes",
                "Maintain therapeutic relationship",
                "Document emotional state"
            ] 