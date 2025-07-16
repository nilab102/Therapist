'use client'

import React, { useEffect, useRef, useState } from 'react'
import { useEnhancedTherapyClient, ConversationMessage, ToolCall, ToolResult } from '@/lib/enhancedTherapyClient'

interface EnhancedConversationDisplayProps {
  language: 'ar' | 'en'
}

export function EnhancedConversationDisplay({ language }: EnhancedConversationDisplayProps) {
  const {
    messages,
    activeToolCalls,
    recentToolResults,
    isConversationConnected,
    isToolsConnected,
    isInConversation,
    connectionStatus,
    connect,
    disconnect,
    startConversation,
    stopConversation,
    saveConversation,
    clearConversation,
    exportConversation
  } = useEnhancedTherapyClient()
  
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const [selectedToolResult, setSelectedToolResult] = useState<ToolResult | null>(null)
  
  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])
  
  // Auto-connect on mount
  useEffect(() => {
    connect()
    return () => disconnect()
  }, [connect, disconnect])
  
  const formatTime = (timestamp: Date) => {
    return new Date(timestamp).toLocaleTimeString(language === 'ar' ? 'ar-OM' : 'en-US', {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    })
  }
  
  const getMessageClass = (message: ConversationMessage) => {
    const baseClass = "rounded-xl p-4 mb-4 shadow-md border-2 transition-all duration-200 hover:shadow-lg max-w-4xl"
    
    switch (message.type) {
      case 'user':
        return `${baseClass} bg-blue-600 border-blue-700 text-white ml-8 mr-2`
      case 'assistant':
        return `${baseClass} bg-emerald-600 border-emerald-700 text-white mr-8 ml-2`
      case 'system':
        return `${baseClass} bg-gray-600 border-gray-700 text-white mx-4`
      case 'error':
        return `${baseClass} bg-red-600 border-red-700 text-white mx-4`
      case 'tool_call':
        return `${baseClass} bg-orange-600 border-orange-700 text-white mx-4`
      case 'tool_result':
        return `${baseClass} bg-purple-600 border-purple-700 text-white mx-4`
      default:
        return `${baseClass} bg-slate-600 border-slate-700 text-white mx-4`
    }
  }
  
  const getSpeakerLabel = (message: ConversationMessage) => {
    switch (message.type) {
      case 'user':
        return language === 'ar' ? 'المستخدم ←' : 'User -->'
      case 'assistant':
        return language === 'ar' ? 'المعالج ←' : 'Therapist -->'
      case 'system':
        return language === 'ar' ? 'النظام ←' : 'System -->'
      case 'error':
        return language === 'ar' ? 'خطأ ←' : 'Error -->'
      case 'tool_call':
        return language === 'ar' ? 'استدعاء أداة ←' : 'Tool Call -->'
      case 'tool_result':
        return language === 'ar' ? 'نتيجة الأداة ←' : 'Tool Result -->'
      default:
        return language === 'ar' ? 'رسالة ←' : 'Message -->'
    }
  }
  
  const getMessageIcon = (message: ConversationMessage) => {
    switch (message.type) {
      case 'user':
        return message.isAudio ? '🎤' : '👤'
      case 'assistant':
        return '🏥'
      case 'system':
        return '⚙️'
      case 'error':
        return '❌'
      case 'tool_call':
        return '🔧'
      case 'tool_result':
        return '✅'
      default:
        return '📝'
    }
  }
  
  const renderToolCallDetails = (toolCall: ToolCall) => (
    <div className="mt-3 p-3 bg-white bg-opacity-20 rounded-lg border border-white border-opacity-30">
      <div className="text-sm font-medium text-white">
        🔧 Tool: {toolCall.toolName} | Action: {toolCall.action}
      </div>
      <div className="text-xs text-white text-opacity-90 mt-1">
        Status: <span className={`px-2 py-1 rounded ${
          toolCall.status === 'completed' ? 'bg-green-500 text-white' :
          toolCall.status === 'failed' ? 'bg-red-500 text-white' :
          'bg-yellow-500 text-black'
        }`}>
          {toolCall.status}
        </span>
      </div>
      {Object.keys(toolCall.parameters).length > 0 && (
        <details className="mt-2">
          <summary className="text-xs cursor-pointer text-white text-opacity-90 hover:text-white">
            View Parameters
          </summary>
          <pre className="text-xs mt-1 p-2 bg-white bg-opacity-90 text-black rounded border overflow-x-auto">
            {JSON.stringify(toolCall.parameters, null, 2)}
          </pre>
        </details>
      )}
    </div>
  )
  
  const renderToolResultDetails = (toolResult: ToolResult) => (
    <div className="mt-3 p-3 bg-white bg-opacity-20 rounded-lg border border-white border-opacity-30">
      <div className="text-sm font-medium text-white">
        ✅ {toolResult.displayData?.title || `${toolResult.toolName} Result`}
      </div>
      <div className="text-sm text-white text-opacity-90 mt-1">
        {toolResult.displayData?.summary || 'Tool completed successfully'}
      </div>
      
      {toolResult.displayData?.details && Object.keys(toolResult.displayData.details).length > 0 && (
        <div className="mt-2">
          <button
            onClick={() => setSelectedToolResult(toolResult)}
            className="text-xs bg-white bg-opacity-90 text-purple-700 px-3 py-1 rounded hover:bg-white transition-colors font-medium"
          >
            View Details
          </button>
        </div>
      )}
      
      <div className="text-xs text-white text-opacity-80 mt-2">
        Completed: {formatTime(toolResult.timestamp)}
      </div>
    </div>
  )
  
  const texts = {
    ar: {
      title: 'سجل المحادثة المحسن',
      noMessages: 'لم تبدأ المحادثة بعد',
      startPrompt: 'اضغط "ابدأ المحادثة" لبدء جلسة العلاج',
      connectionStatus: 'حالة الاتصال',
      conversationSystem: 'نظام المحادثة',
      toolSystem: 'نظام الأدوات',
      connected: 'متصل',
      disconnected: 'منقطع',
      listening: 'يستمع...',
      startConversation: 'ابدأ المحادثة',
      stopConversation: 'أوقف المحادثة',
      saveConversation: 'احفظ المحادثة',
      clearConversation: 'امسح المحادثة',
      exportConversation: 'صدر المحادثة',
      toolCalls: 'استدعاءات الأدوات',
      activeTools: 'الأدوات النشطة',
      recentResults: 'النتائج الحديثة',
      you: 'أنت',
      therapist: 'المعالج',
      toolCall: 'استدعاء أداة',
      toolResult: 'نتيجة الأداة'
    },
    en: {
      title: 'Enhanced Conversation History',
      noMessages: 'No messages yet',
      startPrompt: 'Click "Start Conversation" to begin therapy session',
      connectionStatus: 'Connection Status',
      conversationSystem: 'Conversation System',
      toolSystem: 'Tool System',
      connected: 'Connected',
      disconnected: 'Disconnected',
      listening: 'Listening...',
      startConversation: 'Start Conversation',
      stopConversation: 'Stop Conversation',
      saveConversation: 'Save Conversation',
      clearConversation: 'Clear Conversation',
      exportConversation: 'Export Conversation',
      toolCalls: 'Tool Calls',
      activeTools: 'Active Tools',
      recentResults: 'Recent Results',
      you: 'You',
      therapist: 'Therapist',
      toolCall: 'Tool Call',
      toolResult: 'Tool Result'
    }
  }
  
  const currentTexts = texts[language]
  
  return (
    <div className="therapy-card max-w-4xl mx-auto">
      <div className="flex items-center justify-between mb-4">
        <h3 className={`text-xl font-bold text-therapy-text ${language === 'ar' ? 'arabic-text' : 'english-text'}`}>
          {currentTexts.title}
        </h3>
        <div className="flex items-center space-x-2">
          {/* Connection Status Indicators */}
          <div className="text-xs bg-white rounded-lg p-2 shadow-sm border">
            <div className="flex items-center space-x-2 mb-1">
              <span>{currentTexts.conversationSystem}:</span>
              <div className={`w-2 h-2 rounded-full ${isConversationConnected ? 'bg-green-500' : 'bg-red-500'}`}></div>
              <span className={isConversationConnected ? 'text-green-600' : 'text-red-600'}>
                {isConversationConnected ? currentTexts.connected : currentTexts.disconnected}
              </span>
            </div>
            <div className="flex items-center space-x-2">
              <span>{currentTexts.toolSystem}:</span>
              <div className={`w-2 h-2 rounded-full ${isToolsConnected ? 'bg-green-500' : 'bg-red-500'}`}></div>
              <span className={isToolsConnected ? 'text-green-600' : 'text-red-600'}>
                {isToolsConnected ? currentTexts.connected : currentTexts.disconnected}
              </span>
            </div>
          </div>
          
          {isInConversation && (
            <div className="text-xs bg-blue-100 text-blue-800 px-3 py-2 rounded-lg border border-blue-200 animate-pulse">
              🎤 {currentTexts.listening}
            </div>
          )}
        </div>
      </div>
      
      {/* Control Buttons */}
      <div className="flex flex-wrap gap-2 mb-4">
        <button
          onClick={isInConversation ? stopConversation : startConversation}
          className={`px-4 py-2 text-white rounded-lg font-medium transition-colors ${
            isInConversation 
              ? 'bg-red-500 hover:bg-red-600' 
              : 'bg-green-500 hover:bg-green-600'
          }`}
        >
          {isInConversation ? currentTexts.stopConversation : currentTexts.startConversation}
        </button>
        
        <button
          onClick={saveConversation}
          className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors font-medium"
        >
          {currentTexts.saveConversation}
        </button>
        
        <button
          onClick={clearConversation}
          className="px-4 py-2 bg-orange-500 text-white rounded-lg hover:bg-orange-600 transition-colors font-medium"
        >
          {currentTexts.clearConversation}
        </button>
        
        <button
          onClick={() => {
            const data = exportConversation()
            if (data) {
              const blob = new Blob([data], { type: 'application/json' })
              const url = URL.createObjectURL(blob)
              const a = document.createElement('a')
              a.href = url
              a.download = `therapy-conversation-${Date.now()}.json`
              a.click()
              URL.revokeObjectURL(url)
            }
          }}
          className="px-4 py-2 bg-purple-500 text-white rounded-lg hover:bg-purple-600 transition-colors font-medium"
        >
          {currentTexts.exportConversation}
        </button>
      </div>
      
      {/* Messages Display */}
      <div className="max-h-96 overflow-y-auto border-2 border-gray-200 rounded-xl bg-gradient-to-b from-gray-50 to-gray-100 shadow-inner">
        {messages.length === 0 ? (
          <div className={`text-center text-gray-600 py-8 ${language === 'ar' ? 'arabic-text' : 'english-text'}`}>
            <div className="text-6xl mb-4">💬</div>
            <p className="mb-2 font-semibold text-lg">{currentTexts.noMessages}</p>
            <p className="text-sm text-gray-500">{currentTexts.startPrompt}</p>
          </div>
        ) : (
          <div className="p-4">
            {messages.map((message, index) => (
              <div key={message.id} className={getMessageClass(message)}>
                {/* Speaker Label - Large and Prominent */}
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center space-x-3">
                    <div className="text-3xl">
                      {getMessageIcon(message)}
                    </div>
                    <div className="text-lg font-bold text-white">
                      {getSpeakerLabel(message)}
                    </div>
                  </div>
                  <div className="flex items-center space-x-2">
                    {message.isAudio && (
                      <span className="text-xs bg-white bg-opacity-20 text-white px-2 py-1 rounded-full border border-white border-opacity-30">
                        🎤 Audio
                      </span>
                    )}
                    
                    {message.type === 'tool_call' && (
                      <span className="text-xs bg-white bg-opacity-20 text-white px-2 py-1 rounded-full border border-white border-opacity-30">
                        🔧 Tool Active
                      </span>
                    )}
                    
                    {message.type === 'tool_result' && (
                      <span className="text-xs bg-white bg-opacity-20 text-white px-2 py-1 rounded-full border border-white border-opacity-30">
                        ✅ Result
                      </span>
                    )}
                    
                    <span className="text-xs text-white text-opacity-80 font-mono bg-white bg-opacity-10 px-2 py-1 rounded">
                      {formatTime(message.timestamp)}
                    </span>
                  </div>
                </div>
                
                {/* Message Content */}
                <div className="prose prose-sm max-w-none">
                  <div className="text-white leading-relaxed text-base font-medium">
                    {message.content}
                  </div>
                </div>
                
                {/* Tool Call Details */}
                {message.toolCall && renderToolCallDetails(message.toolCall)}
                
                {/* Tool Result Details */}
                {message.toolResult && renderToolResultDetails(message.toolResult)}
                
                {/* Context Tags */}
                <div className="flex flex-wrap gap-2 mt-3">
                  {message.emotionalContext && (
                    <span className="text-xs bg-white bg-opacity-20 text-white px-2 py-1 rounded-full border border-white border-opacity-30">
                      💭 {message.emotionalContext}
                    </span>
                  )}
                  
                  {message.culturalContext && (
                    <span className="text-xs bg-white bg-opacity-20 text-white px-2 py-1 rounded-full border border-white border-opacity-30">
                      🌍 {message.culturalContext}
                    </span>
                  )}
                </div>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>
      
      {/* Tool Results Modal */}
      {selectedToolResult && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl p-6 max-w-2xl w-full max-h-96 overflow-y-auto shadow-2xl">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-bold text-gray-800">
                {selectedToolResult.displayData?.title || `${selectedToolResult.toolName} Details`}
              </h3>
              <button
                onClick={() => setSelectedToolResult(null)}
                className="text-gray-500 hover:text-gray-700 text-2xl"
              >
                ×
              </button>
            </div>
            <div className="prose prose-sm max-w-none">
              <p className="text-gray-700 mb-4">
                {selectedToolResult.displayData?.summary}
              </p>
              {selectedToolResult.displayData?.details && (
                <pre className="bg-gray-100 p-4 rounded-lg overflow-x-auto text-sm">
                  {JSON.stringify(selectedToolResult.displayData.details, null, 2)}
                </pre>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  )
} 