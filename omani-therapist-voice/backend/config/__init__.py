"""
Configuration Package for OMANI Therapist Voice.
Contains therapy agent management and system configuration.
"""

from .therapy_agent_manager import (
    TherapyAgentManager,
    GENERAL_THERAPY_INSTRUCTION,
    CRISIS_INTERVENTION_INSTRUCTION,
    CBT_SPECIALIST_INSTRUCTION
)

__all__ = [
    'TherapyAgentManager',
    'GENERAL_THERAPY_INSTRUCTION',
    'CRISIS_INTERVENTION_INSTRUCTION',
    'CBT_SPECIALIST_INSTRUCTION'
] 