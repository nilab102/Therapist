#!/bin/bash

# Setup Git Commits for Therapist Project
# This script creates a series of logical commits for the project

echo "🚀 Setting up Git repository with commit history..."

# Initialize git repository if not already done
if [ ! -d ".git" ]; then
    git init
    echo "✅ Initialized git repository"
fi

# Add all files
git add .

# Commit 1: Initial project structure
git commit -m "🎉 Initial commit: Project structure and documentation

- Add comprehensive README with installation and setup instructions
- Create .gitignore for both frontend and backend
- Add environment example files for configuration
- Document project architecture and features
- Include troubleshooting guide and port information"

# Create logs directory for backend
mkdir -p omani-therapist-voice/logs
mkdir -p omani-therapist-voice/uploads
mkdir -p omani-therapist-voice/models

# Add and commit backend structure
git add omani-therapist-voice/logs/
git add omani-therapist-voice/uploads/
git add omani-therapist-voice/models/
git commit -m "📁 Add backend directory structure

- Create logs directory for application logging
- Add uploads directory for file storage
- Create models directory for AI/ML models
- Prepare backend file organization"

# Create frontend environment file
cp omani-therapist-frontend/env.example omani-therapist-frontend/.env.local

# Add and commit frontend setup
git add omani-therapist-frontend/.env.local
git commit -m "⚙️ Add frontend environment configuration

- Copy environment example to .env.local
- Configure API endpoints and WebSocket URLs
- Set up feature flags and voice interface settings
- Configure session management and UI preferences"

# Create backend environment file
cp omani-therapist-voice/env.example omani-therapist-voice/.env

# Add and commit backend setup
git add omani-therapist-voice/.env
git commit -m "🔧 Add backend environment configuration

- Copy environment example to .env
- Configure server settings and database connection
- Set up security keys and API configurations
- Configure voice processing and WebSocket settings"

# Create package.json for frontend if it doesn't exist
if [ ! -f "omani-therapist-frontend/package.json" ]; then
    cat > omani-therapist-frontend/package.json << 'EOF'
{
  "name": "omani-therapist-frontend",
  "version": "1.0.0",
  "description": "AI-Powered Therapy Assistant Frontend",
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "next": "^14.0.0",
    "react": "^18.0.0",
    "react-dom": "^18.0.0",
    "typescript": "^5.0.0",
    "@types/node": "^20.0.0",
    "@types/react": "^18.0.0",
    "@types/react-dom": "^18.0.0",
    "tailwindcss": "^3.3.0",
    "autoprefixer": "^10.4.0",
    "postcss": "^8.4.0"
  },
  "devDependencies": {
    "eslint": "^8.0.0",
    "eslint-config-next": "^14.0.0"
  }
}
EOF
    git add omani-therapist-frontend/package.json
    git commit -m "📦 Add frontend package.json

- Define Next.js project dependencies
- Configure development and build scripts
- Add TypeScript and Tailwind CSS support
- Set up ESLint for code quality"
fi

# Create requirements.txt for backend if it doesn't exist
if [ ! -f "omani-therapist-voice/requirements.txt" ]; then
    cat > omani-therapist-voice/requirements.txt << 'EOF'
fastapi==0.104.1
uvicorn[standard]==0.24.0
websockets==12.0
python-multipart==0.0.6
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-dotenv==1.0.0
sqlalchemy==2.0.23
alembic==1.12.1
pydantic==2.5.0
pydantic-settings==2.1.0
requests==2.31.0
aiofiles==23.2.1
python-socketio==5.10.0
numpy==1.24.3
pandas==2.0.3
scikit-learn==1.3.2
librosa==0.10.1
soundfile==0.12.1
transformers==4.35.2
torch==2.1.1
torchaudio==2.1.1
EOF
    git add omani-therapist-voice/requirements.txt
    git commit -m "🐍 Add backend requirements.txt

- Define Python dependencies for FastAPI backend
- Include AI/ML libraries for therapy analysis
- Add audio processing libraries for voice interface
- Configure WebSocket and database dependencies"
fi

# Create a simple main.py for backend if it doesn't exist
if [ ! -f "omani-therapist-voice/main.py" ]; then
    cat > omani-therapist-voice/main.py << 'EOF'
#!/usr/bin/env python3
"""
Therapist Assistant Backend
AI-Powered Therapy Assistant with Voice Interface
"""

import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Therapist Assistant API",
    description="AI-Powered Therapy Assistant Backend",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Therapist Assistant API", "status": "running"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "therapist-assistant"}

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    debug = os.getenv("DEBUG", "true").lower() == "true"
    
    print(f"🚀 Starting Therapist Assistant Backend on {host}:{port}")
    uvicorn.run(app, host=host, port=port, reload=debug)
EOF
    git add omani-therapist-voice/main.py
    git commit -m "🐍 Add basic FastAPI backend

- Create main.py with FastAPI application setup
- Configure CORS middleware for frontend communication
- Add health check and root endpoints
- Set up environment-based configuration"
fi

# Create a simple page.tsx for frontend if it doesn't exist
if [ ! -f "omani-therapist-frontend/app/page.tsx" ]; then
    mkdir -p omani-therapist-frontend/app
    cat > omani-therapist-frontend/app/page.tsx << 'EOF'
'use client';

import { useState, useEffect } from 'react';

export default function Home() {
  const [status, setStatus] = useState('Loading...');

  useEffect(() => {
    // Check backend health
    fetch('http://localhost:8000/health')
      .then(response => response.json())
      .then(data => {
        setStatus('Backend Connected');
      })
      .catch(error => {
        setStatus('Backend Disconnected');
      });
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
      <div className="bg-white rounded-lg shadow-xl p-8 max-w-md w-full mx-4">
        <div className="text-center">
          <h1 className="text-3xl font-bold text-gray-800 mb-4">
            Therapist Assistant
          </h1>
          <p className="text-gray-600 mb-6">
            AI-Powered Therapy Assistant
          </p>
          <div className="bg-gray-100 rounded-lg p-4">
            <p className="text-sm text-gray-700">
              Backend Status: <span className="font-semibold">{status}</span>
            </p>
          </div>
          <div className="mt-6 text-sm text-gray-500">
            <p>Frontend: http://localhost:3000</p>
            <p>Backend: http://localhost:8000</p>
            <p>API Docs: http://localhost:8000/docs</p>
          </div>
        </div>
      </div>
    </div>
  );
}
EOF
    git add omani-therapist-frontend/app/page.tsx
    git commit -m "⚛️ Add basic Next.js frontend

- Create main page component with health check
- Add responsive design with Tailwind CSS
- Display backend connection status
- Show service URLs for development"
fi

# Create layout.tsx for frontend
if [ ! -f "omani-therapist-frontend/app/layout.tsx" ]; then
    cat > omani-therapist-frontend/app/layout.tsx << 'EOF'
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Therapist Assistant',
  description: 'AI-Powered Therapy Assistant',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  )
}
EOF
    git add omani-therapist-frontend/app/layout.tsx
    git commit -m "🎨 Add Next.js layout component

- Create root layout with Inter font
- Configure metadata for SEO
- Set up global CSS imports
- Establish basic page structure"
fi

# Create globals.css for frontend
if [ ! -f "omani-therapist-frontend/app/globals.css" ]; then
    cat > omani-therapist-frontend/app/globals.css << 'EOF'
@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --foreground-rgb: 0, 0, 0;
  --background-start-rgb: 214, 219, 220;
  --background-end-rgb: 255, 255, 255;
}

@media (prefers-color-scheme: dark) {
  :root {
    --foreground-rgb: 255, 255, 255;
    --background-start-rgb: 0, 0, 0;
    --background-end-rgb: 0, 0, 0;
  }
}

body {
  color: rgb(var(--foreground-rgb));
  background: linear-gradient(
      to bottom,
      transparent,
      rgb(var(--background-end-rgb))
    )
    rgb(var(--background-start-rgb));
}
EOF
    git add omani-therapist-frontend/app/globals.css
    git commit -m "🎨 Add global CSS styles

- Configure Tailwind CSS imports
- Set up CSS variables for theming
- Add dark mode support
- Create responsive background gradients"
fi

# Create tailwind.config.js for frontend
if [ ! -f "omani-therapist-frontend/tailwind.config.js" ]; then
    cat > omani-therapist-frontend/tailwind.config.js << 'EOF'
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-conic':
          'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
      },
    },
  },
  plugins: [],
}
EOF
    git add omani-therapist-frontend/tailwind.config.js
    git commit -m "🎨 Configure Tailwind CSS

- Set up content paths for all components
- Configure custom gradient backgrounds
- Enable responsive design utilities
- Prepare for custom theme extensions"
fi

# Create tsconfig.json for frontend
if [ ! -f "omani-therapist-frontend/tsconfig.json" ]; then
    cat > omani-therapist-frontend/tsconfig.json << 'EOF'
{
  "compilerOptions": {
    "target": "es5",
    "lib": ["dom", "dom.iterable", "es6"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "paths": {
      "@/*": ["./*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
EOF
    git add omani-therapist-frontend/tsconfig.json
    git commit -m "⚙️ Configure TypeScript

- Set up TypeScript compiler options
- Configure module resolution for Next.js
- Enable strict type checking
- Set up path aliases for clean imports"
fi

# Create next.config.js for frontend
if [ ! -f "omani-therapist-frontend/next.config.js" ]; then
    cat > omani-therapist-frontend/next.config.js << 'EOF'
/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    appDir: true,
  },
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:8000/:path*',
      },
    ];
  },
}

module.exports = nextConfig
EOF
    git add omani-therapist-frontend/next.config.js
    git commit -m "⚙️ Configure Next.js

- Enable experimental app directory
- Set up API proxy to backend
- Configure development server settings
- Prepare for production deployment"
fi

# Create postcss.config.js for frontend
if [ ! -f "omani-therapist-frontend/postcss.config.js" ]; then
    cat > omani-therapist-frontend/postcss.config.js << 'EOF'
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
EOF
    git add omani-therapist-frontend/postcss.config.js
    git commit -m "🎨 Configure PostCSS

- Set up Tailwind CSS processing
- Enable autoprefixer for cross-browser compatibility
- Configure CSS optimization pipeline"
fi

echo "✅ Git repository setup complete!"
echo ""
echo "📋 Summary of commits created:"
echo "1. 🎉 Initial project structure and documentation"
echo "2. 📁 Backend directory structure"
echo "3. ⚙️ Frontend environment configuration"
echo "4. 🔧 Backend environment configuration"
echo "5. 📦 Frontend package.json"
echo "6. 🐍 Backend requirements.txt"
echo "7. 🐍 Basic FastAPI backend"
echo "8. ⚛️ Basic Next.js frontend"
echo "9. 🎨 Next.js layout component"
echo "10. 🎨 Global CSS styles"
echo "11. 🎨 Tailwind CSS configuration"
echo "12. ⚙️ TypeScript configuration"
echo "13. ⚙️ Next.js configuration"
echo "14. 🎨 PostCSS configuration"
echo ""
echo "🚀 Next steps:"
echo "1. Run 'cd omani-therapist-frontend && npm install'"
echo "2. Run 'cd omani-therapist-voice && pip install -r requirements.txt'"
echo "3. Start backend: 'cd omani-therapist-voice && python main.py'"
echo "4. Start frontend: 'cd omani-therapist-frontend && npm run dev'"
echo ""
echo "🌐 Access your application:"
echo "- Frontend: http://localhost:3000"
echo "- Backend: http://localhost:8000"
echo "- API Docs: http://localhost:8000/docs" 