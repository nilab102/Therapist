# OMANI Therapist Voice - Architecture Documentation

## 🏗️ System Overview

OMANI Therapist Voice is a sophisticated AI-powered therapeutic platform designed for Gulf Arabic speakers. The system architecture follows a microservices pattern with real-time voice processing, cultural adaptation, and clinical safety protocols. The platform now supports **dual AI service integration** with intelligent fallback mechanisms for maximum reliability and performance.

## 📐 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                            │
├─────────────────────────────────────────────────────────────────┤
│  Web Browser (Next.js)  │  Mobile App  │  Desktop App         │
│  • Voice Interface      │  • Native UI │  • Electron App      │
│  • Cultural UI          │  • Offline   │  • Desktop Voice     │
│  • Session Management   │  • Sync      │  • Local Processing  │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                      TRANSPORT LAYER                           │
├─────────────────────────────────────────────────────────────────┤
│  WebSocket (RTVI)       │  HTTP REST API  │  WebRTC           │
│  • Real-time Audio      │  • Session Mgmt │  • P2P Voice      │
│  • Bidirectional        │  • Tool Config  │  • Low Latency    │
│  • Protobuf Frames      │  • Health Check │  • Fallback       │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                      API GATEWAY LAYER                         │
├─────────────────────────────────────────────────────────────────┤
│  FastAPI Application    │  CORS Middleware │  Rate Limiting   │
│  • WebSocket Endpoints  │  • Security      │  • Load Balancing│
│  • REST Endpoints       │  • Authentication│  • Monitoring    │
│  • Health Monitoring    │  • Authorization │  • Logging       │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                      CORE SERVICES LAYER                       │
├─────────────────────────────────────────────────────────────────┤
│  Therapy Agent Manager  │  Tool Registry   │  Session Manager │
│  • Multi-Agent System   │  • Tool Discovery│  • State Mgmt    │
│  • Agent Switching      │  • Tool Loading  │  • Persistence   │
│  • Cultural Context     │  • Tool Config   │  • Recovery      │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                      THERAPEUTIC TOOLS LAYER                   │
├─────────────────────────────────────────────────────────────────┤
│  Crisis Detection       │  CBT Techniques  │  Emotional Analysis│
│  • Risk Assessment      │  • I-CBT         │  • Sentiment      │
│  • Safety Protocols     │  • Cultural CBT  │  • Pattern Recog  │
│  • Emergency Escalation │  • Islamic CBT   │  • Mood Tracking  │
│                         │                  │                   │
│  Session Management     │  Cultural Tools  │  Documentation    │
│  • Progress Tracking    │  • Dialect Adapt │  • Clinical Notes │
│  • Goal Setting         │  • Islamic Int.  │  • Compliance     │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                      AI PROCESSING LAYER                       │
├─────────────────────────────────────────────────────────────────┤
│  Pipecat Pipeline       │  Dual AI Services │  Voice Processing │
│  • Audio Pipeline       │  • OpenAI Realtime│  • VAD (Silero)   │
│  • Context Aggregation  │  • Gemini Live    │  • Transcription  │
│  • Frame Processing     │  • Fallback Logic │  • Audio Quality  │
│  • Service Selection    │  • Load Balancing │  • Quality Check  │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                      DATA LAYER                                │
├─────────────────────────────────────────────────────────────────┤
│  Session Storage        │  Clinical Data   │  Cultural Data   │
│  • Redis Cache          │  • Encrypted DB  │  • Dialect DB    │
│  • Session State        │  • HIPAA Compl.  │  • Islamic Ref.  │
│  • Real-time Sync       │  • Audit Logs    │  • Cultural Ref. │
└─────────────────────────────────────────────────────────────────┘
```

## 🔄 Data Flow Architecture

### 1. Voice Input Flow with Dual AI Services

```
User Voice Input
       │
       ▼
┌─────────────────┐
│  Microphone     │
│  (Browser/App)  │
└─────────────────┘
       │
       ▼
┌─────────────────┐
│  WebSocket      │
│  (RTVI Client)  │
└─────────────────┘
       │
       ▼
┌─────────────────┐
│  FastAPI        │
│  WebSocket      │
│  Endpoint       │
└─────────────────┘
       │
       ▼
┌─────────────────┐
│  Pipecat        │
│  Pipeline       │
└─────────────────┘
       │
       ▼
┌─────────────────┐
│  Service        │
│  Selection      │
│  Logic          │
└─────────────────┘
       │
       ▼
┌─────────────────┐    ┌─────────────────┐
│  OpenAI         │    │  Gemini Live    │
│  Realtime API   │    │  (Fallback)     │
│  (Preferred)    │    │                 │
└─────────────────┘    └─────────────────┘
       │                       │
       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐
│  Therapeutic    │    │  Therapeutic    │
│  Tools          │    │  Tools          │
└─────────────────┘    └─────────────────┘
       │                       │
       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐
│  Response       │    │  Response       │
│  Generation     │    │  Generation     │
└─────────────────┘    └─────────────────┘
       │                       │
       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐
│  Voice Output   │    │  Voice Output   │
│  (Cultural      │    │  (Cultural      │
│   Adaptation)   │    │   Adaptation)   │
└─────────────────┘    └─────────────────┘
```

### 2. AI Service Selection and Fallback Flow

```
Service Request
       │
       ▼
┌─────────────────┐
│  API Key        │
│  Validation     │
└─────────────────┘
       │
       ▼
┌─────────────────┐
│  Priority       │
│  Check          │
│  (OpenAI First) │
└─────────────────┘
       │
       ▼
┌─────────────────┐
│  OpenAI         │
│  Realtime       │
│  Available?     │
└─────────────────┘
       │
       ▼
       ├─ YES ──► ┌─────────────────┐
       │          │  Use OpenAI     │
       │          │  Realtime API   │
       │          └─────────────────┘
       │
       ▼
       ├─ NO ───► ┌─────────────────┐
                  │  Check Gemini   │
                  │  Live Available │
                  └─────────────────┘
                          │
                          ▼
                  ┌─────────────────┐
                  │  Use Gemini     │
                  │  Live (Fallback)│
                  └─────────────────┘
                          │
                          ▼
                  ┌─────────────────┐
                  │  Error: No      │
                  │  Service        │
                  │  Available      │
                  └─────────────────┘
```

### 3. Therapeutic Tool Flow

```
User Request
       │
       ▼
┌─────────────────┐
│  Tool Registry  │
│  (Discovery)    │
└─────────────────┘
       │
       ▼
┌─────────────────┐
│  Tool Instance  │
│  (Execution)    │
└─────────────────┘
       │
       ▼
┌─────────────────┐
│  Cultural       │
│  Adaptation     │
└─────────────────┘
       │
       ▼
┌─────────────────┐
│  Clinical       │
│  Safety Check   │
└─────────────────┘
       │
       ▼
┌─────────────────┐
│  Response       │
│  Generation     │
└─────────────────┘
```

## 🧠 Model Integration Architecture

### Dual AI Service Integration

The system now supports **two native audio AI services** with intelligent fallback mechanisms:

#### OpenAI Realtime API (Preferred Service)
```python
# OpenAI Realtime Service Integration
class OpenAIRealtimeTherapyService:
    """
    OpenAI Realtime Beta service optimized for therapy.
    Preferred service due to ultra-low latency and reliability.
    """
    
    def __init__(self, api_key: str, system_instruction: str):
        self.session_properties = SessionProperties(
            input_audio_transcription=InputAudioTranscription(),
            turn_detection=SemanticTurnDetection(),
            input_audio_noise_reduction=InputAudioNoiseReduction(type="near_field"),
            instructions=system_instruction
        )
        
        self.llm_service = OpenAIRealtimeBetaLLMService(
            api_key=api_key,
            session_properties=self.session_properties,
            start_audio_paused=False,
        )
```

#### Gemini Live (Fallback Service)
```python
# Gemini Live Service Integration
class GeminiTherapyContext(OpenAILLMContext):
    """
    Therapy-safe context for Gemini Live with clinical boundaries.
    Fallback service when OpenAI Realtime is unavailable.
    """
    
    def __init__(self, messages=None, system_message=None):
        if messages:
            messages = GeminiTherapyContextFilter.filter_messages_for_therapy(messages)
        super().__init__(messages, system_message)
    
    def get_messages_for_initializing_history(self):
        original_messages = super().get_messages_for_initializing_history()
        filtered_messages = GeminiTherapyContextFilter.filter_messages_for_therapy(original_messages)
        return filtered_messages
```

### Service Selection Logic

```python
# Intelligent Service Selection
async def create_native_audio_therapy_llm(enable_function_calling=False, force_service=None):
    """
    Create an LLM service with intelligent fallback logic.
    Priority: OpenAI Realtime > Gemini Live > Error
    """
    
    # Force service selection if specified
    if force_service == "openai_realtime":
        return await create_therapy_openai_realtime_llm(SYSTEM_INSTRUCTION, tools)
    elif force_service == "gemini_live":
        return await create_therapy_gemini_llm(SYSTEM_INSTRUCTION, tools)
    
    # Normal priority-based fallback logic
    # 1. Try OpenAI Realtime API first (preferred for therapy)
    openai_key = os.getenv("OPENAI_API_KEY")
    if OPENAI_REALTIME_AVAILABLE and is_valid_api_key(openai_key, "openai"):
        try:
            llm_service = await create_therapy_openai_realtime_llm(SYSTEM_INSTRUCTION, tools)
            return llm_service, "openai_realtime"
        except Exception as e:
            logger.warning(f"OpenAI Realtime failed: {e}, trying Gemini Live fallback")
    
    # 2. Fallback to Gemini Multimodal Live
    google_key = os.getenv("GOOGLE_API_KEY")
    if is_valid_api_key(google_key, "google"):
        try:
            llm_service = await create_therapy_gemini_llm(SYSTEM_INSTRUCTION, tools)
            return llm_service, "gemini_live"
        except Exception as e:
            logger.error(f"Gemini Live also failed: {e}")
    
    # 3. No service available
    raise ValueError("No LLM service available. Please configure OpenAI or Google API keys.")
```

### Multi-Agent System Architecture

```python
# Therapy Agent Manager with Dual Service Support
class TherapyAgentManager:
    """
    Manages different therapeutic agents with cultural sensitivity.
    Supports both OpenAI Realtime and Gemini Live services.
    """
    
    def __init__(self):
        self.agents = {
            "general_therapy": {
                "instructions": GENERAL_THERAPY_INSTRUCTION,
                "tools": ["crisis_detection", "cbt_techniques", "emotional_analysis"],
                "cultural_context": "omani_gulf_arabic",
                "supported_services": ["openai_realtime", "gemini_live"]
            },
            "crisis_intervention": {
                "instructions": CRISIS_INTERVENTION_INSTRUCTION,
                "tools": ["crisis_detection", "session_management"],
                "cultural_context": "emergency_cultural_protocols",
                "supported_services": ["openai_realtime", "gemini_live"]
            },
            "cbt_specialist": {
                "instructions": CBT_SPECIALIST_INSTRUCTION,
                "tools": ["cbt_techniques", "emotional_analysis"],
                "cultural_context": "islamic_cbt_integration",
                "supported_services": ["openai_realtime", "gemini_live"]
            }
        }
```

## 🔧 Component Architecture

### 1. Backend Components

#### FastAPI Application (`main.py`)
- **WebSocket Endpoints**: Real-time voice communication
- **REST Endpoints**: Session management and configuration
- **Middleware**: CORS, authentication, rate limiting
- **Health Monitoring**: System status and diagnostics
- **Service Selection**: Intelligent AI service routing
- **Fallback Management**: Automatic service switching

#### Dual AI Service Integration
```python
# Service Creation Functions
async def create_therapy_openai_realtime_llm(system_instruction: str, tools_schema=None):
    """Create OpenAI Realtime Beta LLM service optimized for therapy."""
    openai_key = os.getenv("OPENAI_API_KEY")
    
    if not is_valid_openai_api_key(openai_key):
        raise ValueError("Invalid or missing OPENAI_API_KEY")
    
    session_properties = SessionProperties(
        input_audio_transcription=InputAudioTranscription(),
        turn_detection=SemanticTurnDetection(),
        input_audio_noise_reduction=InputAudioNoiseReduction(type="near_field"),
        instructions=system_instruction
    )
    
    return OpenAIRealtimeBetaLLMService(
        api_key=openai_key,
        session_properties=session_properties,
        start_audio_paused=False,
    )

async def create_therapy_gemini_llm(system_instruction: str, tools_schema=None):
    """Create Gemini Live LLM service optimized for therapy."""
    google_key = os.getenv("GOOGLE_API_KEY")
    
    if not is_valid_google_api_key(google_key):
        raise ValueError("Invalid or missing GOOGLE_API_KEY")
    
    return GeminiMultimodalLiveLLMService(
        api_key=google_key,
        system_instruction=system_instruction,
        voice_id="Zephyr",  # Calm, empathetic voice
        models='models/gemini-live-2.5-flash-preview',
        temperature=1,
        transcribe_model_audio=True,
        tools=tools_schema,
    )
```

#### Therapy Agent Manager (`config/therapy_agent_manager.py`)
- **Agent Registry**: Manages different therapeutic agents
- **Context Switching**: Seamless agent transitions
- **Cultural Adaptation**: Context-aware responses
- **Clinical Protocols**: Safety and escalation management
- **Service Compatibility**: Support for both AI services

#### Tool Registry (`tools/tool_registry.py`)
- **Tool Discovery**: Dynamic tool loading
- **Tool Configuration**: Parameter management
- **Tool Execution**: Safe tool invocation
- **Tool Monitoring**: Performance and usage tracking
- **Service Agnostic**: Works with both AI services

### 2. Therapeutic Tools

#### Base Tool (`tools/base_tool.py`)
```python
class BaseTool(ABC):
    """
    Base class for all therapeutic tools.
    Compatible with both OpenAI Realtime and Gemini Live.
    """
    
    def __init__(self, rtvi_processor, task=None):
        self.rtvi_processor = rtvi_processor
        self.task = task
        self.clinical_data = {}
        self.crisis_detected = False
        self.supported_services = ["openai_realtime", "gemini_live"]
```

#### Crisis Detection Tool (`tools/crisis_detection_tool.py`)
- **Risk Assessment**: Suicide and self-harm detection
- **Safety Planning**: Crisis intervention protocols
- **Emergency Escalation**: Professional referral system
- **Cultural Crisis Protocols**: Family and community involvement
- **Service Compatibility**: Works with both AI services

#### CBT Techniques Tool (`tools/cbt_techniques_tool.py`)
- **Islamic CBT**: Religious concept integration
- **Cultural Adaptation**: Gulf-specific techniques
- **Thought Challenging**: Culturally-sensitive approaches
- **Behavioral Activation**: Community-based activities
- **Service Compatibility**: Works with both AI services

#### Emotional Analysis Tool (`tools/emotional_analysis_tool.py`)
- **Sentiment Analysis**: Real-time emotion detection
- **Pattern Recognition**: Mood trend analysis
- **Cultural Context**: Emotion expression in Gulf culture
- **Clinical Documentation**: Emotional state tracking
- **Service Compatibility**: Works with both AI services

#### Session Management Tool (`tools/session_management_tool.py`)
- **Progress Tracking**: Therapeutic goal monitoring
- **Session Documentation**: Clinical record keeping
- **Cultural Notes**: Cultural context documentation
- **Follow-up Planning**: Continuity of care
- **Service Compatibility**: Works with both AI services

### 3. Frontend Components

#### Voice Interface (`components/VoiceInterface.tsx`)
- **Real-time Audio**: WebSocket-based voice communication
- **Cultural UI**: Omani Arabic interface elements
- **Session Controls**: Start, pause, end session
- **Emergency Access**: Crisis intervention buttons
- **Service Status**: Display current AI service being used

#### Therapy Session Panel (`components/TherapySessionPanel.tsx`)
- **Session Status**: Real-time session information
- **Agent Display**: Current therapeutic agent
- **Tool Status**: Active therapeutic tools
- **Cultural Indicators**: Cultural adaptation status
- **Service Indicator**: Shows which AI service is active

#### Crisis Intervention Panel (`components/CrisisInterventionPanel.tsx`)
- **Crisis Alerts**: Real-time crisis detection
- **Emergency Resources**: Local crisis resources
- **Safety Planning**: Crisis safety plan interface
- **Professional Referral**: Referral system access
- **Service Reliability**: Ensures crisis detection works with both services

## 🔄 Real-time Communication Architecture

### WebSocket Protocol

```typescript
// WebSocket Message Types with Service Information
interface WebSocketMessage {
  type: 'audio_frame' | 'therapeutic_command' | 'crisis_alert' | 'session_update' | 'service_status';
  data: any;
  timestamp: string;
  session_id: string;
  cultural_context?: CulturalContext;
  ai_service?: 'openai_realtime' | 'gemini_live';
  service_status?: ServiceStatus;
}

interface ServiceStatus {
  current_service: 'openai_realtime' | 'gemini_live';
  fallback_available: boolean;
  latency: number;
  reliability_score: number;
}
```

### RTVI Integration with Dual Services

```typescript
// RTVI Client Configuration with Service Awareness
const rtviConfig = {
  transport: new WebSocketTransport({
    url: 'ws://localhost:8003/ws',
    protocols: ['rtvi-protocol']
  }),
  pipeline: {
    audio: {
      sampleRate: 16000,
      channels: 1,
      encoding: 'pcm'
    },
    vad: {
      model: 'silero',
      params: {
        stop_secs: 1.0,
        start_secs: 0.3
      }
    },
    service_selection: {
      preferred_service: 'openai_realtime',
      fallback_service: 'gemini_live',
      auto_fallback: true
    }
  }
};
```

## 🗄️ Data Architecture

### Session Data Model with Service Information

```typescript
interface SessionData {
  session_id: string;
  user_id: string;
  start_time: string;
  end_time?: string;
  current_agent: string;
  cultural_context: CulturalContext;
  clinical_data: ClinicalData;
  therapeutic_tools: ToolStatus[];
  crisis_flags: CrisisFlags;
  session_documentation: SessionDocumentation;
  ai_service_info: AIServiceInfo;
}

interface AIServiceInfo {
  current_service: 'openai_realtime' | 'gemini_live';
  service_history: ServiceTransition[];
  fallback_events: FallbackEvent[];
  performance_metrics: ServicePerformance;
}

interface ServiceTransition {
  from_service: 'openai_realtime' | 'gemini_live';
  to_service: 'openai_realtime' | 'gemini_live';
  timestamp: string;
  reason: 'preferred' | 'fallback' | 'error' | 'manual';
}
```

### Clinical Data Model

```typescript
interface ClinicalData {
  crisis_detected: boolean;
  emergency_escalation_needed: boolean;
  professional_referral_suggested: boolean;
  risk_assessment: RiskAssessment;
  safety_plan: SafetyPlan;
  therapeutic_progress: TherapeuticProgress;
  cultural_notes: CulturalNotes;
  service_reliability: ServiceReliability;
}

interface ServiceReliability {
  current_service: 'openai_realtime' | 'gemini_live';
  uptime_percentage: number;
  average_latency: number;
  error_rate: number;
  last_fallback: string;
}
```

### Cultural Context Model

```typescript
interface CulturalContext {
  dialect: 'omani_arabic' | 'gulf_arabic' | 'standard_arabic';
  religious_preference: 'islamic' | 'secular' | 'mixed';
  family_dynamics: FamilyDynamics;
  gender_considerations: GenderConsiderations;
  community_support: CommunitySupport;
  cultural_values: CulturalValues;
  service_preference: 'openai_realtime' | 'gemini_live' | 'auto';
}
```

## 🔒 Security Architecture

### Authentication & Authorization

```python
# Security Middleware with Service Validation
class TherapeuticSecurityMiddleware:
    """
    Security middleware for therapeutic sessions with dual service support.
    """
    
    def __init__(self):
        self.encryption_key = os.getenv("ENCRYPTION_KEY")
        self.jwt_secret = os.getenv("JWT_SECRET")
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.google_key = os.getenv("GOOGLE_API_KEY")
    
    async def authenticate_session(self, session_id: str) -> bool:
        # Session authentication logic
        pass
    
    async def authorize_therapeutic_access(self, user_id: str, tool_name: str) -> bool:
        # Therapeutic tool authorization
        pass
    
    async def validate_service_access(self, service_type: str) -> bool:
        # Validate access to specific AI service
        if service_type == "openai_realtime":
            return is_valid_openai_api_key(self.openai_key)
        elif service_type == "gemini_live":
            return is_valid_google_api_key(self.google_key)
        return False
```

### Data Protection

- **End-to-End Encryption**: All voice data encrypted in transit
- **Data Anonymization**: Clinical data anonymized for privacy
- **Audit Logging**: Comprehensive security event logging
- **HIPAA Compliance**: Clinical data protection standards
- **Cultural Privacy**: Respect for cultural privacy norms
- **Service Security**: Secure API key management for both services

## 📊 Monitoring & Observability

### Health Monitoring with Service Status

```python
@app.get("/health")
async def health_check():
    """Health check endpoint for therapeutic service with dual AI support."""
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
            "dual_service_fallback": True,
            "available_tools": global_tool_registry.list_available_tools(),
            "therapeutic_agents": ["general_therapy", "crisis_intervention", "cbt_specialist"]
        },
        "expected_latency": "sub-500ms" if therapy_available else "service_unavailable",
        "clinical_safety": "enabled",
        "cultural_sensitivity": "gulf_arabic_islamic",
        "service_priority": {
            "preferred": "openai_realtime" if openai_available else "gemini_live" if gemini_available else "none",
            "fallback": "gemini_live" if openai_available and gemini_available else "none"
        }
    }
```

### Performance Metrics

- **Latency Monitoring**: End-to-end response time tracking for both services
- **Accuracy Metrics**: Crisis detection accuracy across services
- **Cultural Sensitivity**: Dialect compliance monitoring
- **Clinical Safety**: Safety protocol effectiveness
- **System Reliability**: Uptime and error rate tracking
- **Service Performance**: Comparative performance between OpenAI and Gemini
- **Fallback Effectiveness**: Success rate of service transitions

### Service Performance Monitoring

```python
class ServicePerformanceMonitor:
    """
    Monitor performance of both AI services.
    """
    
    def __init__(self):
        self.openai_metrics = ServiceMetrics("openai_realtime")
        self.gemini_metrics = ServiceMetrics("gemini_live")
        self.fallback_events = []
    
    async def record_service_usage(self, service_type: str, latency: float, success: bool):
        if service_type == "openai_realtime":
            await self.openai_metrics.record_usage(latency, success)
        elif service_type == "gemini_live":
            await self.gemini_metrics.record_usage(latency, success)
    
    async def record_fallback_event(self, from_service: str, to_service: str, reason: str):
        self.fallback_events.append({
            "from": from_service,
            "to": to_service,
            "reason": reason,
            "timestamp": datetime.now().isoformat()
        })
```

## 🚀 Scalability Architecture

### Horizontal Scaling with Service Distribution

```python
# Load Balancer Configuration with Service Awareness
class TherapeuticLoadBalancer:
    """
    Load balancer for therapeutic sessions with dual service support.
    """
    
    def __init__(self):
        self.session_servers = []
        self.health_check_interval = 30
        self.service_preferences = {
            "openai_realtime": 0.7,  # 70% preference for OpenAI
            "gemini_live": 0.3       # 30% preference for Gemini
        }
    
    async def route_session(self, session_id: str, user_preference: str = None) -> str:
        # Session routing logic with service preference
        if user_preference and user_preference in self.service_preferences:
            return await self.route_to_preferred_service(user_preference)
        return await self.route_with_load_balancing()
    
    async def health_check_servers(self):
        # Server health monitoring for both services
        pass
```

### Session Distribution

- **Session Affinity**: Consistent session routing
- **Geographic Distribution**: Regional server deployment
- **Cultural Optimization**: Region-specific cultural adaptations
- **Emergency Routing**: Crisis session prioritization
- **Service Distribution**: Load balancing between OpenAI and Gemini
- **Fallback Routing**: Automatic service switching during failures

## 🔧 Configuration Management

### Environment Configuration with Dual Service Support

```python
# Configuration Management for Dual AI Services
class TherapeuticConfig:
    """
    Configuration management for therapeutic system with dual AI support.
    """
    
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        self.cultural_settings = self.load_cultural_settings()
        self.clinical_protocols = self.load_clinical_protocols()
        self.emergency_resources = self.load_emergency_resources()
        self.service_config = self.load_service_configuration()
    
    def load_service_configuration(self):
        return {
            "preferred_service": "openai_realtime",
            "fallback_service": "gemini_live",
            "auto_fallback": True,
            "service_timeout": 30,
            "retry_attempts": 3,
            "performance_thresholds": {
                "max_latency": 500,
                "min_reliability": 0.95
            }
        }
```

### Cultural Configuration

```json
{
  "cultural_settings": {
    "omani_arabic": {
      "dialect_features": ["soft_consonants", "stretched_vowels"],
      "cultural_expressions": ["insha'Allah", "habibi", "masha'Allah"],
      "family_dynamics": "extended_family_support",
      "religious_integration": "islamic_therapeutic_concepts",
      "service_preferences": {
        "openai_realtime": "preferred_for_accuracy",
        "gemini_live": "fallback_for_reliability"
      }
    }
  }
}
```

## 🔄 Deployment Architecture

### Container Architecture with Service Dependencies

```dockerfile
# Backend Docker Configuration with Dual Service Support
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .

# Install dependencies for both OpenAI and Gemini
RUN pip install -r requirements.txt

# Install OpenAI Realtime Beta if available
RUN pip install pipecat[openai-realtime-beta] || echo "OpenAI Realtime not available"

COPY . .
EXPOSE 8003

# Environment variables for both services
ENV OPENAI_API_KEY=""
ENV GOOGLE_API_KEY=""
ENV PREFERRED_SERVICE="openai_realtime"
ENV FALLBACK_SERVICE="gemini_live"

CMD ["python", "main.py"]
```

### Service Discovery with Dual Service Support

```python
# Service Registry with Dual AI Services
class TherapeuticServiceRegistry:
    """
    Service registry for therapeutic components with dual AI support.
    """
    
    def __init__(self):
        self.services = {}
        self.health_checks = {}
        self.ai_services = {
            "openai_realtime": {
                "status": "unknown",
                "last_check": None,
                "performance": {}
            },
            "gemini_live": {
                "status": "unknown",
                "last_check": None,
                "performance": {}
            }
        }
    
    async def register_service(self, service_name: str, service_url: str):
        # Service registration
        pass
    
    async def discover_service(self, service_name: str) -> str:
        # Service discovery
        pass
    
    async def check_ai_service_health(self, service_type: str) -> bool:
        # Health check for specific AI service
        pass
```

## 📈 Future Architecture Considerations

### AI Model Evolution

- **Model Fine-tuning**: Cultural-specific model training for both services
- **Multi-modal Enhancement**: Video and gesture integration
- **Personalization**: Individual therapeutic adaptation
- **Continuous Learning**: Session-based model improvement
- **Service Optimization**: Performance tuning for each AI service
- **Hybrid Approaches**: Combining strengths of both services

### Cultural Expansion

- **Regional Dialects**: Additional Gulf Arabic dialects
- **Religious Variations**: Different Islamic traditions
- **Cultural Nuances**: Sub-cultural adaptations
- **Language Expansion**: Additional regional languages
- **Service Adaptation**: Optimizing each service for cultural contexts

### Clinical Enhancement

- **Evidence-based Integration**: Clinical research integration
- **Professional Collaboration**: Therapist-AI collaboration
- **Outcome Measurement**: Therapeutic effectiveness tracking
- **Regulatory Compliance**: Clinical standards compliance
- **Service Reliability**: Ensuring clinical safety across both services

### Technical Enhancements

- **Advanced Fallback Logic**: More sophisticated service switching
- **Performance Optimization**: Service-specific optimizations
- **Load Balancing**: Intelligent distribution between services
- **Monitoring Enhancement**: Advanced service performance tracking
- **Security Hardening**: Enhanced security for dual service architecture


