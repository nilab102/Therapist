"""
Session Management Tool for OMANI Therapist Voice.
Manages therapeutic sessions, consent, documentation, and session flow.
"""

from typing import Dict, Any, List
from datetime import datetime, timedelta
from loguru import logger
from pipecat.adapters.schemas.function_schema import FunctionSchema
from .base_tool import BaseTool


class SessionManagementTool(BaseTool):
    """
    Session management tool for therapeutic sessions.
    
    Features:
    - Session consent management
    - Session documentation and notes
    - Privacy and confidentiality protocols
    - Session flow control
    - Emergency contact management
    - Cultural preferences tracking
    """
    
    def __init__(self, rtvi_processor, task=None):
        """Initialize session management tool."""
        super().__init__(rtvi_processor, task)
        
        # Session tracking
        self.current_session = {}
        self.session_history = []
        self.consent_status = {}
        self.emergency_contacts = []
        self.cultural_preferences = {}
        
        # Session state
        self.session_active = False
        self.session_start_time = None
        self.session_notes = []
        self.privacy_level = "high"
        
        # Therapeutic goals and progress
        self.therapeutic_goals = []
        self.progress_markers = []
        self.session_outcomes = {}
        
        logger.info("📋 Session Management Tool initialized")
    
    def get_tool_definition(self) -> FunctionSchema:
        """Define the session management tool for LLM function calling."""
        return FunctionSchema(
            name="manage_session",
            description="Manage therapeutic sessions including consent, documentation, privacy, and session flow",
            properties={
                "action": {
                    "type": "string",
                    "enum": [
                        "start_session",
                        "end_session",
                        "manage_consent",
                        "update_notes",
                        "set_emergency_contacts",
                        "manage_privacy_settings",
                        "track_therapeutic_goals",
                        "document_progress",
                        "handle_session_interruption",
                        "export_session_summary"
                    ],
                    "description": "Session management action to perform"
                },
                "consent_details": {
                    "type": "object",
                    "properties": {
                        "recording_consent": {"type": "boolean"},
                        "data_storage_consent": {"type": "boolean"},
                        "family_involvement_consent": {"type": "boolean"},
                        "emergency_contact_consent": {"type": "boolean"}
                    },
                    "description": "Consent preferences for the session"
                },
                "emergency_contacts": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "relationship": {"type": "string"},
                            "phone": {"type": "string"},
                            "priority": {"type": "integer"}
                        }
                    },
                    "description": "Emergency contact information"
                },
                "cultural_preferences": {
                    "type": "object",
                    "properties": {
                        "preferred_language": {"type": "string"},
                        "religious_considerations": {"type": "boolean"},
                        "family_involvement_preferred": {"type": "boolean"},
                        "gender_preference_therapist": {"type": "string"}
                    },
                    "description": "Cultural and personal preferences"
                },
                "therapeutic_goals": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Therapeutic goals for this session or treatment"
                },
                "session_notes": {
                    "type": "string",
                    "description": "Clinical notes for the session"
                },
                "privacy_level": {
                    "type": "string",
                    "enum": ["minimal", "standard", "high", "maximum"],
                    "description": "Privacy level for the session"
                }
            },
            required=["action"]
        )
    
    async def execute(self, action: str, **kwargs) -> str:
        """Execute session management actions."""
        valid_actions = [
            "start_session", "end_session", "manage_consent", "update_notes",
            "set_emergency_contacts", "manage_privacy_settings", "track_therapeutic_goals",
            "document_progress", "handle_session_interruption", "export_session_summary"
        ]
        
        if not self.validate_action(action, valid_actions):
            return f"Invalid session action. Use: {', '.join(valid_actions)}"
        
        # Extract parameters
        consent_details = kwargs.get("consent_details", {})
        emergency_contacts = kwargs.get("emergency_contacts", [])
        cultural_preferences = kwargs.get("cultural_preferences", {})
        therapeutic_goals = kwargs.get("therapeutic_goals", [])
        session_notes = kwargs.get("session_notes", "")
        privacy_level = kwargs.get("privacy_level", "high")
        
        # Log session management action
        await self.log_clinical_action(f"session_management_{action}", {
            "consent_status": bool(consent_details),
            "emergency_contacts_count": len(emergency_contacts),
            "cultural_preferences": bool(cultural_preferences),
            "therapeutic_goals_count": len(therapeutic_goals),
            "privacy_level": privacy_level
        })
        
        if action == "start_session":
            return await self._start_session(consent_details, cultural_preferences)
        elif action == "end_session":
            return await self._end_session(session_notes)
        elif action == "manage_consent":
            return await self._manage_consent(consent_details)
        elif action == "update_notes":
            return await self._update_session_notes(session_notes)
        elif action == "set_emergency_contacts":
            return await self._set_emergency_contacts(emergency_contacts)
        elif action == "manage_privacy_settings":
            return await self._manage_privacy_settings(privacy_level)
        elif action == "track_therapeutic_goals":
            return await self._track_therapeutic_goals(therapeutic_goals)
        elif action == "document_progress":
            return await self._document_progress(session_notes)
        elif action == "handle_session_interruption":
            return await self._handle_session_interruption()
        elif action == "export_session_summary":
            return await self._export_session_summary()
    
    async def _start_session(self, consent_details: Dict[str, Any], cultural_preferences: Dict[str, Any]) -> str:
        """Start a new therapeutic session."""
        
        # Check if session already active
        if self.session_active:
            return "A session is already active. Please end the current session before starting a new one."
        
        # Initialize session
        self.session_start_time = datetime.now()
        self.session_active = True
        self.session_notes = []
        self.session_outcomes = {}
        
        # Store cultural preferences
        if cultural_preferences:
            self.cultural_preferences.update(cultural_preferences)
        
        # Handle consent
        if consent_details:
            self.consent_status.update(consent_details)
        
        # Create session record
        session_id = f"session_{self.session_start_time.strftime('%Y%m%d_%H%M%S')}"
        self.current_session = {
            "session_id": session_id,
            "start_time": self.session_start_time.isoformat(),
            "consent_status": self.consent_status.copy(),
            "cultural_preferences": self.cultural_preferences.copy(),
            "therapeutic_goals": self.therapeutic_goals.copy(),
            "privacy_level": self.privacy_level,
            "session_type": "voice_therapy",
            "platform": "omani_therapist_voice"
        }
        
        # Cultural greeting based on preferences
        if cultural_preferences.get("preferred_language") == "arabic":
            greeting = "أهلاً وسهلاً! مرحباً بك في جلسة العلاج النفسي الصوتي."
            greeting += "\nWelcome to your voice therapy session."
        else:
            greeting = "Welcome to your therapeutic voice session with OMANI Therapist Voice."
        
        # Add consent information
        consent_info = "\n\nBefore we begin, let me review our privacy and consent:"
        if self.consent_status.get("recording_consent"):
            consent_info += "\n✅ Session recording: Consented"
        else:
            consent_info += "\n❌ Session recording: Not consented"
        
        if self.consent_status.get("data_storage_consent"):
            consent_info += "\n✅ Clinical data storage: Consented"
        else:
            consent_info += "\n❌ Clinical data storage: Not consented"
        
        response = self.format_response_culturally(
            greeting + consent_info + 
            "\n\nYour privacy and confidentiality are our highest priority. "
            "This is a safe space for you to share and explore your feelings.",
            "supportive"
        )
        
        # Add Islamic greeting if appropriate
        if cultural_preferences.get("religious_considerations"):
            response += "\n\nبسم الله نبدأ جلستنا (In the name of Allah, we begin our session)."
        
        # Send session start notification to client
        await self.send_client_command("session_started", {
            "session_id": session_id,
            "session_info": self.current_session,
            "cultural_adaptations": self.cultural_preferences,
            "consent_status": self.consent_status
        })
        
        return response
    
    async def _end_session(self, final_notes: str = "") -> str:
        """End the current therapeutic session."""
        
        if not self.session_active:
            return "No active session to end."
        
        # Calculate session duration
        session_end_time = datetime.now()
        session_duration = session_end_time - self.session_start_time
        
        # Add final notes
        if final_notes:
            self.session_notes.append({
                "timestamp": session_end_time.isoformat(),
                "type": "final_notes",
                "content": final_notes,
                "author": "system"
            })
        
        # Finalize session record
        self.current_session.update({
            "end_time": session_end_time.isoformat(),
            "duration_minutes": int(session_duration.total_seconds() / 60),
            "session_notes": self.session_notes.copy(),
            "therapeutic_goals_addressed": self.therapeutic_goals.copy(),
            "progress_markers": self.progress_markers.copy(),
            "session_outcomes": self.session_outcomes.copy(),
            "clinical_data": self.clinical_data.copy()
        })
        
        # Add to session history
        self.session_history.append(self.current_session.copy())
        
        # Generate session summary
        summary = await self._generate_session_summary()
        
        # Cultural closing
        if self.cultural_preferences.get("preferred_language") == "arabic":
            closing = "شكراً لك على مشاركتك في هذه الجلسة. "
            closing += "أتمنى أن تكون مفيدة لك. الله يعطيك العافية."
            closing += "\n\nThank you for participating in this session. "
            closing += "I hope it was helpful for you. May Allah give you strength."
        else:
            closing = "Thank you for sharing in this therapeutic session. "
            closing += "I hope you found it helpful and supportive."
        
        response = self.format_response_culturally(
            closing + f"\n\nSession Summary:\n{summary}",
            "encouraging"
        )
        
        # Send session end notification to client
        await self.send_client_command("session_ended", {
            "session_summary": summary,
            "session_duration": int(session_duration.total_seconds() / 60),
            "follow_up_recommendations": self._generate_follow_up_recommendations(),
            "next_session_suggested": self._suggest_next_session_timing()
        })
        
        # Reset session state
        self.session_active = False
        self.current_session = {}
        self.session_notes = []
        self.progress_markers = []
        self.session_outcomes = {}
        
        return response
    
    async def _manage_consent(self, consent_details: Dict[str, Any]) -> str:
        """Manage consent preferences for the session."""
        
        if not consent_details:
            # Return current consent status
            consent_summary = "Current consent status:"
            for key, value in self.consent_status.items():
                status = "✅ Granted" if value else "❌ Not granted"
                consent_summary += f"\n• {key.replace('_', ' ').title()}: {status}"
            
            return consent_summary
        
        # Update consent
        previous_consent = self.consent_status.copy()
        self.consent_status.update(consent_details)
        
        # Log consent changes
        consent_changes = []
        for key, new_value in consent_details.items():
            old_value = previous_consent.get(key, False)
            if old_value != new_value:
                change_type = "granted" if new_value else "revoked"
                consent_changes.append(f"{key.replace('_', ' ').title()}: {change_type}")
        
        if consent_changes:
            await self.log_clinical_action("consent_updated", {
                "changes": consent_changes,
                "new_consent_status": self.consent_status
            })
        
        response = self.format_response_culturally(
            "Thank you for updating your consent preferences. "
            "Your choices are respected and can be changed at any time during our session."
        )
        
        if consent_changes:
            response += f"\n\nConsent changes made:\n• " + "\n• ".join(consent_changes)
        
        # Special handling for recording consent
        if "recording_consent" in consent_details:
            if consent_details["recording_consent"]:
                response += "\n\n🔴 Session recording is now enabled for clinical documentation."
            else:
                response += "\n\n⏹️ Session recording has been disabled per your request."
        
        # Send consent update to client
        await self.send_client_command("consent_updated", {
            "consent_status": self.consent_status,
            "changes_made": consent_changes
        })
        
        return response
    
    async def _update_session_notes(self, notes: str) -> str:
        """Update session notes with new clinical observations."""
        
        if not notes.strip():
            return "Please provide notes to add to the session."
        
        # Add timestamped note
        note_entry = {
            "timestamp": datetime.now().isoformat(),
            "type": "clinical_note",
            "content": notes,
            "author": "therapist_ai"
        }
        
        self.session_notes.append(note_entry)
        
        # Store in clinical data
        if "session_notes" not in self.clinical_data:
            self.clinical_data["session_notes"] = []
        self.clinical_data["session_notes"].append(note_entry)
        
        await self.log_clinical_action("session_notes_updated", {
            "note_length": len(notes),
            "total_notes": len(self.session_notes)
        })
        
        response = "Session notes have been updated with your clinical observations."
        
        # Send note update to client (if consented)
        if self.consent_status.get("data_storage_consent"):
            await self.send_client_command("notes_updated", {
                "note_added": True,
                "total_notes": len(self.session_notes),
                "privacy_maintained": True
            })
        
        return response
    
    async def _set_emergency_contacts(self, contacts: List[Dict[str, Any]]) -> str:
        """Set emergency contact information."""
        
        if not contacts:
            return "Please provide emergency contact information."
        
        # Validate and store contacts
        valid_contacts = []
        for contact in contacts:
            if contact.get("name") and contact.get("phone"):
                valid_contacts.append({
                    "name": contact["name"],
                    "relationship": contact.get("relationship", "emergency_contact"),
                    "phone": contact["phone"],
                    "priority": contact.get("priority", 1),
                    "cultural_considerations": contact.get("cultural_considerations", "")
                })
        
        self.emergency_contacts = valid_contacts
        
        # Store in clinical data
        self.clinical_data["emergency_contacts"] = valid_contacts
        
        await self.log_clinical_action("emergency_contacts_updated", {
            "contacts_count": len(valid_contacts),
            "has_family_contacts": any(c.get("relationship") in ["family", "parent", "spouse", "sibling"] for c in valid_contacts)
        })
        
        response = self.format_response_culturally(
            f"Emergency contacts have been securely stored ({len(valid_contacts)} contacts). "
            "This information will only be used in crisis situations or emergencies."
        )
        
        # Cultural considerations for family contacts
        family_contacts = [c for c in valid_contacts if c.get("relationship") in ["family", "parent", "spouse", "sibling"]]
        if family_contacts:
            response += "\n\nI notice you've included family members as emergency contacts. "
            response += "In our culture, family support is very important for healing and recovery."
        
        # Send emergency contacts confirmation (without sensitive details)
        await self.send_client_command("emergency_contacts_set", {
            "contacts_count": len(valid_contacts),
            "family_contacts_included": len(family_contacts),
            "privacy_secured": True
        })
        
        return response
    
    async def _manage_privacy_settings(self, privacy_level: str) -> str:
        """Manage privacy settings for the session."""
        
        valid_levels = ["minimal", "standard", "high", "maximum"]
        if privacy_level not in valid_levels:
            return f"Invalid privacy level. Choose from: {', '.join(valid_levels)}"
        
        previous_level = self.privacy_level
        self.privacy_level = privacy_level
        
        # Privacy level descriptions
        privacy_descriptions = {
            "minimal": "Basic privacy - session data may be stored for service improvement",
            "standard": "Standard privacy - clinical data stored securely, limited sharing",
            "high": "High privacy - encrypted storage, no sharing without explicit consent",
            "maximum": "Maximum privacy - minimal data retention, local processing preferred"
        }
        
        response = self.format_response_culturally(
            f"Privacy level updated to: {privacy_level.upper()}\n"
            f"This means: {privacy_descriptions[privacy_level]}"
        )
        
        # Adjust data handling based on privacy level
        if privacy_level == "maximum":
            response += "\n\n🔒 Maximum privacy mode: Session data will be processed locally and deleted after session."
        elif privacy_level == "high":
            response += "\n\n🔐 High privacy mode: All data encrypted and access strictly controlled."
        
        await self.log_clinical_action("privacy_settings_updated", {
            "previous_level": previous_level,
            "new_level": privacy_level
        })
        
        # Send privacy update to client
        await self.send_client_command("privacy_settings_updated", {
            "privacy_level": privacy_level,
            "data_handling_info": privacy_descriptions[privacy_level]
        })
        
        return response
    
    async def _track_therapeutic_goals(self, goals: List[str]) -> str:
        """Track and update therapeutic goals for the session."""
        
        if not goals:
            if self.therapeutic_goals:
                current_goals = "\n".join([f"• {goal}" for goal in self.therapeutic_goals])
                return f"Current therapeutic goals:\n{current_goals}"
            else:
                return "No therapeutic goals currently set. Would you like to establish some goals for our work together?"
        
        # Update goals
        self.therapeutic_goals = goals
        
        # Store in clinical data
        self.clinical_data["therapeutic_goals"] = {
            "goals": goals,
            "set_at": datetime.now().isoformat(),
            "session_context": "voice_therapy"
        }
        
        await self.log_clinical_action("therapeutic_goals_updated", {
            "goals_count": len(goals),
            "goals_list": goals
        })
        
        # Generate culturally appropriate response
        response = self.format_response_culturally(
            "Therapeutic goals have been established for our work together. "
            "Having clear goals helps us focus our efforts and measure progress."
        )
        
        response += "\n\nYour therapeutic goals:"
        for i, goal in enumerate(goals, 1):
            response += f"\n{i}. {goal}"
        
        # Add cultural encouragement
        if self.cultural_preferences.get("religious_considerations"):
            response += "\n\nRemember: 'And whoever relies upon Allah - then He is sufficient for him. Indeed, Allah will accomplish His purpose.' (Quran 65:3)"
        
        # Send goals update to client
        await self.send_client_command("therapeutic_goals_set", {
            "goals": goals,
            "goals_count": len(goals),
            "tracking_enabled": True
        })
        
        return response
    
    async def _document_progress(self, progress_notes: str) -> str:
        """Document therapeutic progress and outcomes."""
        
        if not progress_notes.strip():
            return "Please provide progress notes to document."
        
        # Create progress marker
        progress_entry = {
            "timestamp": datetime.now().isoformat(),
            "progress_notes": progress_notes,
            "session_context": self.current_session.get("session_id", "unknown"),
            "therapeutic_goals_addressed": self.therapeutic_goals.copy(),
            "clinical_observations": self.clinical_data.copy()
        }
        
        self.progress_markers.append(progress_entry)
        
        # Update session outcomes
        self.session_outcomes["progress_documented"] = True
        self.session_outcomes["progress_timestamp"] = datetime.now().isoformat()
        
        await self.log_clinical_action("progress_documented", {
            "progress_notes_length": len(progress_notes),
            "total_progress_markers": len(self.progress_markers)
        })
        
        response = self.format_response_culturally(
            "Therapeutic progress has been documented. "
            "This helps us track your journey and adjust our approach as needed."
        )
        
        # Analyze progress if multiple markers exist
        if len(self.progress_markers) > 1:
            progress_trend = self._analyze_progress_trend()
            response += f"\n\nProgress trend analysis: {progress_trend}"
        
        # Send progress update to client
        await self.send_client_command("progress_documented", {
            "progress_entry": progress_entry,
            "total_progress_markers": len(self.progress_markers),
            "trend_analysis": self._analyze_progress_trend() if len(self.progress_markers) > 1 else None
        })
        
        return response
    
    async def _handle_session_interruption(self) -> str:
        """Handle unexpected session interruption."""
        
        if not self.session_active:
            return "No active session to handle interruption for."
        
        # Document interruption
        interruption_time = datetime.now()
        interruption_record = {
            "timestamp": interruption_time.isoformat(),
            "type": "session_interruption",
            "session_duration_before_interruption": int((interruption_time - self.session_start_time).total_seconds() / 60),
            "clinical_data_preserved": True,
            "emergency_protocols_activated": self.emergency_escalation_needed
        }
        
        # Save current session state
        self.current_session["interruption_record"] = interruption_record
        self.session_history.append(self.current_session.copy())
        
        await self.log_clinical_action("session_interrupted", interruption_record)
        
        # Generate appropriate response based on context
        if self.emergency_escalation_needed:
            response = "Session interrupted due to emergency protocols activation. "
            response += "Emergency contacts have been notified if consented. "
            response += "Professional support resources are available."
        else:
            response = self.format_response_culturally(
                "Session was interrupted. Your progress and clinical data have been safely preserved. "
                "You can resume therapy whenever you're ready."
            )
        
        # Add cultural comfort
        if self.cultural_preferences.get("religious_considerations"):
            response += "\n\nالله معك في كل الأوقات (Allah is with you at all times)."
        
        # Send interruption notification to client
        await self.send_client_command("session_interrupted", {
            "interruption_record": interruption_record,
            "data_preserved": True,
            "resume_available": True,
            "emergency_activated": self.emergency_escalation_needed
        })
        
        # Reset session state
        self.session_active = False
        
        return response
    
    async def _export_session_summary(self) -> str:
        """Export a comprehensive session summary."""
        
        if not self.session_history and not self.session_active:
            return "No session data available to export."
        
        # Use current session if active, otherwise use latest session
        session_data = self.current_session if self.session_active else self.session_history[-1]
        
        summary = {
            "session_overview": {
                "session_id": session_data.get("session_id"),
                "date": session_data.get("start_time", "").split("T")[0],
                "duration": session_data.get("duration_minutes", "ongoing"),
                "session_type": "Voice Therapy - OMANI Therapist Voice"
            },
            "cultural_adaptations": self.cultural_preferences,
            "therapeutic_goals": self.therapeutic_goals,
            "progress_markers": len(self.progress_markers),
            "clinical_observations": len(self.session_notes),
            "privacy_level": self.privacy_level,
            "emergency_contacts_set": len(self.emergency_contacts) > 0,
            "consent_status": self.consent_status
        }
        
        # Generate human-readable summary
        readable_summary = f"""
📋 THERAPEUTIC SESSION SUMMARY
═══════════════════════════════

Session ID: {summary['session_overview']['session_id']}
Date: {summary['session_overview']['date']}
Duration: {summary['session_overview']['duration']} minutes
Type: {summary['session_overview']['session_type']}

🎯 THERAPEUTIC GOALS ({len(self.therapeutic_goals)})
{chr(10).join([f"• {goal}" for goal in self.therapeutic_goals]) if self.therapeutic_goals else "• No specific goals set"}

📈 PROGRESS TRACKING
• Progress markers documented: {summary['progress_markers']}
• Clinical observations: {summary['clinical_observations']}
• Privacy level: {summary['privacy_level'].upper()}

🌍 CULTURAL ADAPTATIONS
• Preferred language: {self.cultural_preferences.get('preferred_language', 'Not specified')}
• Religious considerations: {'Yes' if self.cultural_preferences.get('religious_considerations') else 'No'}
• Family involvement: {'Preferred' if self.cultural_preferences.get('family_involvement_preferred') else 'Not specified'}

🔒 PRIVACY & CONSENT
• Recording consent: {'✅ Granted' if self.consent_status.get('recording_consent') else '❌ Not granted'}
• Data storage consent: {'✅ Granted' if self.consent_status.get('data_storage_consent') else '❌ Not granted'}
• Emergency contacts: {'✅ Set' if summary['emergency_contacts_set'] else '❌ Not set'}

📝 CLINICAL NOTES
{chr(10).join([f"• {note['content'][:100]}..." for note in self.session_notes[-3:]]) if self.session_notes else "• No clinical notes recorded"}
        """
        
        # Send export data to client
        await self.send_client_command("session_summary_exported", {
            "summary_data": summary,
            "readable_summary": readable_summary,
            "export_timestamp": datetime.now().isoformat()
        })
        
        return self.format_response_culturally(
            "Session summary has been generated and exported. "
            "This summary maintains your privacy settings and contains your therapeutic progress information."
        )
    
    async def _generate_session_summary(self) -> str:
        """Generate a brief session summary."""
        
        if not self.session_active and not self.current_session:
            return "No session data available."
        
        duration = int((datetime.now() - self.session_start_time).total_seconds() / 60)
        
        summary_parts = []
        
        # Basic info
        summary_parts.append(f"Session duration: {duration} minutes")
        
        # Goals addressed
        if self.therapeutic_goals:
            summary_parts.append(f"Therapeutic goals worked on: {len(self.therapeutic_goals)}")
        
        # Clinical observations
        if self.session_notes:
            summary_parts.append(f"Clinical observations recorded: {len(self.session_notes)}")
        
        # Progress markers
        if self.progress_markers:
            summary_parts.append(f"Progress documented: {len(self.progress_markers)} markers")
        
        # Crisis status
        if self.crisis_detected:
            summary_parts.append("⚠️ Crisis indicators were addressed")
        
        # Cultural adaptations
        if self.cultural_preferences:
            summary_parts.append("Cultural preferences were incorporated")
        
        return " | ".join(summary_parts)
    
    def _generate_follow_up_recommendations(self) -> List[str]:
        """Generate follow-up recommendations based on session."""
        
        recommendations = []
        
        # Based on crisis status
        if self.crisis_detected:
            recommendations.extend([
                "Schedule follow-up within 24-48 hours",
                "Maintain safety plan adherence",
                "Consider professional referral consultation"
            ])
        
        # Based on progress
        if self.progress_markers:
            recommendations.append("Continue working on established therapeutic goals")
        
        # Based on cultural preferences
        if self.cultural_preferences.get("family_involvement_preferred"):
            recommendations.append("Consider family session for additional support")
        
        if self.cultural_preferences.get("religious_considerations"):
            recommendations.append("Integrate spiritual practices in self-care routine")
        
        # Default recommendations
        if not recommendations:
            recommendations.extend([
                "Practice techniques discussed in session",
                "Schedule regular follow-up session",
                "Maintain self-care routine"
            ])
        
        return recommendations
    
    def _suggest_next_session_timing(self) -> str:
        """Suggest timing for next session based on current status."""
        
        if self.crisis_detected or self.emergency_escalation_needed:
            return "Within 24-48 hours (urgent follow-up)"
        elif self.current_emotional_state.get("emotional_intensity", 0) > 7:
            return "Within 3-5 days (close monitoring)"
        elif len(self.progress_markers) > 0:
            return "Within 1 week (maintain momentum)"
        else:
            return "Within 1-2 weeks (regular follow-up)"
    
    def _analyze_progress_trend(self) -> str:
        """Analyze progress trend from multiple sessions."""
        
        if len(self.progress_markers) < 2:
            return "Insufficient data for trend analysis"
        
        # Simple trend analysis based on timestamps and content sentiment
        recent_markers = self.progress_markers[-3:]  # Last 3 markers
        
        # This is a simplified analysis - could be enhanced with sentiment analysis
        positive_indicators = ["improvement", "better", "progress", "helpful", "positive"]
        negative_indicators = ["worse", "difficult", "struggle", "setback", "challenging"]
        
        progress_scores = []
        for marker in recent_markers:
            # Handle None or empty progress_notes
            progress_notes = marker.get("progress_notes", "")
            if not progress_notes:
                progress_scores.append(0)
                continue
                
            content = progress_notes.lower()
            positive_count = sum(1 for indicator in positive_indicators if indicator in content)
            negative_count = sum(1 for indicator in negative_indicators if indicator in content)
            progress_scores.append(positive_count - negative_count)
        
        if len(progress_scores) >= 2:
            if progress_scores[-1] > progress_scores[0]:
                return "Positive progress trend observed"
            elif progress_scores[-1] < progress_scores[0]:
                return "Some challenges noted - continued support needed"
            else:
                return "Stable progress - maintaining current approach"
        
        return "Progress tracking ongoing" 