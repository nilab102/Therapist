'use client'

import { useEffect, useRef } from 'react'
import { User, Bot, AlertTriangle, Info, Mic, Volume2 } from 'lucide-react'

interface Message {
  id: string
  type: 'user' | 'assistant' | 'system' | 'error'
  content: string
  timestamp: Date
  isAudio?: boolean
  metadata?: any
}

interface ConversationDisplayProps {
  messages: Message[]
  language: 'ar' | 'en'
  onToolCallClick?: (toolId: string) => void
}

export default function ConversationDisplay({ 
  messages, 
  language, 
  onToolCallClick 
}: ConversationDisplayProps) {
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const formatTime = (timestamp: Date) => {
    return timestamp.toLocaleTimeString([], { 
      hour: '2-digit', 
      minute: '2-digit'
    })
  }

  const getMessageIcon = (type: string, isAudio?: boolean) => {
    if (isAudio && type === 'user') {
      return <Mic className="w-4 h-4" />
    }
    
    if (isAudio && type === 'assistant') {
      return <Volume2 className="w-4 h-4" />
    }
    
    switch (type) {
      case 'user':
        return <User className="w-5 h-5" />
      case 'assistant':
        return <Bot className="w-5 h-5" />
      case 'system':
        return <Info className="w-4 h-4" />
      case 'error':
        return <AlertTriangle className="w-4 h-4" />
      default:
        return <Bot className="w-5 h-5" />
    }
  }

  const getMessageStyles = (type: string) => {
    switch (type) {
      case 'user':
        return {
          container: `ml-auto max-w-xs lg:max-w-md ${language === 'ar' ? 'mr-0 ml-auto' : 'ml-auto mr-0'}`,
          bubble: 'bg-gradient-to-r from-blue-500 to-blue-600 text-white shadow-lg',
          icon: 'bg-blue-100 text-blue-600'
        }
      case 'assistant':
        return {
          container: `mr-auto max-w-xs lg:max-w-md ${language === 'ar' ? 'ml-0 mr-auto' : 'mr-auto ml-0'}`,
          bubble: 'bg-gradient-to-r from-emerald-500 to-green-600 text-white shadow-lg',
          icon: 'bg-emerald-100 text-emerald-600'
        }
      case 'system':
        return {
          container: 'mx-auto max-w-sm',
          bubble: 'bg-gray-100 text-gray-700 text-center text-sm shadow-sm',
          icon: 'bg-gray-100 text-gray-500'
        }
      case 'error':
        return {
          container: 'mx-auto max-w-sm',
          bubble: 'bg-red-100 text-red-800 text-center shadow-sm',
          icon: 'bg-red-100 text-red-600'
        }
      default:
        return {
          container: 'mr-auto max-w-xs lg:max-w-md',
          bubble: 'bg-gray-100 text-gray-800 shadow-sm',
          icon: 'bg-gray-100 text-gray-600'
        }
    }
  }

  const renderMessageContent = (message: Message) => {
    const content = message.content

    // Check if content contains tool references
    if (content.includes('🔧') && onToolCallClick) {
      const parts = content.split(/(🔧[^:]+:[^🔧]+)/g)
      return parts.map((part, index) => {
        if (part.startsWith('🔧')) {
          return (
            <span
              key={index}
              className="inline-block bg-purple-100 text-purple-800 px-2 py-1 rounded-md text-xs cursor-pointer hover:bg-purple-200 transition-colors mx-1"
              onClick={() => onToolCallClick && onToolCallClick(`tool_${index}`)}
            >
              {part}
            </span>
          )
        }
        return <span key={index}>{part}</span>
      })
    }

    return content
  }

  const texts = {
    ar: {
      noMessages: 'لا توجد رسائل بعد',
      startConversation: 'ابدأ محادثة بالتسجيل أو الكتابة',
      user: 'أنت',
      assistant: 'حمزة (المعالج)',
      system: 'النظام',
      audioMessage: 'رسالة صوتية'
    },
    en: {
      noMessages: 'No messages yet',
      startConversation: 'Start a conversation by recording or typing',
      user: 'You',
      assistant: 'Nabil (Therapist)',
      system: 'System',
      audioMessage: 'Audio message'
    }
  }

  const t = texts[language]

  if (messages.length === 0) {
    return (
      <div className="h-64 flex items-center justify-center text-gray-500 bg-gradient-to-br from-blue-50 to-green-50 rounded-xl border border-gray-100">
        <div className="text-center p-8">
          <Bot className="w-16 h-16 mx-auto mb-4 text-gray-300" />
          <h3 className="text-lg font-semibold text-gray-700 mb-2">{t.noMessages}</h3>
          <p className="text-sm text-gray-500">{t.startConversation}</p>
          <div className="mt-6 flex justify-center space-x-6 rtl:space-x-reverse">
            <div className="flex items-center space-x-2 rtl:space-x-reverse text-xs text-gray-400">
              <Mic className="w-4 h-4" />
              <span className="font-medium">{language === 'ar' ? 'صوت' : 'Voice'}</span>
            </div>
            <div className="flex items-center space-x-2 rtl:space-x-reverse text-xs text-gray-400">
              <Bot className="w-4 h-4" />
              <span className="font-medium">{language === 'ar' ? 'ذكي' : 'AI'}</span>
            </div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="h-64 overflow-y-auto space-y-4 p-4 bg-gradient-to-br from-blue-50/30 to-green-50/30 rounded-xl border border-gray-100 pr-2">
      {messages.map((message) => {
        const styles = getMessageStyles(message.type)
        
        return (
          <div key={message.id} className={`flex items-start space-x-3 rtl:space-x-reverse ${styles.container}`}>
            {/* Avatar */}
            <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${styles.icon} shadow-sm`}>
              {getMessageIcon(message.type, message.isAudio)}
            </div>
            
            {/* Message Bubble */}
            <div className="flex-1 min-w-0">
              {/* Speaker Name */}
              {message.type !== 'system' && (
                <div className="text-xs text-gray-500 mb-2 px-1 font-medium">
                  {message.type === 'user' ? t.user : 
                   message.type === 'assistant' ? t.assistant : 
                   t.system}
                  {message.isAudio && (
                    <span className="ml-2 rtl:ml-0 rtl:mr-2 text-gray-400">
                      ({t.audioMessage})
                    </span>
                  )}
                </div>
              )}
              
              {/* Message Content */}
              <div className={`px-4 py-3 rounded-2xl ${styles.bubble}`}>
                <div className="text-sm whitespace-pre-wrap break-words leading-relaxed">
                  {renderMessageContent(message)}
                </div>
              </div>
              
              {/* Timestamp */}
              <div className="text-xs text-gray-400 mt-1 px-1">
                {formatTime(message.timestamp)}
              </div>
            </div>
          </div>
        )
      })}
      
      {/* Scroll anchor */}
      <div ref={messagesEndRef} />
    </div>
  )
}

export { ConversationDisplay } 