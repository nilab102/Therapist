'use client'

import React, { useState, useEffect } from 'react'
import { ConversationDisplay } from '@/components/ConversationDisplay'
import ToolMonitor from '@/components/ToolMonitor'
import { VoiceInterface } from '@/components/VoiceInterface'
import { LanguageSwitcher } from '@/components/LanguageSwitcher'
import { Heart, Brain, Shield, MessageCircle } from 'lucide-react'
import { useTherapyVoiceClient } from '@/lib/therapyVoiceClient'

interface Message {
  id: string
  type: 'user' | 'assistant' | 'system' | 'error'
  content: string
  timestamp: Date
  isAudio?: boolean
  metadata?: any
}

interface ToolCall {
  id: string
  toolName: string
  action: string
  timestamp: Date
  status: 'pending' | 'completed' | 'error'
  result?: any
  culturalContext?: any
}

export default function TherapistHome() {
  const [language, setLanguage] = useState<'ar' | 'en'>('ar')
  // Remove local messages state
  // const [messages, setMessages] = useState<Message[]>([])
  const [toolCalls, setToolCalls] = useState<ToolCall[]>([])
  // Remove local isConnected state
  // const [isConnected, setIsConnected] = useState(false)
  const [currentAgent, setCurrentAgent] = useState('general_therapy')

  // Use the therapy voice client hook for live conversation
  const {
    messages,
    isConnected,
    isInConversation,
    connect,
    disconnect,
    startConversation,
    stopConversation,
    crisisMode,
  } = useTherapyVoiceClient()

  // Add a test message to verify conversation display is working
  useEffect(() => {
    // Add a welcome message after a short delay to test the UI
    const timer = setTimeout(() => {
      if (messages.length === 0) {
        console.log('🏥 Adding test message to verify conversation display')
        // The test message will be added by the hook when connection is established
      }
    }, 1000)
    
    return () => clearTimeout(timer)
  }, [messages.length])

  // Debug logging for messages
  useEffect(() => {
    console.log('🏥 Messages updated:', messages.length, 'messages')
    if (messages.length > 0) {
      console.log('🏥 Latest message:', messages[messages.length - 1])
    }
  }, [messages])

  // Remove local addMessage and setMessages logic

  const addMessage = (message: Omit<Message, 'id' | 'timestamp'>) => {
    const newMessage: Message = {
      ...message,
      id: `msg_${Date.now()}_${Math.random()}`,
      timestamp: new Date()
    }
    // setMessages(prev => [...prev, newMessage]) // This line is removed as per the edit hint
  }

  const addToolCall = (toolCall: Omit<ToolCall, 'id' | 'timestamp'>) => {
    const newToolCall: ToolCall = {
      ...toolCall,
      id: `tool_${Date.now()}_${Math.random()}`,
      timestamp: new Date()
    }
    setToolCalls(prev => [...prev, newToolCall])
  }

  const updateToolCall = (id: string, updates: Partial<ToolCall>) => {
    setToolCalls(prev => prev.map(call => 
      call.id === id ? { ...call, ...updates } : call
    ))
  }

  const texts = {
    ar: {
      title: 'المعالج النفسي العُماني',
      subtitle: 'حمزة - مساعد العلاج النفسي الذكي',
      description: 'علاج نفسي متقدم بالذكاء الاصطناعي مع الحساسية الثقافية العُمانية والإسلامية',
      features: {
        conversation: 'المحادثة العلاجية',
        tools: 'الأدوات المستخدمة',
        voice: 'التفاعل الصوتي',
        cultural: 'الحساسية الثقافية'
      },
      status: {
        connected: 'متصل',
        disconnected: 'غير متصل',
        agent: 'النوع: '
      }
    },
    en: {
      title: 'OMANI Therapist Voice',
      subtitle: 'Nabil - Your AI Therapeutic Assistant',
      description: 'Advanced AI therapy with Omani cultural sensitivity and Islamic integration',
      features: {
        conversation: 'Therapeutic Conversation',
        tools: 'Tools Used',
        voice: 'Voice Interaction',
        cultural: 'Cultural Sensitivity'
      },
      status: {
        connected: 'Connected',
        disconnected: 'Disconnected',
        agent: 'Agent: '
      }
    }
  }

  const t = texts[language]

  const getAgentDisplayName = (agent: string) => {
    const names = {
      ar: {
        general_therapy: 'المعالج العام',
        crisis_intervention: 'التدخل في الأزمات',
        cbt_specialist: 'أخصائي العلاج المعرفي'
      },
      en: {
        general_therapy: 'General Therapist',
        crisis_intervention: 'Crisis Intervention',
        cbt_specialist: 'CBT Specialist'
      }
    }
    return names[language][agent as keyof typeof names.en] || agent
  }

  return (
    <div className={`min-h-screen bg-gradient-to-br from-blue-50 via-green-50 to-teal-50 ${language === 'ar' ? 'rtl' : 'ltr'}`}>
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-sm border-b border-blue-100 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center space-x-4 rtl:space-x-reverse">
              <div className="flex items-center space-x-2 rtl:space-x-reverse">
                <Heart className="w-8 h-8 text-rose-500" />
                <Brain className="w-8 h-8 text-blue-500" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">{t.title}</h1>
                <p className="text-sm text-gray-600">{t.subtitle}</p>
              </div>
            </div>
            
            <div className="flex items-center space-x-4 rtl:space-x-reverse">
              {/* Connection Status */}
              <div className="flex items-center space-x-2 rtl:space-x-reverse">
                <div className={`w-3 h-3 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'} animate-pulse`} />
                <span className="text-sm font-medium text-gray-700">
                  {isConnected ? t.status.connected : t.status.disconnected}
                </span>
              </div>
              
              {/* Current Agent */}
              <div className="flex items-center space-x-2 rtl:space-x-reverse bg-blue-100 px-3 py-1 rounded-full">
                <Shield className="w-4 h-4 text-blue-600" />
                <span className="text-sm font-medium text-blue-800">
                  {t.status.agent}{getAgentDisplayName(currentAgent)}
                </span>
              </div>
              
              <LanguageSwitcher currentLanguage={language} onLanguageChange={setLanguage} />
            </div>
          </div>
          
          {/* Description */}
          <p className="mt-2 text-gray-600 text-center max-w-2xl mx-auto">
            {t.description}
          </p>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          
          {/* Conversation Area - Takes up 2/4 of the width */}
          <div className="lg:col-span-2 space-y-6">
            {/* Conversation Display */}
            <div className="bg-white rounded-2xl shadow-xl border border-blue-100 overflow-hidden backdrop-blur-sm">
              <div className="bg-gradient-to-r from-blue-500 via-blue-600 to-teal-500 px-6 py-4">
                <div className="flex items-center space-x-3 rtl:space-x-reverse text-white">
                  <MessageCircle className="w-6 h-6" />
                  <h2 className="text-lg font-semibold">{t.features.conversation}</h2>
                </div>
              </div>
              <div className="p-6">
                <ConversationDisplay 
                  messages={messages.filter(m => ['user', 'assistant', 'system', 'error'].includes(m.type)).map(msg => ({
                    id: msg.id,
                    type: msg.type as 'user' | 'assistant' | 'system' | 'error',
                    content: msg.content,
                    timestamp: msg.timestamp,
                    isAudio: msg.isAudio,
                    metadata: {
                      emotionalContext: msg.emotionalContext,
                      culturalContext: msg.culturalContext
                    }
                  }))}
                  language={language}
                  onToolCallClick={(toolId: string) => {
                    // Scroll to tool call in monitor
                    const element = document.getElementById(`tool-${toolId}`)
                    element?.scrollIntoView({ behavior: 'smooth' })
                  }}
                />
              </div>
            </div>

            {/* Voice Interface */}
            <div className="bg-white rounded-2xl shadow-xl border border-green-100 overflow-hidden backdrop-blur-sm">
              <div className="bg-gradient-to-r from-green-500 via-emerald-600 to-teal-500 px-6 py-4">
                <div className="flex items-center space-x-3 rtl:space-x-reverse text-white">
                  <Brain className="w-6 h-6" />
                  <h2 className="text-lg font-semibold">{t.features.voice}</h2>
                </div>
              </div>
              <div className="p-6">
                <VoiceInterface
                  language={language}
                  crisisMode={crisisMode}
                  onCrisisDetected={() => {
                    setCurrentAgent('crisis_intervention')
                  }}
                  // Pass connection functions from the main hook
                  connect={connect}
                  disconnect={disconnect}
                  startConversation={startConversation}
                  stopConversation={stopConversation}
                  isConnected={isConnected}
                  isInConversation={isInConversation}
                />
              </div>
            </div>
          </div>

          {/* Tools Monitor - Takes up 2/4 of the width */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-2xl shadow-xl border border-purple-100 overflow-hidden backdrop-blur-sm h-[500px]">
              <div className="bg-gradient-to-r from-purple-500 via-indigo-600 to-blue-500 px-6 py-4">
                <div className="flex items-center space-x-3 rtl:space-x-reverse text-white">
                  <Shield className="w-6 h-6" />
                  <h2 className="text-lg font-semibold">{t.features.tools}</h2>
                </div>
              </div>
              <div className="p-6 h-full">
                <ToolMonitor
                  toolCalls={toolCalls}
                  language={language}
                  onToolCall={addToolCall}
                  onToolResult={updateToolCall}
                  onConnectionChange={() => {}}
                />
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* Cultural Features Footer */}
      <footer className="mt-12 bg-white/50 backdrop-blur-sm border-t border-blue-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex justify-center items-center space-x-8 rtl:space-x-reverse text-gray-600">
            <div className="flex items-center space-x-2 rtl:space-x-reverse">
              <Heart className="w-5 h-5 text-rose-500" />
              <span className="text-sm">{language === 'ar' ? 'علاج نفسي آمن' : 'Safe Therapy'}</span>
            </div>
            <div className="flex items-center space-x-2 rtl:space-x-reverse">
              <Shield className="w-5 h-5 text-blue-500" />
              <span className="text-sm">{language === 'ar' ? 'حماية البيانات' : 'Data Protection'}</span>
            </div>
            <div className="flex items-center space-x-2 rtl:space-x-reverse">
              <Brain className="w-5 h-5 text-green-500" />
              <span className="text-sm">{language === 'ar' ? 'ذكاء اصطناعي' : 'AI Powered'}</span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
} 