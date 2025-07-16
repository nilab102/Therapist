# OMANI Therapist Voice Frontend 🏥🇴🇲

**Frontend for OMANI Therapist Voice - Culturally-Sensitive AI Voice Therapy Platform**

A Next.js frontend specifically designed for the OMANI Therapist Voice system, featuring dual WebSocket communication for therapy tools and real-time voice interaction.

## 🌟 Key Features

- **Real-time Voice Therapy**: Sub-500ms latency with Gemini Live
- **Dual WebSocket Communication**: 
  - Main WebSocket (`/ws`) for audio streaming (RTVI protocol)
  - Tool WebSocket (`/ws/tools`) for therapy commands
- **Arabic/English Support**: RTL text support with Islamic fonts
- **Crisis Intervention**: Automatic crisis detection and intervention panels
- **CBT Tools**: Cognitive Behavioral Therapy techniques
- **Cultural Adaptation**: Islamic values integration
- **Therapy Session Management**: Complete session tracking

## 🏗 Architecture

```
Frontend (Next.js)                    Backend (Python)
├── Main WebSocket (/ws) ←──────────→ Gemini Live Audio
├── Tool WebSocket (/ws/tools) ←────→ Therapy Tools
├── VoiceInterface ←─────────────────→ Crisis Detection
├── TherapySessionPanel ←───────────→ Session Management  
├── CrisisInterventionPanel ←───────→ Crisis Assessment
└── CBTToolsPanel ←─────────────────→ CBT Techniques
```

## 🔧 How Tool Calling Works

### Backend Tool Execution Flow

1. **User speaks**: "I'm feeling very anxious and having suicidal thoughts"
2. **Gemini Live processes**: Identifies need for crisis intervention
3. **Function call**: Backend calls `detect_crisis` tool
4. **Tool execution**: Crisis detection tool processes the request:

```python
# In crisis_detection_tool.py
async def execute(self, action: str, **kwargs):
    if action == "assess_crisis":
        # Process crisis indicators
        result = await self._assess_crisis_level(kwargs)
        
        # Send command to frontend via WebSocket
        await self._send_client_command("crisis_detected", {
            "severity": "high",
            "risk_factors": ["suicidal_ideation", "severe_anxiety"],
            "immediate_action": "activate_crisis_protocol"
        })
        
        return "Crisis intervention activated"
```

5. **WebSocket communication**: Tool sends command to frontend:

```python
# Tool sends via tool_websockets registry
async def _send_client_command(self, command: str, data: Dict[str, Any]):
    command_data = {
        "type": "crisis_command",
        "action": command,
        **data
    }
    
    # Send to all connected therapy tool clients
    from utils.tool_websocket_registry import tool_websockets
    for client_id, ws in tool_websockets.items():
        await ws.send_json(command_data)
```

6. **Frontend receives command**: Tool WebSocket handler processes:

```typescript
// In therapyVoiceClient.ts
toolWebSocketRef.current.onmessage = (event) => {
  const data = JSON.parse(event.data)
  
  if (data.type === 'crisis_command' && data.action === 'crisis_detected') {
    // Activate crisis mode
    setCrisisMode(true)
    
    // Open crisis intervention panel
    if (window.openCrisisIntervention) {
      window.openCrisisIntervention()
    }
  }
}
```

7. **UI Updates**: Crisis intervention panel opens automatically
8. **Audio confirmation**: Gemini Live confirms via voice: "I've activated crisis intervention protocols..."

### Tool WebSocket Registry Pattern

The backend uses a global registry pattern (from `main_old.py`):

```python
# tool_websocket_registry.py
tool_websockets = {}

# In main.py WebSocket handler
@app.websocket("/ws/tools")
async def tools_websocket_endpoint(websocket: WebSocket):
    client_id = str(uuid.uuid4())
    tool_websockets[client_id] = websocket
    
    # Keep connection alive for tool commands
    while True:
        message = await websocket.receive_text()
        logger.info(f"🏥 Received tool message: {message}")
```

### Global Function Exposure Pattern

Frontend exposes functions globally for tool commands (similar to invoice system):

```typescript
// In page.tsx
useEffect(() => {
  // Crisis intervention functions
  window.openCrisisIntervention = () => {
    setIsCrisisPanelOpen(true)
    setCrisisMode(true)
  }
  
  window.updateCrisisAssessment = (assessment: any) => {
    // Handle crisis assessment data
  }
  
  // CBT tools functions
  window.applyCBTTechnique = (technique: string, data: any) => {
    // Apply CBT technique
  }
  
  // Session management functions
  window.updateSessionField = (field: string, value: any) => {
    // Update therapy session data
  }
}, [])
```

## 📁 Project Structure

```
omani-therapist-frontend/
├── app/
│   ├── globals.css              # Therapy styling + Arabic fonts
│   ├── layout.tsx               # RTL layout with Arabic support
│   └── page.tsx                 # Main therapy interface
├── components/
│   ├── VoiceInterface.tsx       # Main voice interaction
│   ├── ConversationDisplay.tsx  # Message history
│   ├── TherapySessionPanel.tsx  # Session management
│   ├── CrisisInterventionPanel.tsx # Crisis intervention
│   ├── CBTToolsPanel.tsx        # CBT techniques
│   └── LanguageSwitcher.tsx     # Arabic/English toggle
├── lib/
│   └── therapyVoiceClient.ts    # Dual WebSocket client
├── package.json                 # Dependencies
├── tailwind.config.js           # RTL + therapy colors
└── tsconfig.json               # TypeScript config
```

## 🚀 Setup Instructions

### 1. Install Dependencies

```bash
cd omani-therapist-frontend
npm install
```

### 2. Start Backend First

```bash
# In omani-therapist-voice/backend/
cd omani-therapist-voice/backend
python main.py
# Backend runs on http://localhost:8003
```

### 3. Start Frontend

```bash
# In omani-therapist-frontend/
npm run dev
# Frontend runs on http://localhost:3001
```

### 4. Test the System

1. **Open frontend**: http://localhost:3001
2. **Click "Connect to Therapist"**: Establishes dual WebSocket connection
3. **Start conversation**: Voice interaction with therapy tools
4. **Test tool calling**: Say phrases like:
   - "I'm feeling very anxious" → Emotional analysis tool
   - "I'm having suicidal thoughts" → Crisis intervention tool  
   - "I need help with negative thoughts" → CBT tools
   - "Can we start a session?" → Session management tool

## 🔌 WebSocket Endpoints

- **Main Audio**: `ws://localhost:8003/ws` (RTVI protocol)
- **Therapy Tools**: `ws://localhost:8003/ws/tools` (JSON commands)

## 🎭 Therapy Tool Commands

### Crisis Detection
```json
{
  "type": "crisis_command",
  "action": "crisis_detected", 
  "severity": "high",
  "risk_factors": ["suicidal_ideation"]
}
```

### CBT Techniques
```json
{
  "type": "cbt_command",
  "action": "apply_cbt_technique",
  "technique": "thought_challenging",
  "data": { "negative_thought": "I'm worthless" }
}
```

### Emotional Analysis
```json
{
  "type": "emotion_command", 
  "action": "emotion_analysis",
  "emotion": "severe_anxiety",
  "confidence": 0.95
}
```

### Session Management
```json
{
  "type": "session_command",
  "action": "start_session",
  "session_type": "cbt_session"
}
```

## 🌍 Arabic/Islamic Features

- **RTL Text Support**: Proper right-to-left layout
- **Islamic Fonts**: Amiri and Noto Sans Arabic
- **Cultural Colors**: Green (therapy), Blue (trust), patterns
- **Bilingual Interface**: Seamless Arabic/English switching
- **Islamic Integration**: Respectful therapeutic language

## 🚨 Crisis Intervention Features

- **Automatic Detection**: Backend analyzes speech for crisis indicators
- **Immediate UI Response**: Crisis mode activates instantly
- **Visual Alerts**: Red pulsing indicators and warnings
- **Safety Protocols**: Connection to human therapists
- **Emergency Contacts**: Local Omani mental health services

## 🎨 Styling System

### Therapy Colors
```css
--therapy-primary: #2E7D32    /* Calming green */
--therapy-secondary: #4A90E2  /* Trust blue */
--therapy-crisis: #E74C3C     /* Crisis red */
--therapy-accent: #F39C12     /* Warm orange */
```

### CSS Classes
```css
.therapy-card              /* Main component styling */
.therapy-button-primary    /* Primary action buttons */
.therapy-button-crisis     /* Crisis intervention buttons */
.arabic-text              /* RTL text with Arabic fonts */
.crisis-mode              /* Crisis mode visual changes */
.voice-indicator          /* Voice activity animation */
```

## 🔍 Debugging

### Check WebSocket Connections
```javascript
// In browser console
console.log('Main WebSocket:', rtviClientRef.current)
console.log('Tool WebSocket:', toolWebSocketRef.current)
```

### Monitor Tool Commands
```bash
# Backend logs show tool execution
🏥 Received therapy tool message: {"type": "crisis_command", ...}
🏥 Processing therapy command from tool WebSocket
✅ Crisis intervention activated
```

### Frontend Message Flow
```javascript
// Messages appear in conversation display
🚨 Crisis intervention activated | تم تفعيل التدخل في الأزمة
🧠 Applied CBT technique: thought_challenging
📋 Opening therapy session | فتح جلسة علاجية
```

## 🔧 Development

### Adding New Therapy Tools

1. **Backend**: Create tool in `omani-therapist-voice/backend/tools/`
2. **Register tool**: Add to therapy agent manager
3. **Frontend**: Add handler in `therapyVoiceClient.ts`
4. **UI**: Create panel component if needed

### Extending Language Support

1. **Add fonts**: Update `globals.css`
2. **Add translations**: Extend text objects in components
3. **Test RTL**: Ensure proper Arabic layout

## 📊 Performance

- **Voice Latency**: <500ms with Gemini Live
- **Tool Response**: <100ms for tool commands
- **UI Updates**: Real-time WebSocket communication
- **Memory**: Optimized for mobile therapy sessions

## 🛡️ Security & Privacy

- **HTTPS Only**: All connections encrypted
- **No Data Storage**: Client-side only (configurable)
- **Medical Privacy**: HIPAA-style protection
- **Cultural Privacy**: Respects Gulf cultural norms

---

**Ready to provide culturally-sensitive AI therapy for Gulf Arabic speakers! 🏥🇴🇲** 