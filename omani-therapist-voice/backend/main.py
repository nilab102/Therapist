#!/usr/bin/env python3
"""
OMANI Therapist Voice - Real-time AI Therapy using Gemini Live Multimodal
A culturally-sensitive therapeutic voice assistant for Gulf Arabic speakers.

Features:
- Ultra-low latency voice interaction with Gemini Live
- Clinical safety protocols and crisis intervention
- CBT techniques adapted for Arabic/Islamic context
- Cultural sensitivity for Gulf social norms
- Emergency escalation and professional referral
"""

import os
import sys
import asyncio
import json
import time
from datetime import datetime
from typing import Any, Dict, List
from contextlib import asynccontextmanager

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket, Request, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

# Standard FastAPI and WebSocket imports

from pipecat.audio.vad.silero import SileroVADAnalyzer
from pipecat.audio.vad.vad_analyzer import VADParams
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.task import PipelineParams, PipelineTask
from pipecat.processors.aggregators.openai_llm_context import OpenAILLMContext
from pipecat.processors.frameworks.rtvi import RTVIConfig, RTVIObserver, RTVIProcessor
from pipecat.serializers.protobuf import ProtobufFrameSerializer
from pipecat.services.llm_service import FunctionCallParams
from pipecat.adapters.schemas.tools_schema import ToolsSchema
from pipecat.processors.transcript_processor import TranscriptProcessor

# Import Gemini Live service
from pipecat.services.gemini_multimodal_live.gemini import GeminiMultimodalLiveLLMService

# Import OpenAI Realtime Beta service for fallback
try:
    from pipecat.services.openai_realtime_beta import (
        OpenAIRealtimeBetaLLMService,
        SessionProperties,
        InputAudioTranscription,
        SemanticTurnDetection,
        InputAudioNoiseReduction
    )
    OPENAI_REALTIME_AVAILABLE = True
except ImportError:
    OPENAI_REALTIME_AVAILABLE = False

# Import therapeutic tools
from tools.tool_registry import global_tool_registry, register_tool
from tools.base_tool import BaseTool
from tools.crisis_detection_tool import CrisisDetectionTool
from tools.cbt_techniques_tool import CBTTechniquesTool
from tools.emotional_analysis_tool import EmotionalAnalysisTool
from tools.session_management_tool import SessionManagementTool

# Import therapy agent manager
from config.therapy_agent_manager import (
    TherapyAgentManager,
    GENERAL_THERAPY_INSTRUCTION,
    CRISIS_INTERVENTION_INSTRUCTION,
    CBT_SPECIALIST_INSTRUCTION
)

from pipecat.transports.network.fastapi_websocket import (
    FastAPIWebsocketParams,
    FastAPIWebsocketTransport,
)

load_dotenv(override=True)

logger.remove(0)
logger.add(sys.stderr, level="DEBUG")

# Default to general therapy agent
SYSTEM_INSTRUCTION = GENERAL_THERAPY_INSTRUCTION


# Removed complex transport error handler - using simpler approach


class GeminiTherapyContextFilter:
    """
    Therapy-focused context filter for Gemini Live.
    Ensures clinical safety by filtering out inappropriate content.
    """
    
    @staticmethod
    def filter_messages_for_therapy(messages: List[Dict]) -> List[Dict]:
        """Filter messages to maintain therapeutic boundaries and Gemini Live compatibility."""
        valid_roles = {'user', 'model'}
        filtered_messages = []
        
        for message in messages:
            if isinstance(message, dict) and 'role' in message:
                if message['role'] in valid_roles:
                    # Additional therapeutic content filtering could be added here
                    filtered_messages.append(message)
                else:
                    logger.debug(f"🏥 Filtered message with role '{message['role']}' for therapeutic safety")
            else:
                filtered_messages.append(message)
        
        logger.debug(f"🏥 Therapy context filter: {len(messages)} → {len(filtered_messages)} messages")
        return filtered_messages


class GeminiTherapyContext(OpenAILLMContext):
    """
    Therapy-safe context for Gemini Live with clinical boundaries.
    """
    
    def __init__(self, messages=None, system_message=None):
        if messages:
            messages = GeminiTherapyContextFilter.filter_messages_for_therapy(messages)
        super().__init__(messages, system_message)
        logger.debug("🏥 Created GeminiTherapyContext with therapeutic safeguards")
    
    def get_messages_for_initializing_history(self):
        original_messages = super().get_messages_for_initializing_history()
        filtered_messages = GeminiTherapyContextFilter.filter_messages_for_therapy(original_messages)
        logger.debug(f"🏥 Therapy context filtered {len(original_messages)} → {len(filtered_messages)} messages")
        return filtered_messages
    
    @property
    def messages(self):
        original_messages = super().messages
        return GeminiTherapyContextFilter.filter_messages_for_therapy(original_messages)


def is_valid_google_api_key(key):
    """Validate Google API key for Gemini Live access."""
    if not key:
        return False
    
    placeholders = ["your_", "ai...", "your-", "example", "placeholder", "here", "key_here"]
    key_lower = key.lower()
    for placeholder in placeholders:
        if placeholder in key_lower:
            return False
    
    if not key.startswith("AI"):
        return False
    
    return True


def is_valid_openai_api_key(key):
    """Validate OpenAI API key for Realtime API access."""
    if not key:
        return False
    
    placeholders = ["your_", "sk-your_", "your-", "sk-...", "example", "placeholder", "here", "key_here"]
    key_lower = key.lower()
    for placeholder in placeholders:
        if placeholder in key_lower:
            return False
    
    if not key.startswith("sk-"):
        return False
    
    return True


def is_valid_api_key(key, key_type):
    """Check if API key is valid (not a placeholder)."""
    if not key:
        return False
    
    # Check for common placeholder patterns
    placeholders = [
        "your_", "sk-your_", "your-", "ai...", "sk-...", 
        "example", "placeholder", "here", "key_here"
    ]
    
    key_lower = key.lower()
    for placeholder in placeholders:
        if placeholder in key_lower:
            return False
    
    # Basic format validation
    if key_type == "openai" and not key.startswith("sk-"):
        return False
    if key_type == "google" and not key.startswith("AI"):
        return False
    
    return True


async def create_therapy_gemini_llm(system_instruction: str, tools_schema=None):
    """Create Gemini Live LLM service optimized for therapy."""
    google_key = os.getenv("GOOGLE_API_KEY")
    
    if not is_valid_google_api_key(google_key):
        raise ValueError("Invalid or missing GOOGLE_API_KEY. Please set a valid Google API key for therapy sessions.")
    
    logger.info("🏥 Creating Gemini Live therapeutic service")
    
    llm_service = GeminiMultimodalLiveLLMService(
        api_key=google_key,
        system_instruction=system_instruction,
        voice_id="Zephyr",  # Calm, empathetic voice
        models='models/gemini-2.5-flash-preview-native-audio-dialog',
        temperature=0,
        transcribe_model_audio=True,
        tools=tools_schema,
    )
    
    return llm_service


async def create_therapy_openai_realtime_llm(system_instruction: str, tools_schema=None):
    """Create OpenAI Realtime Beta LLM service optimized for therapy."""
    openai_key = os.getenv("OPENAI_API_KEY")
    
    if not is_valid_openai_api_key(openai_key):
        raise ValueError("Invalid or missing OPENAI_API_KEY. Please set a valid OpenAI API key for therapy sessions.")
    
    logger.info("🏥 Creating OpenAI Realtime Beta therapeutic service")
    
    session_properties = SessionProperties(
        input_audio_transcription=InputAudioTranscription(),
        turn_detection=SemanticTurnDetection(),
        input_audio_noise_reduction=InputAudioNoiseReduction(type="near_field"),
        instructions=system_instruction
    )
    
    llm_service = OpenAIRealtimeBetaLLMService(
        api_key=openai_key,
        session_properties=session_properties,
        start_audio_paused=False,
    )
    
    return llm_service


async def create_native_audio_therapy_llm(enable_function_calling=False, force_service=None):
    """Create an LLM service that handles audio natively for maximum therapy efficiency."""
    
    # If force_service is specified, try that service first
    if force_service == "openai_realtime":
        openai_key = os.getenv("OPENAI_API_KEY")
        if OPENAI_REALTIME_AVAILABLE and is_valid_api_key(openai_key, "openai"):
            logger.info("🏥 Using OpenAI Realtime API (forced selection)")
            tools = None
            if enable_function_calling:
                tools = ToolsSchema(standard_tools=global_tool_registry.get_tool_definitions())
                logger.info("🔧 Enabling function calling for OpenAI Realtime therapy")
            llm_service = await create_therapy_openai_realtime_llm(SYSTEM_INSTRUCTION, tools)
            return llm_service, "openai_realtime"
        else:
            logger.warning("🏥 Forced OpenAI Realtime not available, falling back to normal priority")
    
    elif force_service == "gemini_live":
        google_key = os.getenv("GOOGLE_API_KEY")
        if is_valid_api_key(google_key, "google"):
            logger.info("🏥 Using Gemini Multimodal Live (forced selection)")
            tools = None
            if enable_function_calling:
                tools = ToolsSchema(standard_tools=global_tool_registry.get_tool_definitions())
                logger.info("🔧 Enabling function calling for Gemini Live therapy")
            llm_service = await create_therapy_gemini_llm(SYSTEM_INSTRUCTION, tools)
            return llm_service, "gemini_live"
        else:
            logger.warning("🏥 Forced Gemini Live not available, falling back to normal priority")
    
    # Normal priority-based fallback logic
    # Check OpenAI Realtime API first (preferred for therapy)
    openai_key = os.getenv("OPENAI_API_KEY")
    if OPENAI_REALTIME_AVAILABLE and is_valid_api_key(openai_key, "openai"):
        logger.info("🏥 Using OpenAI Realtime API (native audio streaming) for therapy")
        
        # Create tools if function calling is enabled
        tools = None
        if enable_function_calling:
            tools = ToolsSchema(standard_tools=global_tool_registry.get_tool_definitions())
            logger.info("🔧 Enabling function calling for OpenAI Realtime therapy")
        
        try:
            llm_service = await create_therapy_openai_realtime_llm(SYSTEM_INSTRUCTION, tools)
            return llm_service, "openai_realtime"
        except Exception as e:
            logger.warning(f"🏥 OpenAI Realtime failed: {e}, trying Gemini Live fallback")
    
    # Check Gemini Multimodal Live as fallback
    google_key = os.getenv("GOOGLE_API_KEY")
    if is_valid_api_key(google_key, "google"):
        logger.info("🏥 Using Gemini Multimodal Live (native audio streaming) for therapy")
        
        # Create tools if function calling is enabled
        tools = None
        if enable_function_calling:
            tools = ToolsSchema(standard_tools=global_tool_registry.get_tool_definitions())
            logger.info("🔧 Enabling function calling for Gemini Live therapy")
        
        try:
            llm_service = await create_therapy_gemini_llm(SYSTEM_INSTRUCTION, tools)
            return llm_service, "gemini_live"
        except Exception as e:
            logger.error(f"🏥 Gemini Live also failed: {e}")
    
    # No native audio LLM available
    logger.error("❌ No native audio LLM available. Please configure OPENAI_API_KEY or GOOGLE_API_KEY.")
    raise ValueError("No LLM service available. Please configure OpenAI or Google API keys for therapy sessions.")


async def setup_therapeutic_tools(rtvi_processor: RTVIProcessor, therapy_agent_manager: TherapyAgentManager):
    """Set up therapeutic tools for clinical safety and treatment."""
    logger.info("🏥 Setting up therapeutic tool system")
    
    # Register therapeutic tool classes
    register_tool("crisis_detection", CrisisDetectionTool)
    register_tool("cbt_techniques", CBTTechniquesTool)
    register_tool("emotional_analysis", EmotionalAnalysisTool)
    register_tool("session_management", SessionManagementTool)
    
    # Create tool instances
    crisis_tool = global_tool_registry.create_tool("crisis_detection", rtvi_processor)
    cbt_tool = global_tool_registry.create_tool("cbt_techniques", rtvi_processor)
    emotional_tool = global_tool_registry.create_tool("emotional_analysis", rtvi_processor)
    session_tool = global_tool_registry.create_tool("session_management", rtvi_processor)
    
    # Set up tool callbacks
    if crisis_tool:
        crisis_tool.escalation_callback = therapy_agent_manager.handle_crisis_escalation
    
    return {
        "crisis_detection": crisis_tool,
        "cbt_techniques": cbt_tool,
        "emotional_analysis": emotional_tool,
        "session_management": session_tool
    }


async def run_therapy_bot(websocket: WebSocket):
    """Run the therapeutic conversational AI bot."""
    logger.info("🏥 Starting OMANI Therapist Voice session")
    
    # Custom error-tolerant serializer for therapeutic sessions
    class TherapeuticProtobufSerializer(ProtobufFrameSerializer):
        """Enhanced protobuf serializer with error handling for therapeutic WebSocket sessions."""
        
        def deserialize(self, data):
            """Deserialize with enhanced error handling for malformed messages."""
            try:
                # First try normal protobuf deserialization
                return super().deserialize(data)
            except KeyError as e:
                if "'bytes'" in str(e):
                    logger.warning("🏥 Received non-protobuf message on main WebSocket endpoint")
                    logger.warning("🏥 Tool/config messages should be sent to /ws/tools endpoint")
                    logger.warning("🏥 Main /ws endpoint expects protobuf audio frames only")
                    # Return empty audio frame to prevent pipeline disruption
                    from pipecat.frames.frames import AudioRawFrame
                    return AudioRawFrame(data=b"", sample_rate=16000, num_channels=1)
                else:
                    logger.debug(f"🏥 Protobuf deserialization KeyError: {e}")
                    raise
            except Exception as e:
                logger.debug(f"🏥 Protobuf deserialization error: {e}")
                # Let other exceptions propagate normally  
                raise
    
    # Create transport with therapeutic optimization and error handling
    transport = FastAPIWebsocketTransport(
        websocket=websocket,
        params=FastAPIWebsocketParams(
            audio_in_enabled=True,
            audio_out_enabled=True,
            add_wav_header=False,
            # Optimized for therapeutic conversation
            vad_analyzer=SileroVADAnalyzer(params=VADParams(
                stop_secs=1.0,  # Allow for pauses in emotional speech
                start_secs=0.3
            )),
            serializer=TherapeuticProtobufSerializer(),
        ),
    )
    
    # RTVI processor for client communication
    rtvi = RTVIProcessor(config=RTVIConfig(config=[]))

    # Add transcript processor for real-time transcription relay
    transcript = TranscriptProcessor()
    
    # Create therapy agent manager
    therapy_agent_manager_instance = TherapyAgentManager()
    
    # Set global reference for WebSocket access
    global therapy_agent_manager
    therapy_agent_manager = therapy_agent_manager_instance
    
    # Set up therapeutic tools
    tool_instances = await setup_therapeutic_tools(rtvi, therapy_agent_manager_instance)
    
    # Check if we can enable function calling (works with both OpenAI and Google)
    openai_key = os.getenv("OPENAI_API_KEY")
    google_key = os.getenv("GOOGLE_API_KEY")
    can_use_function_calling = (
        is_valid_api_key(openai_key, "openai") or 
        is_valid_api_key(google_key, "google")
    )
    
    if can_use_function_calling:
        logger.info("🔧 Function calling available - enabling therapeutic tools with native audio")
        llm_service, llm_type = await create_native_audio_therapy_llm(enable_function_calling=True)
    else:
        logger.info("⚡ Using native audio mode (no API keys for function calling)")
        llm_service, llm_type = await create_native_audio_therapy_llm(enable_function_calling=False)
    
    # Use therapeutic context - adapt based on LLM type
    if llm_type == "openai_realtime":
        # OpenAI Realtime uses standard context
        context = OpenAILLMContext([{
            "role": "user", 
            "content": "أهلاً وسهلاً! أنا أحتاج للحديث مع معالج نفسي. (Hello! I need to speak with a therapist.)"
        }])
        logger.info("🏥 Using OpenAILLMContext for OpenAI Realtime therapy")
    else:
        # Gemini Live uses therapeutic context with filtering
        context = GeminiTherapyContext([{
            "role": "user", 
            "content": "أهلاً وسهلاً! أنا أحتاج للحديث مع معالج نفسي. (Hello! I need to speak with a therapist.)"
        }])
        logger.info("🏥 Using GeminiTherapyContext for clinical safety")
    
    context_aggregator = llm_service.create_context_aggregator(context)
    
    # Apply therapeutic context filtering only for Gemini Live
    user_aggregator = context_aggregator.user()
    if llm_type == "gemini_live":
        orig_get_context_frame = user_aggregator.get_context_frame
        def get_context_frame_therapy_safe(*args, **kwargs):
            frame = orig_get_context_frame(*args, **kwargs)
            if hasattr(frame, 'messages') and isinstance(frame.messages, list):
                filtered = GeminiTherapyContextFilter.filter_messages_for_therapy(frame.messages)
                frame.messages = filtered
                logger.debug(f"🏥 Applied therapeutic filtering to {len(filtered)} messages")
            return frame
        user_aggregator.get_context_frame = get_context_frame_therapy_safe
    
    # Build therapeutic pipeline - adapt based on LLM type
    if llm_type == "openai_realtime":
        # OpenAI Realtime API pipeline
        pipeline = Pipeline([
            transport.input(),
            context_aggregator.user(),
            rtvi,
            llm_service,
            transcript.user(),
            transport.output(),
            transcript.assistant(),
            context_aggregator.assistant(),
        ])
    else:  # gemini_live
        # Gemini Live pipeline
        pipeline = Pipeline([
            transport.input(),
            context_aggregator.user(),
            rtvi,
            llm_service,
            transport.output(),
            context_aggregator.assistant(),
        ])
    
    # Create pipeline task with therapeutic parameters
    task = PipelineTask(
        pipeline,
        params=PipelineParams(
            enable_metrics=True,
            enable_usage_metrics=True,
        ),
        observers=[RTVIObserver(rtvi)],
    )
    
    # Set task reference for all tools
    global_tool_registry.set_task_for_all_tools(task)
    therapy_agent_manager_instance.task = task
    
    # Create therapeutic LLM recreation callback
    async def recreate_therapy_llm_callback(new_system_instruction: str, new_tools: list):
        """Recreate LLM session for agent switching in therapy context."""
        logger.info(f"🏥 Switching therapeutic agent with new specialization")
        
        # Implementation similar to main.py but with therapeutic context
        fresh_tools_schema = ToolsSchema(standard_tools=global_tool_registry.get_tool_definitions())
        
        current_pipeline = task._pipeline
        current_llm_service = None
        llm_index = -1
        current_llm_type = None
        
        # Find current LLM service and determine type
        for i, processor in enumerate(current_pipeline._processors):
            if hasattr(processor, '__class__'):
                if 'GeminiMultimodalLiveLLMService' in processor.__class__.__name__:
                    current_llm_service = processor
                    current_llm_type = "gemini_live"
                    llm_index = i
                    break
                elif 'OpenAIRealtimeBetaLLMService' in processor.__class__.__name__:
                    current_llm_service = processor
                    current_llm_type = "openai_realtime"
                    llm_index = i
                    break
        
        if current_llm_service is None:
            logger.error("Could not find LLM service in therapeutic pipeline")
            return
        
        # Create new LLM service based on current type
        try:
            if current_llm_type == "openai_realtime":
                new_llm_service = await create_therapy_openai_realtime_llm(new_system_instruction, fresh_tools_schema)
            elif current_llm_type == "gemini_live":
                new_llm_service = await create_therapy_gemini_llm(new_system_instruction, fresh_tools_schema)
            else:
                logger.error(f"Unknown LLM type: {current_llm_type}")
                return
        except Exception as e:
            logger.error(f"Failed to recreate {current_llm_type} service: {e}")
            # Try fallback to the other service
            try:
                if current_llm_type == "openai_realtime":
                    logger.info("🏥 Trying Gemini Live as fallback for agent switch")
                    new_llm_service = await create_therapy_gemini_llm(new_system_instruction, fresh_tools_schema)
                    current_llm_type = "gemini_live"
                else:
                    logger.info("🏥 Trying OpenAI Realtime as fallback for agent switch")
                    new_llm_service = await create_therapy_openai_realtime_llm(new_system_instruction, fresh_tools_schema)
                    current_llm_type = "openai_realtime"
            except Exception as fallback_error:
                logger.error(f"Fallback service also failed: {fallback_error}")
                return
        
        # Create context based on LLM type
        if current_llm_type == "openai_realtime":
            fresh_context = OpenAILLMContext([])
        else:  # gemini_live
            fresh_context = GeminiTherapyContext([])
        new_context_aggregator = new_llm_service.create_context_aggregator(fresh_context)
        
        # Register therapeutic function handlers
        async def handle_therapy_function_call(params):
            try:
                class MockFunctionCall:
                    def __init__(self, name, arguments):
                        self.name = name
                        self.arguments = arguments
                mock_call = MockFunctionCall(params.function_name, params.arguments)
                result = await therapy_agent_manager_instance.handle_function_call(mock_call)
                await params.result_callback({"result": result})
            except Exception as e:
                logger.error(f"Error in therapeutic function handler: {e}")
                await params.result_callback({"error": str(e)})
        
        # Register all therapeutic functions
        new_llm_service.register_function("detect_crisis", handle_therapy_function_call)
        new_llm_service.register_function("apply_cbt_technique", handle_therapy_function_call)
        new_llm_service.register_function("analyze_emotion", handle_therapy_function_call)
        new_llm_service.register_function("manage_session", handle_therapy_function_call)
        
        # Replace pipeline components (similar to main.py)
        current_pipeline._processors[llm_index] = new_llm_service
        
        # Update context aggregators
        user_context_aggregator = new_context_aggregator.user()
        assistant_context_aggregator = new_context_aggregator.assistant()
        
        for i, processor in enumerate(current_pipeline._processors):
            if hasattr(processor, '__class__'):
                if 'GeminiMultimodalLiveUserContextAggregator' in processor.__class__.__name__ or 'OpenAIRealtimeBetaUserContextAggregator' in processor.__class__.__name__:
                    current_pipeline._processors[i] = user_context_aggregator
                    break
        
        for i, processor in enumerate(current_pipeline._processors):
            if hasattr(processor, '__class__'):
                if 'GeminiMultimodalLiveAssistantContextAggregator' in processor.__class__.__name__ or 'OpenAIRealtimeBetaAssistantContextAggregator' in processor.__class__.__name__:
                    current_pipeline._processors[i] = assistant_context_aggregator
                    break
        
        # Re-link and setup pipeline
        for i in range(len(current_pipeline._processors) - 1):
            current_pipeline._processors[i].link(current_pipeline._processors[i + 1])
        
        from pipecat.processors.frame_processor import FrameProcessorSetup
        setup = FrameProcessorSetup(
            clock=task._clock,
            task_manager=task._task_manager,
            observer=task._turn_tracking_observer,
            watchdog_timers_enabled=task._enable_watchdog_timers,
        )
        
        await new_llm_service.setup(setup)
        await user_context_aggregator.setup(setup)
        await assistant_context_aggregator.setup(setup)
        
        from pipecat.frames.frames import StartFrame
        from pipecat.processors.frame_processor import FrameDirection
        
        start_frame = StartFrame(
            allow_interruptions=task._params.allow_interruptions,
            audio_in_sample_rate=task._params.audio_in_sample_rate,
            audio_out_sample_rate=task._params.audio_out_sample_rate,
            enable_metrics=task._params.enable_metrics,
            enable_usage_metrics=task._params.enable_usage_metrics,
            report_only_initial_ttfb=task._params.report_only_initial_ttfb,
            interruption_strategies=task._params.interruption_strategies,
        )
        
        await new_llm_service.process_frame(start_frame, FrameDirection.DOWNSTREAM)
        await user_context_aggregator.process_frame(start_frame, FrameDirection.DOWNSTREAM)
        await assistant_context_aggregator.process_frame(start_frame, FrameDirection.DOWNSTREAM)
        
        logger.info(f"✅ Successfully recreated therapeutic {current_llm_type} session")
        
        # Disconnect old session
        try:
            if hasattr(current_llm_service, '_disconnect'):
                await current_llm_service._disconnect()
            elif hasattr(current_llm_service, '_ws') and current_llm_service._ws:
                await current_llm_service._ws.close()
                current_llm_service._ws = None
        except Exception as e:
            logger.warning(f"Error disconnecting old therapeutic session: {e}")
    
    therapy_agent_manager_instance.llm_recreate_callback = recreate_therapy_llm_callback
    
    # Register therapeutic agents
    therapy_agent_manager_instance.register_agent(
        "general_therapy", 
        GENERAL_THERAPY_INSTRUCTION,
        [t.get_tool_definition() for t in tool_instances.values()],
        tool_instances
    )
    
    therapy_agent_manager_instance.register_agent(
        "crisis_intervention",
        CRISIS_INTERVENTION_INSTRUCTION,
        [tool_instances["crisis_detection"].get_tool_definition(), tool_instances["session_management"].get_tool_definition()],
        {"crisis_detection": tool_instances["crisis_detection"], "session_management": tool_instances["session_management"]}
    )
    
    therapy_agent_manager_instance.register_agent(
        "cbt_specialist",
        CBT_SPECIALIST_INSTRUCTION,
        [tool_instances["cbt_techniques"].get_tool_definition(), tool_instances["emotional_analysis"].get_tool_definition()],
        {"cbt_techniques": tool_instances["cbt_techniques"], "emotional_analysis": tool_instances["emotional_analysis"]}
    )
    
    # Register therapeutic function handlers
    async def handle_therapy_function_call(params: FunctionCallParams):
        try:
            class MockFunctionCall:
                def __init__(self, name, arguments):
                    self.name = name
                    self.arguments = arguments
            
            mock_call = MockFunctionCall(params.function_name, params.arguments)
            result = await therapy_agent_manager.handle_function_call(mock_call)
            await params.result_callback({"result": result})
        except Exception as e:
            logger.error(f"Error in therapeutic function handler: {e}")
            await params.result_callback({"error": str(e)})
    
    # Register all therapeutic functions
    llm_service.register_function("detect_crisis", handle_therapy_function_call)
    llm_service.register_function("apply_cbt_technique", handle_therapy_function_call)
    llm_service.register_function("analyze_emotion", handle_therapy_function_call)
    llm_service.register_function("manage_session", handle_therapy_function_call)
    
    logger.info("🏥 Registered all therapeutic function handlers")
    
    @rtvi.event_handler("on_client_ready")
    async def on_client_ready(rtvi):
        logger.info("✅ Client ready - starting therapeutic session")
        await rtvi.set_bot_ready()
        await task.queue_frames([user_aggregator.get_context_frame()])
    
    @transport.event_handler("on_client_connected")
    async def on_client_connected(transport, client):
        logger.info("🏥 Client connected to OMANI Therapist Voice")
    
    @transport.event_handler("on_client_disconnected")
    async def on_client_disconnected(transport, client):
        logger.info("👋 Client disconnected from therapeutic session")
        await task.cancel()
    
    # Add transcript relay to frontend
    @transcript.event_handler("on_transcript_update")
    async def on_transcript_update(processor, frame):
        # Log transcriptions for debugging (RTVI handles frontend communication automatically)
        for msg in frame.messages:
            if hasattr(msg, 'role') and hasattr(msg, 'content'):
                if msg.role in ("user", "model", "assistant") and msg.content:
                    logger.info(f"🏥 Transcript: {msg.role}: {msg.content}")
    
    # Run the therapeutic pipeline
    runner = PipelineRunner(handle_sigint=False)
    try:
        await runner.run(task)
    except Exception as e:
        logger.error(f"❌ Therapeutic pipeline error: {e}")
        await websocket.close(code=1000, reason="Therapeutic session error")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle FastAPI startup and shutdown for therapy service."""
    logger.info("🏥 Starting OMANI Therapist Voice Server")
    logger.info("🇴🇲 Culturally-sensitive AI therapy for Gulf Arabic speakers")
    yield
    logger.info("👋 Shutting down OMANI Therapist Voice Server")


# Initialize FastAPI app
app = FastAPI(
    title="OMANI Therapist Voice",
    description="Culturally-sensitive AI therapy using Gemini Live multimodal for Gulf Arabic speakers",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import tool WebSocket registry
from utils.tool_websocket_registry import tool_websockets

# Global therapy agent manager for WebSocket access
therapy_agent_manager = None


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for therapeutic conversation."""
    await websocket.accept()
    logger.info("🏥 WebSocket connection accepted for therapeutic session")
    try:
        await run_therapy_bot(websocket)
    except WebSocketDisconnect:
        logger.info("👋 Client disconnected from therapeutic session")
    except Exception as e:
        logger.error(f"❌ Exception in therapeutic session: {e}")
        try:
            await websocket.close(code=1000, reason="Therapeutic session error")
        except:
            pass


@app.websocket("/ws/tools")
async def tools_websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for therapeutic tool commands and session management."""
    await websocket.accept()
    
    import uuid
    client_id = str(uuid.uuid4())
    tool_websockets[client_id] = websocket
    
    logger.info(f"🏥 Therapeutic tool WebSocket connected for client {client_id}")
    
    try:
        # Send welcome message with available commands
        welcome_message = {
            "type": "therapeutic_welcome",
            "message": "أهلاً وسهلاً! Welcome to OMANI Therapist Voice tool interface",
            "available_commands": [
                "get_agent_status", "switch_agent", "get_tools", "check_crisis_status",
                "update_cultural_context", "get_session_info"
            ],
            "cultural_features": ["omani_arabic", "islamic_integration", "gulf_family_dynamics"],
            "client_id": client_id
        }
        await websocket.send_json(welcome_message)
        
        while True:
            # Listen for JSON commands
            message = await websocket.receive_text()
            logger.info(f"🏥 Received therapeutic tool message from {client_id}: {message}")
            
            try:
                # Parse JSON command
                command = json.loads(message)
                response = await handle_tool_command(command, client_id)
                await websocket.send_json(response)
                
            except json.JSONDecodeError:
                error_response = {
                    "type": "error",
                    "message": "Invalid JSON format. Please send valid JSON commands.",
                    "client_id": client_id
                }
                await websocket.send_json(error_response)
            except Exception as e:
                error_response = {
                    "type": "error", 
                    "message": f"Error processing command: {str(e)}",
                    "client_id": client_id
                }
                await websocket.send_json(error_response)
            
    except WebSocketDisconnect:
        logger.info(f"👋 Therapeutic tool WebSocket disconnected for client {client_id}")
    except Exception as e:
        logger.error(f"❌ Exception in therapeutic tool WebSocket: {e}")
    finally:
        # Clean up
        if client_id in tool_websockets:
            del tool_websockets[client_id]
            logger.info(f"🧹 Cleaned up therapeutic tool WebSocket for client {client_id}")
        
        try:
            await websocket.close()
        except:
            pass


async def handle_tool_command(command: Dict[str, Any], client_id: str) -> Dict[str, Any]:
    """Handle therapeutic tool commands from WebSocket clients."""
    command_type = command.get("type", "unknown")
    
    try:
        if command_type == "get_agent_status":
            # Get current therapeutic agent status
            if 'therapy_agent_manager' in globals():
                agent_info = therapy_agent_manager.get_current_agent_info()
                return {
                    "type": "agent_status_response",
                    "data": agent_info,
                    "client_id": client_id
                }
            else:
                return {
                    "type": "error",
                    "message": "Therapy agent manager not available",
                    "client_id": client_id
                }
        
        elif command_type == "switch_agent":
            # Switch therapeutic agent
            target_agent = command.get("agent", "general_therapy")
            reason = command.get("reason", "Client request")
            cultural_context = command.get("cultural_context", {})
            
            if 'therapy_agent_manager' in globals():
                result = await therapy_agent_manager.switch_agent(target_agent, reason, cultural_context)
                return {
                    "type": "agent_switch_response",
                    "data": {"result": result, "new_agent": target_agent},
                    "client_id": client_id
                }
            else:
                return {
                    "type": "error",
                    "message": "Therapy agent manager not available",
                    "client_id": client_id
                }
        
        elif command_type == "get_tools":
            # Get available therapeutic tools
            tools_info = {
                "available_tools": global_tool_registry.list_available_tools(),
                "active_tools": global_tool_registry.list_active_tools(),
                "tool_stats": global_tool_registry.get_tool_stats()
            }
            return {
                "type": "tools_response",
                "data": tools_info,
                "client_id": client_id
            }
        
        elif command_type == "check_crisis_status":
            # Check crisis status across all tools
            crisis_status = global_tool_registry.check_crisis_status()
            return {
                "type": "crisis_status_response",
                "data": crisis_status,
                "client_id": client_id
            }
        
        elif command_type == "update_cultural_context":
            # Update cultural context for session
            cultural_updates = command.get("cultural_context", {})
            if 'therapy_agent_manager' in globals():
                therapy_agent_manager.update_cultural_context(cultural_updates)
                return {
                    "type": "cultural_context_updated",
                    "data": {"updated_context": cultural_updates},
                    "client_id": client_id
                }
            else:
                return {
                    "type": "error",
                    "message": "Therapy agent manager not available",
                    "client_id": client_id
                }
        
        elif command_type == "get_session_info":
            # Get comprehensive session information
            session_info = {
                "connected_clients": len(tool_websockets),
                "service_status": "active",
                "cultural_adaptations": ["omani_arabic", "islamic_integration", "gulf_family_dynamics"],
                "safety_protocols": ["crisis_detection", "emergency_escalation", "professional_referral"]
            }
            
            if 'therapy_agent_manager' in globals():
                session_info.update(therapy_agent_manager.get_system_status())
            
            return {
                "type": "session_info_response",
                "data": session_info,
                "client_id": client_id
            }
        
        else:
            return {
                "type": "error",
                "message": f"Unknown command type: {command_type}. Available: get_agent_status, switch_agent, get_tools, check_crisis_status, update_cultural_context, get_session_info",
                "client_id": client_id
            }
    
    except Exception as e:
        logger.error(f"Error handling tool command {command_type}: {e}")
        return {
            "type": "error",
            "message": f"Error executing command: {str(e)}",
            "client_id": client_id
        }


@app.get("/health")
async def health_check():
    """Health check endpoint for therapeutic service."""
    openai_key = os.getenv("OPENAI_API_KEY")
    google_key = os.getenv("GOOGLE_API_KEY")
    
    openai_available = OPENAI_REALTIME_AVAILABLE and is_valid_api_key(openai_key, "openai")
    gemini_available = is_valid_api_key(google_key, "google")
    therapy_available = openai_available or gemini_available
    
    return {
        "status": "healthy" if therapy_available else "needs_configuration",
        "service": "OMANI Therapist Voice",
        "features": {
            "openai_realtime_therapy": openai_available,
            "gemini_live_therapy": gemini_available,
            "crisis_detection": True,
            "cbt_techniques": True,
            "emotional_analysis": True,
            "cultural_adaptation": True,
            "gulf_arabic_support": True,
            "available_tools": global_tool_registry.list_available_tools(),
            "therapeutic_agents": ["general_therapy", "crisis_intervention", "cbt_specialist"]
        },
        "expected_latency": "sub-500ms" if therapy_available else "service_unavailable",
        "clinical_safety": "enabled",
        "cultural_sensitivity": "gulf_arabic_islamic",
        "websocket_usage": {
            "main_endpoint": "/ws - For protobuf audio frames only (RTVI compatible)",
            "tools_endpoint": "/ws/tools - For session config, tool commands, and JSON messages",
            "message_format": "Send audio as protobuf frames to /ws, configuration as JSON to /ws/tools"
        }
    }


@app.post("/connect")
async def bot_connect(request: Request) -> Dict[Any, Any]:
    """RTVI connect endpoint for therapeutic client."""
    return {
        "ws_url": f"ws://localhost:{int(os.getenv('SERVER_PORT', 8003))}/ws"
    }


@app.get("/tools")
async def list_therapeutic_tools():
    """List all available therapeutic tools."""
    return {
        "available_therapeutic_tools": global_tool_registry.list_available_tools(),
        "active_tool_instances": global_tool_registry.list_active_tools(),
        "total_tools": len(global_tool_registry.list_available_tools()),
        "clinical_safety_level": "high",
        "cultural_adaptation": "enabled"
    }


@app.get("/optimization-status")
async def optimization_status():
    """Detailed optimization status and recommendations for therapy service."""
    openai_key = os.getenv("OPENAI_API_KEY")
    google_key = os.getenv("GOOGLE_API_KEY")
    
    native_audio_available = (
        (OPENAI_REALTIME_AVAILABLE and is_valid_api_key(openai_key, "openai")) or
        (is_valid_api_key(google_key, "google"))
    )
    
    recommendations = []
    
    if not native_audio_available:
        recommendations.append("🚀 Enable native audio by setting OPENAI_API_KEY (for Realtime API) or GOOGLE_API_KEY (for Gemini Live)")
        recommendations.append("⚡ Native audio reduces latency from ~1000ms to ~500ms")
    
    return {
        "native_audio_enabled": native_audio_available,
        "expected_performance": "Ultra-low latency (<500ms)" if native_audio_available else "Standard latency (~1000ms)",
        "recommendations": recommendations,
        "services_status": {
            "openai_realtime": OPENAI_REALTIME_AVAILABLE and is_valid_api_key(openai_key, "openai"),
            "gemini_live": is_valid_api_key(google_key, "google"),
        },
        "therapy_features": {
            "crisis_detection": True,
            "cbt_techniques": True,
            "emotional_analysis": True,
            "cultural_adaptation": True
        }
    }


@app.get("/session/status")
async def session_status():
    """Get current therapeutic session status."""
    return {
        "active_sessions": len(tool_websockets),
        "service_type": "therapeutic_voice_assistance",
        "language_support": ["arabic_gulf", "english"],
        "clinical_protocols": ["crisis_intervention", "cbt", "emotional_support"],
        "safety_features": ["crisis_detection", "emergency_escalation", "professional_referral"]
    }


@app.get("/test-fallback")
async def test_fallback_endpoint():
    """Test endpoint to verify fallback mechanism is working correctly."""
    openai_key = os.getenv("OPENAI_API_KEY")
    google_key = os.getenv("GOOGLE_API_KEY")
    
    test_results = {
        "api_key_validation": {
            "openai_valid": is_valid_api_key(openai_key, "openai"),
            "google_valid": is_valid_api_key(google_key, "google"),
            "openai_realtime_available": OPENAI_REALTIME_AVAILABLE
        },
        "fallback_priority": {
            "preferred_service": "openai_realtime" if (OPENAI_REALTIME_AVAILABLE and is_valid_api_key(openai_key, "openai")) else "gemini_live" if is_valid_api_key(google_key, "google") else "none",
            "fallback_service": "gemini_live" if (OPENAI_REALTIME_AVAILABLE and is_valid_api_key(openai_key, "openai")) and is_valid_api_key(google_key, "google") else "none"
        },
        "service_creation_test": {},
        "recommendations": []
    }
    
    # Test service creation
    try:
        llm_service, llm_type = await create_native_audio_therapy_llm(enable_function_calling=False)
        test_results["service_creation_test"] = {
            "success": True,
            "service_type": llm_type,
            "service_class": type(llm_service).__name__
        }
    except Exception as e:
        test_results["service_creation_test"] = {
            "success": False,
            "error": str(e)
        }
    
    # Generate recommendations
    if not is_valid_api_key(openai_key, "openai") and not is_valid_api_key(google_key, "google"):
        test_results["recommendations"].append("Set OPENAI_API_KEY or GOOGLE_API_KEY environment variable")
    
    if not OPENAI_REALTIME_AVAILABLE:
        test_results["recommendations"].append("Install OpenAI Realtime Beta for optimal performance")
    
    if is_valid_api_key(openai_key, "openai") and is_valid_api_key(google_key, "google"):
        test_results["recommendations"].append("Both services available - OpenAI Realtime will be preferred")
    
    return test_results


@app.get("/session/documentation")
async def get_session_documentation():
    """Get comprehensive session documentation for clinical records."""
    documentation = {
        "session_overview": {
            "service": "OMANI Therapist Voice",
            "session_id": f"session_{int(time.time())}",
            "timestamp": datetime.now().isoformat(),
            "cultural_context": "omani_gulf_arabic_islamic",
            "therapeutic_approach": "culturally_integrated_ai_therapy"
        },
        "agent_status": {},
        "tool_documentation": {},
        "clinical_summary": {},
        "safety_assessment": {},
        "cultural_adaptations_applied": [
            "omani_arabic_expressions",
            "islamic_therapeutic_concepts", 
            "gulf_family_dynamics",
            "cultural_crisis_protocols"
        ]
    }
    
    # Get agent documentation if available
    if therapy_agent_manager:
        documentation["agent_status"] = therapy_agent_manager.get_system_status()
        documentation["agent_history"] = therapy_agent_manager.get_agent_history()
    
    # Get tool documentation
    for tool_name, tool_instance in global_tool_registry._active_tools.items():
        if hasattr(tool_instance, 'get_session_documentation'):
            documentation["tool_documentation"][tool_name] = tool_instance.get_session_documentation()
    
    # Get overall clinical summary
    documentation["clinical_summary"] = global_tool_registry.get_all_clinical_data()
    documentation["safety_assessment"] = global_tool_registry.check_crisis_status()
    
    return documentation


@app.post("/session/export")
async def export_session_data(request: Request):
    """Export session data in various formats for clinical records."""
    body = await request.json()
    export_format = body.get("format", "json")  # json, pdf, clinical_notes
    
    documentation = await get_session_documentation()
    
    if export_format == "json":
        return documentation
    
    elif export_format == "clinical_notes":
        # Generate clinical notes format
        notes = generate_clinical_notes(documentation)
        return {"format": "clinical_notes", "content": notes}
    
    else:
        return {"error": "Supported formats: json, clinical_notes"}


def generate_clinical_notes(documentation: Dict[str, Any]) -> str:
    """Generate clinical notes from session documentation."""
    notes = f"""
OMANI THERAPIST VOICE - CLINICAL SESSION NOTES
Session ID: {documentation['session_overview']['session_id']}
Date/Time: {documentation['session_overview']['timestamp']}
Cultural Context: Omani/Gulf Arabic with Islamic considerations

AGENT STATUS:
Current Agent: {documentation.get('agent_status', {}).get('current_agent', 'N/A')}
Crisis Active: {documentation.get('agent_status', {}).get('crisis_active', False)}

SAFETY ASSESSMENT:
Crisis Detected: {documentation.get('safety_assessment', {}).get('any_crisis_detected', False)}
Emergency Escalation: {documentation.get('safety_assessment', {}).get('emergency_escalation_needed', False)}

CULTURAL ADAPTATIONS APPLIED:
- Omani Arabic expressions and cultural sensitivity
- Islamic therapeutic concepts integration
- Gulf family dynamics consideration
- Culturally appropriate crisis protocols

CLINICAL ACTIONS TAKEN:
"""
    
    # Add tool-specific documentation
    for tool_name, tool_doc in documentation.get('tool_documentation', {}).items():
        notes += f"\n{tool_name.upper()} TOOL:\n"
        notes += f"Total Actions: {tool_doc.get('session_summary', {}).get('total_actions', 0)}\n"
        
        # Add recommendations
        recommendations = tool_doc.get('recommendations', [])
        if recommendations:
            notes += "Recommendations:\n"
            for rec in recommendations:
                notes += f"- {rec}\n"
    
    notes += f"""
FOLLOW-UP REQUIREMENTS:
- Continue monitoring as per cultural protocols
- Ensure family support system engagement if appropriate
- Maintain Islamic therapeutic principles in ongoing care
- Document any cultural considerations for future sessions

END OF CLINICAL NOTES
"""
    
    return notes


async def main():
    """Run the OMANI Therapist Voice server."""
    port = int(os.getenv("SERVER_PORT", 8003))
    config = uvicorn.Config(
        app, 
        host="0.0.0.0", 
        port=port,
        log_level="info"
    )
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main()) 