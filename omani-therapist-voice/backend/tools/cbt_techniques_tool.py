"""
CBT Techniques Tool for OMANI Therapist Voice.
Provides Cognitive Behavioral Therapy techniques adapted for Gulf Arabic/Islamic context.
"""

from typing import Dict, Any, List
from loguru import logger
from pipecat.adapters.schemas.function_schema import FunctionSchema
from .base_tool import BaseTool


class CBTTechniquesTool(BaseTool):
    """
    Cognitive Behavioral Therapy techniques tool for therapeutic sessions.
    
    Features:
    - Thought challenging techniques
    - Behavioral activation
    - Mood monitoring
    - Cultural adaptation for Islamic values
    - Arabic-specific therapeutic terminology
    """
    
    def __init__(self, rtvi_processor, task=None):
        """Initialize CBT techniques tool."""
        super().__init__(rtvi_processor, task)
        
        # CBT session tracking
        self.active_techniques = []
        self.thought_records = []
        self.mood_logs = []
        self.behavioral_experiments = []
        
        # Cultural adaptations
        self.islamic_cbt_principles = {
            "tawakkul": "Trust in Allah while taking action",
            "sabr": "Patience and perseverance",
            "shukr": "Gratitude practice",
            "istighfar": "Seeking forgiveness for healing"
        }
        
        logger.info("🧠 CBT Techniques Tool initialized")
    
    def get_tool_definition(self) -> FunctionSchema:
        """Define the CBT techniques tool for LLM function calling."""
        return FunctionSchema(
            name="apply_cbt_technique",
            description="Apply Cognitive Behavioral Therapy techniques adapted for Arabic/Islamic cultural context",
            properties={
                "technique": {
                    "type": "string",
                    "enum": [
                        "thought_challenging",
                        "behavioral_activation",
                        "mood_monitoring",
                        "cognitive_restructuring",
                        "grounding_techniques",
                        "islamic_cbt_integration",
                        "gratitude_practice",
                        "behavioral_experiment"
                    ],
                    "description": "CBT technique to apply"
                },
                "user_thoughts": {
                    "type": "string",
                    "description": "User's current negative thoughts or concerns"
                },
                "target_behavior": {
                    "type": "string",
                    "description": "Behavior to address or activate"
                },
                "mood_rating": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 10,
                    "description": "Current mood rating (1=very low, 10=very high)"
                },
                "cultural_context": {
                    "type": "object",
                    "properties": {
                        "religious_integration": {"type": "boolean"},
                        "family_involvement": {"type": "boolean"},
                        "arabic_preferred": {"type": "boolean"}
                    },
                    "description": "Cultural context for technique adaptation"
                },
                "session_goals": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Specific goals for this CBT session"
                }
            },
            required=["technique"]
        )
    
    async def execute(self, technique: str, **kwargs) -> str:
        """Execute CBT techniques."""
        valid_techniques = [
            "thought_challenging", "behavioral_activation", "mood_monitoring",
            "cognitive_restructuring", "grounding_techniques", "islamic_cbt_integration",
            "gratitude_practice", "behavioral_experiment"
        ]
        
        if not self.validate_action(technique, valid_techniques):
            return f"Invalid CBT technique. Use: {', '.join(valid_techniques)}"
        
        user_thoughts = kwargs.get("user_thoughts", "")
        target_behavior = kwargs.get("target_behavior", "")
        mood_rating = kwargs.get("mood_rating", 5)
        cultural_context = kwargs.get("cultural_context", {})
        session_goals = kwargs.get("session_goals", [])
        
        # Log CBT session
        await self.log_clinical_action(f"cbt_{technique}", {
            "user_thoughts_length": len(user_thoughts),
            "target_behavior": target_behavior,
            "mood_rating": mood_rating,
            "cultural_adaptations": cultural_context,
            "session_goals": session_goals
        })
        
        self.active_techniques.append(technique)
        
        if technique == "thought_challenging":
            return await self._apply_thought_challenging(user_thoughts, cultural_context)
        elif technique == "behavioral_activation":
            return await self._apply_behavioral_activation(target_behavior, cultural_context)
        elif technique == "mood_monitoring":
            return await self._apply_mood_monitoring(mood_rating)
        elif technique == "cognitive_restructuring":
            return await self._apply_cognitive_restructuring(user_thoughts, cultural_context)
        elif technique == "grounding_techniques":
            return await self._apply_grounding_techniques(cultural_context)
        elif technique == "islamic_cbt_integration":
            return await self._apply_islamic_cbt(user_thoughts, cultural_context)
        elif technique == "gratitude_practice":
            return await self._apply_gratitude_practice(cultural_context)
        elif technique == "behavioral_experiment":
            return await self._apply_behavioral_experiment(target_behavior, cultural_context)
    
    async def _apply_thought_challenging(self, user_thoughts: str, cultural_context: Dict[str, Any]) -> str:
        """Apply thought challenging technique with cultural adaptation."""
        
        # Create thought record
        thought_record = {
            "automatic_thought": user_thoughts,
            "emotion": "",
            "evidence_for": [],
            "evidence_against": [],
            "balanced_thought": "",
            "cultural_reframe": ""
        }
        
        # Islamic perspective integration if appropriate
        islamic_questions = [
            "Is this thought aligned with having good thoughts about Allah's wisdom?",
            "Am I being too harsh on myself when Allah is Oft-Forgiving?",
            "How would Prophet Muhammad (PBUH) view this situation?",
            "What would I advise a fellow Muslim facing this thought?"
        ]
        
        secular_questions = [
            "What evidence do I have that this thought is true?",
            "What evidence do I have that contradicts this thought?",
            "What would I tell a good friend having this thought?",
            "How might I think about this situation in 5 years?"
        ]
        
        # Choose questions based on cultural context
        questions = islamic_questions if cultural_context.get("religious_integration") else secular_questions
        
        response = self.format_response_culturally(
            "Let's examine this thought together using a structured approach. "
            "Sometimes our minds create thoughts that aren't completely accurate or helpful.",
            "supportive"
        )
        
        response += f"\n\nYour thought: '{user_thoughts}'"
        response += "\n\nLet's explore this thought by asking:"
        
        for i, question in enumerate(questions, 1):
            response += f"\n{i}. {question}"
        
        # Add cultural wisdom
        if cultural_context.get("religious_integration"):
            response += "\n\nRemember the hadith: 'No fatigue, nor disease, nor sorrow, nor sadness, nor hurt befalls a Muslim - not even a prick from a thorn - except that Allah removes his sins thereby.' Your struggles have meaning and purpose."
        
        thought_record["cultural_questions"] = questions
        self.thought_records.append(thought_record)
        
        await self.send_client_command("thought_challenging_worksheet", {
            "thought_record": thought_record,
            "questions": questions,
            "cultural_adaptations": cultural_context
        })
        
        return response
    
    async def _apply_behavioral_activation(self, target_behavior: str, cultural_context: Dict[str, Any]) -> str:
        """Apply behavioral activation technique."""
        
        # Create activity schedule
        pleasant_activities = {
            "spiritual": [
                "Prayer and dhikr",
                "Reading Quran",
                "Visiting mosque",
                "Islamic study circles"
            ],
            "social": [
                "Family gatherings",
                "Visiting relatives",
                "Community service",
                "Friend meetups"
            ],
            "physical": [
                "Walking in nature",
                "Swimming",
                "Traditional sports",
                "Gentle exercise"
            ],
            "creative": [
                "Arabic calligraphy",
                "Traditional crafts",
                "Cooking traditional food",
                "Poetry writing"
            ],
            "self_care": [
                "Taking a shower",
                "Grooming",
                "Organizing space",
                "Listening to Quran"
            ]
        }
        
        # Customize based on cultural context
        if cultural_context.get("religious_integration"):
            recommended_activities = pleasant_activities["spiritual"] + pleasant_activities["social"]
        else:
            recommended_activities = pleasant_activities["physical"] + pleasant_activities["creative"]
        
        activity_plan = {
            "target_behavior": target_behavior,
            "small_steps": self._break_into_small_steps(target_behavior),
            "pleasant_activities": recommended_activities[:5],
            "scheduling": "Start with 10-15 minutes daily",
            "tracking": True
        }
        
        self.behavioral_experiments.append(activity_plan)
        
        response = self.format_response_culturally(
            "Let's work on increasing positive activities in your life. "
            "When we're feeling low, we often stop doing things that bring us joy and meaning.",
            "encouraging"
        )
        
        response += f"\n\nTarget behavior: {target_behavior}"
        response += "\n\nLet's break this down into small, manageable steps:"
        
        for i, step in enumerate(activity_plan["small_steps"], 1):
            response += f"\n{i}. {step}"
        
        response += "\n\nPleasant activities to try:"
        for activity in recommended_activities[:3]:
            response += f"\n• {activity}"
        
        if cultural_context.get("religious_integration"):
            response += "\n\nRemember: 'And whoever relies upon Allah - then He is sufficient for him. Indeed, Allah will accomplish His purpose.' (Quran 65:3). Take one step at a time with trust in Allah."
        
        await self.send_client_command("behavioral_activation_plan", {
            "activity_plan": activity_plan,
            "cultural_activities": recommended_activities
        })
        
        return response
    
    async def _apply_mood_monitoring(self, mood_rating: int) -> str:
        """Apply mood monitoring technique."""
        
        mood_entry = {
            "rating": mood_rating,
            "timestamp": self._get_timestamp(),
            "activities": [],
            "thoughts": "",
            "physical_symptoms": []
        }
        
        self.mood_logs.append(mood_entry)
        
        # Mood interpretation with cultural sensitivity
        if mood_rating <= 3:
            mood_description = "very low"
            arabic_description = "منخفض جداً"
            encouragement = "This is a difficult time, but feelings change. You're taking a positive step by monitoring your mood."
        elif mood_rating <= 5:
            mood_description = "low to moderate"
            arabic_description = "منخفض إلى متوسط"
            encouragement = "Your awareness of your mood is a strength. Small improvements are possible."
        elif mood_rating <= 7:
            mood_description = "moderate"
            arabic_description = "متوسط"
            encouragement = "This is a manageable level. Let's work on techniques to improve further."
        else:
            mood_description = "good"
            arabic_description = "جيد"
            encouragement = "This is a positive mood level. Let's identify what's helping you feel this way."
        
        response = f"Your current mood rating: {mood_rating}/10 ({mood_description} / {arabic_description})"
        response += f"\n\n{encouragement}"
        
        response += "\n\nMood tracking helps us:"
        response += "\n• Identify patterns and triggers"
        response += "\n• Recognize what activities improve mood"
        response += "\n• See progress over time"
        response += "\n• Make informed decisions about self-care"
        
        await self.send_client_command("mood_log_entry", {
            "mood_entry": mood_entry,
            "mood_trend": self._analyze_mood_trend(),
            "recommendations": self._get_mood_based_recommendations(mood_rating)
        })
        
        return self.format_response_culturally(response)
    
    async def _apply_cognitive_restructuring(self, user_thoughts: str, cultural_context: Dict[str, Any]) -> str:
        """Apply cognitive restructuring with cultural sensitivity."""
        
        # Handle None or empty user_thoughts
        if not user_thoughts:
            return self.format_response_culturally(
                "I'm here to help you work through your thoughts. Please share what's on your mind when you're ready."
            )
        
        # Common cognitive distortions with Arabic translations
        cognitive_distortions = {
            "all_or_nothing": {
                "english": "All-or-nothing thinking",
                "arabic": "التفكير بالأبيض والأسود",
                "description": "Seeing things as completely good or bad, with no middle ground"
            },
            "catastrophizing": {
                "english": "Catastrophizing",
                "arabic": "التوقع الأسوأ",
                "description": "Expecting the worst possible outcome"
            },
            "mind_reading": {
                "english": "Mind reading",
                "arabic": "قراءة الأفكار",
                "description": "Assuming you know what others think"
            },
            "emotional_reasoning": {
                "english": "Emotional reasoning",
                "arabic": "التفكير العاطفي",
                "description": "Believing feelings are facts"
            }
        }
        
        # Analyze for distortions (simplified)
        detected_distortions = []
        thought_lower = user_thoughts.lower()
        
        if any(word in thought_lower for word in ["always", "never", "completely", "totally"]):
            detected_distortions.append("all_or_nothing")
        if any(word in thought_lower for word in ["terrible", "awful", "disaster", "horrible"]):
            detected_distortions.append("catastrophizing")
        
        response = self.format_response_culturally(
            "Let's restructure this thought to make it more balanced and helpful. "
            "Our thoughts greatly influence how we feel and behave.",
            "supportive"
        )
        
        if detected_distortions:
            response += f"\n\nI notice some thinking patterns that might be making you feel worse:"
            for distortion in detected_distortions:
                info = cognitive_distortions[distortion]
                response += f"\n• {info['english']} ({info['arabic']}): {info['description']}"
        
        # Restructuring questions
        restructuring_questions = [
            "What's a more balanced way to think about this?",
            "What evidence supports and challenges this thought?",
            "What would you tell a friend in this situation?",
            "How might this situation teach you something valuable?"
        ]
        
        if cultural_context.get("religious_integration"):
            restructuring_questions.append("How might this challenge be a test that strengthens your faith?")
            restructuring_questions.append("What duas or verses might bring comfort in this situation?")
        
        response += "\n\nLet's work through these questions:"
        for i, question in enumerate(restructuring_questions, 1):
            response += f"\n{i}. {question}"
        
        await self.send_client_command("cognitive_restructuring_worksheet", {
            "original_thought": user_thoughts,
            "detected_distortions": detected_distortions,
            "restructuring_questions": restructuring_questions
        })
        
        return response
    
    async def _apply_grounding_techniques(self, cultural_context: Dict[str, Any]) -> str:
        """Apply grounding techniques for anxiety and distress."""
        
        # 5-4-3-2-1 grounding technique with cultural adaptation
        grounding_steps = [
            "5 things you can see around you",
            "4 things you can touch or feel",
            "3 things you can hear",
            "2 things you can smell",
            "1 thing you can taste"
        ]
        
        islamic_grounding = [
            "Recite 'La hawla wa la quwwata illa billah' (There is no power except with Allah)",
            "Take deep breaths while saying 'SubhanAllah' (Glory be to Allah)",
            "Place your hand on your heart and feel Allah's creation working within you",
            "Look around and say 'Alhamdulillahi rabbil alameen' for what you can see",
            "Remember that Allah is with you: 'And He is with you wherever you are' (57:4)"
        ]
        
        chosen_technique = islamic_grounding if cultural_context.get("religious_integration") else grounding_steps
        
        response = self.format_response_culturally(
            "Let's use a grounding technique to help you feel more present and calm. "
            "This will help bring you back to the here and now.",
            "supportive"
        )
        
        response += "\n\nLet's do this together. Take your time with each step:"
        
        for i, step in enumerate(chosen_technique, 1):
            response += f"\n{i}. {step}"
        
        response += "\n\nTake slow, deep breaths between each step. There's no rush."
        
        if cultural_context.get("religious_integration"):
            response += "\n\nRemember: 'And whoever fears Allah - He will make for him a way out.' (Quran 65:2)"
        
        await self.send_client_command("grounding_exercise", {
            "technique_type": "islamic" if cultural_context.get("religious_integration") else "secular",
            "steps": chosen_technique
        })
        
        return response
    
    async def _apply_islamic_cbt(self, user_thoughts: str, cultural_context: Dict[str, Any]) -> str:
        """Apply CBT integrated with Islamic principles."""
        
        # Handle None or empty user_thoughts
        if not user_thoughts:
            return self.format_response_culturally(
                "I'm here to help you work through your thoughts. Please share what's on your mind when you're ready."
            )

        islamic_cbt_concepts = {
            "tawakkul": {
                "concept": "Trust in Allah after taking action",
                "application": "Do your best, then trust Allah with the outcome",
                "verse": "'And upon Allah rely, if you should be believers.' (5:23)"
            },
            "sabr": {
                "concept": "Patience and perseverance through trials",
                "application": "This difficulty is temporary and has wisdom",
                "verse": "'And give good tidings to the patient.' (2:155)"
            },
            "qadar": {
                "concept": "Divine decree and wisdom in all events",
                "application": "There is wisdom in what Allah has decreed",
                "verse": "'But perhaps you hate a thing and it is good for you.' (2:216)"
            }
        }
        
        # Determine most relevant concept based on thoughts
        if any(word in user_thoughts.lower() for word in ["worry", "anxious", "control"]):
            relevant_concept = "tawakkul"
        elif any(word in user_thoughts.lower() for word in ["difficult", "hard", "struggle"]):
            relevant_concept = "sabr"
        else:
            relevant_concept = "qadar"
        
        concept_info = islamic_cbt_concepts[relevant_concept]
        
        response = self.format_response_culturally(
            "Let's look at this situation through the lens of Islamic wisdom and modern psychology. "
            "Islam provides us with powerful tools for mental and spiritual wellbeing."
        )
        
        response += f"\n\nThe Islamic concept that applies here is **{relevant_concept.upper()}**:"
        response += f"\n• Meaning: {concept_info['concept']}"
        response += f"\n• Application: {concept_info['application']}"
        response += f"\n• Quranic guidance: {concept_info['verse']}"
        
        response += f"\n\nHow can we apply this to your situation?"
        response += f"\n1. Acknowledge your feelings as valid - Islam recognizes human emotions"
        response += f"\n2. Apply the principle of {relevant_concept} to find peace"
        response += f"\n3. Take positive action while trusting in Allah's wisdom"
        response += f"\n4. Remember that trials are opportunities for spiritual growth"
        
        response += "\n\nDua for relief: 'اللهم لا سهل إلا ما جعلته سهلاً وأنت تجعل الحزن إذا شئت سهلاً'"
        response += "\n(O Allah, nothing is easy except what You make easy, and You make the difficult easy if You wish.)"
        
        await self.send_client_command("islamic_cbt_guidance", {
            "concept": relevant_concept,
            "concept_info": concept_info,
            "practical_steps": [
                "Make dua for guidance and ease",
                "Apply the Islamic principle practically", 
                "Take positive action",
                "Trust in Allah's wisdom"
            ]
        })
        
        return response
    
    async def _apply_gratitude_practice(self, cultural_context: Dict[str, Any]) -> str:
        """Apply gratitude practice with cultural adaptation."""
        
        gratitude_prompts = {
            "islamic": [
                "What blessings from Allah are you grateful for today?",
                "Which of your senses allowed you to experience beauty today?",
                "What act of kindness did you witness or receive?",
                "How did Allah make things easy for you today?",
                "What in your faith brings you comfort?"
            ],
            "general": [
                "What three things went well today?",
                "Who in your life are you grateful for?",
                "What ability or skill are you thankful for?",
                "What in nature brought you peace today?",
                "What small pleasure did you enjoy today?"
            ]
        }
        
        prompts = gratitude_prompts["islamic"] if cultural_context.get("religious_integration") else gratitude_prompts["general"]
        
        response = self.format_response_culturally(
            "Gratitude practice is a powerful tool for improving mood and perspective. "
            "Let's focus on the positive aspects of your life, no matter how small.",
            "encouraging"
        )
        
        if cultural_context.get("religious_integration"):
            response += "\n\nThe Quran says: 'If you are grateful, I will certainly give you more.' (14:7)"
            response += "\nGratitude (Shukr) is both a practice and a way of seeing Allah's blessings."
        
        response += "\n\nTake a moment to reflect on these questions:"
        for i, prompt in enumerate(prompts[:3], 1):
            response += f"\n{i}. {prompt}"
        
        response += "\n\nTry to be specific and really feel the gratitude as you think of each answer."
        
        if cultural_context.get("religious_integration"):
            response += "\n\nEnd with: 'الحمد لله رب العالمين' (All praise belongs to Allah, Lord of the worlds)"
        
        await self.send_client_command("gratitude_practice", {
            "prompts": prompts,
            "cultural_type": "islamic" if cultural_context.get("religious_integration") else "general"
        })
        
        return response
    
    async def _apply_behavioral_experiment(self, target_behavior: str, cultural_context: Dict[str, Any]) -> str:
        """Design a behavioral experiment to test assumptions."""
        
        experiment = {
            "hypothesis": f"What will happen if I {target_behavior}?",
            "prediction": "",
            "experiment_steps": self._break_into_small_steps(target_behavior),
            "success_criteria": "Completion and observation of actual outcomes",
            "safety_measures": [],
            "cultural_considerations": []
        }
        
        if cultural_context.get("family_involvement"):
            experiment["cultural_considerations"].append("Include family support where appropriate")
        
        if cultural_context.get("religious_integration"):
            experiment["cultural_considerations"].append("Begin with Bismillah and make dua for success")
            experiment["safety_measures"].append("Ensure actions align with Islamic values")
        
        response = self.format_response_culturally(
            "Let's design a behavioral experiment to test your assumptions about this behavior. "
            "Often our fears about doing something are worse than the reality.",
            "encouraging"
        )
        
        response += f"\n\nExperiment: {experiment['hypothesis']}"
        response += "\n\nSteps to try:"
        for i, step in enumerate(experiment["experiment_steps"], 1):
            response += f"\n{i}. {step}"
        
        response += "\n\nWhat to observe:"
        response += "\n• How did you feel before, during, and after?"
        response += "\n• What actually happened vs. what you expected?"
        response += "\n• What did you learn about yourself?"
        response += "\n• How might this apply to similar situations?"
        
        await self.send_client_command("behavioral_experiment", {
            "experiment": experiment,
            "tracking_form": True
        })
        
        return response
    
    def _break_into_small_steps(self, behavior: str) -> List[str]:
        """Break a behavior into small, manageable steps."""
        # This is a simplified version - could be enhanced with AI analysis
        return [
            f"Plan when to do: {behavior}",
            f"Prepare what you need for: {behavior}",
            f"Start with 5-10 minutes of: {behavior}",
            f"Complete the full: {behavior}",
            f"Reflect on the experience of: {behavior}"
        ]
    
    def _analyze_mood_trend(self) -> Dict[str, Any]:
        """Analyze mood trends from recent logs."""
        if len(self.mood_logs) < 2:
            return {"trend": "insufficient_data", "direction": "unknown"}
        
        recent_ratings = [log["rating"] for log in self.mood_logs[-5:]]
        if len(recent_ratings) >= 2:
            if recent_ratings[-1] > recent_ratings[0]:
                return {"trend": "improving", "direction": "upward"}
            elif recent_ratings[-1] < recent_ratings[0]:
                return {"trend": "declining", "direction": "downward"}
            else:
                return {"trend": "stable", "direction": "steady"}
        
        return {"trend": "stable", "direction": "steady"}
    
    def _get_mood_based_recommendations(self, mood_rating: int) -> List[str]:
        """Get recommendations based on current mood rating."""
        if mood_rating <= 3:
            return [
                "Consider crisis support if needed",
                "Practice grounding techniques",
                "Reach out to a trusted person",
                "Focus on basic self-care"
            ]
        elif mood_rating <= 5:
            return [
                "Try a pleasant activity",
                "Practice gratitude",
                "Get some gentle movement",
                "Connect with others"
            ]
        else:
            return [
                "Maintain current positive activities",
                "Set small goals for growth",
                "Help others if possible",
                "Practice mindfulness"
            ] 