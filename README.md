# Therapist - AI-Powered Therapy Assistant

A comprehensive AI-powered therapy assistant with voice interface, CBT tools, crisis intervention, and emotional analysis capabilities.

## 🏗️ Project Structure

```
Therapist/
├── omani-therapist-frontend/     # Next.js React frontend
├── omani-therapist-voice/        # Python FastAPI backend
└── README.md                     # This file
```

## 🚀 Quick Start

### Prerequisites

- **Node.js** (v18 or higher)
- **Python** (v3.8 or higher)
- **npm** or **yarn**
- **pip** (Python package manager)

### Installation

#### 1. Frontend Setup

```bash
# Navigate to frontend directory
cd omani-therapist-frontend

# Install dependencies
npm install
# or
yarn install
```

#### 2. Backend Setup

```bash
# Navigate to backend directory
cd omani-therapist-voice

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt
```

## 🏃‍♂️ Running the Application

### Frontend (Next.js)

```bash
# Navigate to frontend directory
cd omani-therapist-frontend

# Start development server
npm run dev
# or
yarn dev
```

**Frontend will be available at:** `http://localhost:3000`

### Backend (FastAPI)

```bash
# Navigate to backend directory
cd omani-therapist-voice/backend

# Activate virtual environment (if not already activated)
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# Start the backend server
python main.py
```

**Backend will be available at:** `http://localhost:8003`

**Frontend will be available at:** `http://localhost:3001`

**API Documentation will be available at:** `http://localhost:8003/docs`

## 🔧 Configuration

### Frontend Configuration

The frontend is configured to connect to the backend at `http://localhost:8003`. If you need to change this:

1. Open `omani-therapist-frontend/lib/enhancedTherapyClient.ts`
2. Update the base URL in the API client configuration

### Backend Configuration

Backend configuration files are located in:
- `omani-therapist-voice/backend/config/`

Key configuration files:
- `therapy_agent_manager.py` - Therapy agent settings
- `__init__.py` - General configuration

## 🛠️ Available Tools & Features

### Frontend Components
- **CBTToolsPanel** - Cognitive Behavioral Therapy tools
- **CrisisInterventionPanel** - Crisis detection and intervention
- **TherapySessionPanel** - Session management
- **VoiceInterface** - Voice interaction capabilities
- **LanguageSwitcher** - Multi-language support
- **ToolMonitor** - Real-time tool monitoring

### Backend Services
- **CBT Techniques Tool** - Cognitive Behavioral Therapy techniques
- **Crisis Detection Tool** - Real-time crisis detection
- **Emotional Analysis Tool** - Emotion recognition and analysis
- **Session Management Tool** - Therapy session tracking
- **WebSocket Registry** - Real-time communication

## 🔌 Ports Used

| Service | Port | Description |
|---------|------|-------------|
| Frontend | 3001 | Next.js development server |
| Backend | 8003 | FastAPI server |
| Backend Docs | 8003/docs | API documentation |

## 📦 Dependencies

### Frontend Dependencies
- Next.js 14
- React 18
- TypeScript
- Tailwind CSS
- WebSocket client

### Backend Dependencies
- FastAPI
- WebSockets
- Python tools and utilities
- AI/ML libraries for therapy analysis

## 🚨 Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Kill process using port 3000 (frontend)
   lsof -ti:3000 | xargs kill -9
   
   # Kill process using port 8003 (backend)
   lsof -ti:8000 | xargs kill -9
   ```

2. **Python virtual environment issues**
   ```bash
   # Recreate virtual environment
   rm -rf venv
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Node modules issues**
   ```bash
   # Clear npm cache and reinstall
   npm cache clean --force
   rm -rf node_modules package-lock.json
   npm install
   ```

## 📚 Documentation

- **Architecture Documentation**: `omani-therapist-voice/docs/ARCHITECTURE.md`
- **Comprehensive Documentation**: `omani-therapist-voice/docs/COMPREHENSIVE_DOCUMENTATION.md`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test both frontend and backend
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.


---

**Note**: This is a therapy assistant application. For real mental health support, please contact licensed professionals.
