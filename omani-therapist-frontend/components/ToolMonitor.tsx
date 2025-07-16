'use client'

import { useState, useEffect, useRef } from 'react'
import { Activity, CheckCircle, AlertCircle, Clock, Brain, Heart, Shield } from 'lucide-react'

interface ToolCall {
  id: string
  toolName: string
  action: string
  timestamp: Date
  status: 'pending' | 'completed' | 'error'
  result?: any
  culturalContext?: any
}

interface ToolMonitorProps {
  toolCalls: ToolCall[]
  language: 'ar' | 'en'
  onToolCall: (toolCall: Omit<ToolCall, 'id' | 'timestamp'>) => void
  onToolResult: (id: string, updates: Partial<ToolCall>) => void
  onConnectionChange: (connected: boolean) => void
}

export default function ToolMonitor({ 
  toolCalls, 
  language, 
  onToolCall, 
  onToolResult, 
  onConnectionChange 
}: ToolMonitorProps) {
  const [isConnected, setIsConnected] = useState(false)
  const [selectedTool, setSelectedTool] = useState<string | null>(null)
  const wsRef = useRef<WebSocket | null>(null)
  const containerRef = useRef<HTMLDivElement>(null)
  const toolsEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    toolsEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [toolCalls])

  useEffect(() => {
    connectToToolsWebSocket()
    return () => {
      if (wsRef.current) {
        wsRef.current.close()
      }
    }
  }, [])

  const connectToToolsWebSocket = () => {
    try {
      const wsUrl = `ws://localhost:8003/ws/tools`
      const ws = new WebSocket(wsUrl)
      
      ws.onopen = () => {
        console.log('✅ Connected to therapeutic tools WebSocket')
        setIsConnected(true)
        onConnectionChange(true)
      }

      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data)
          console.log('🏥 Therapeutic tool message:', data)
          
          if (data.type === 'therapeutic_welcome') {
            console.log('🏥 Welcome message received:', data.message)
          } else if (data.type === 'therapeutic_clinical_log') {
            // Handle clinical logs
            onToolCall({
              toolName: data.tool || 'clinical',
              action: data.action || 'log',
              status: 'completed',
              result: data,
              culturalContext: data.clinical_context
            })
          } else if (data.type === 'therapeutic_crisis_documentation') {
            // Handle crisis documentation
            onToolCall({
              toolName: 'crisis_detection',
              action: 'crisis_detected',
              status: 'completed',
              result: data,
              culturalContext: data.crisis_documentation?.cultural_considerations
            })
          }
        } catch (error) {
          console.error('Error parsing therapeutic tool message:', error)
        }
      }

      ws.onerror = (error) => {
        console.error('❌ Therapeutic tools WebSocket error:', error)
        setIsConnected(false)
        onConnectionChange(false)
      }

      ws.onclose = () => {
        console.log('👋 Therapeutic tools WebSocket disconnected')
        setIsConnected(false)
        onConnectionChange(false)
      }

      wsRef.current = ws
    } catch (error) {
      console.error('Failed to connect to therapeutic tools WebSocket:', error)
    }
  }

  const getToolIcon = (toolName: string) => {
    const icons = {
      crisis_detection: Shield,
      cbt_techniques: Brain,
      emotional_analysis: Heart,
      session_management: Activity,
      clinical: Activity
    }
    const IconComponent = icons[toolName as keyof typeof icons] || Activity
    return <IconComponent className="w-4 h-4" />
  }

  const getToolColor = (toolName: string) => {
    const colors = {
      crisis_detection: 'text-red-600 bg-red-100',
      cbt_techniques: 'text-blue-600 bg-blue-100',
      emotional_analysis: 'text-purple-600 bg-purple-100',
      session_management: 'text-green-600 bg-green-100',
      clinical: 'text-gray-600 bg-gray-100'
    }
    return colors[toolName as keyof typeof colors] || 'text-gray-600 bg-gray-100'
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="w-4 h-4 text-green-500" />
      case 'error':
        return <AlertCircle className="w-4 h-4 text-red-500" />
      case 'pending':
        return <Clock className="w-4 h-4 text-yellow-500 animate-spin" />
      default:
        return <Activity className="w-4 h-4 text-gray-500" />
    }
  }

  const formatToolName = (toolName: string) => {
    const names = {
      ar: {
        crisis_detection: 'كشف الأزمات',
        cbt_techniques: 'تقنيات CBT',
        emotional_analysis: 'تحليل المشاعر',
        session_management: 'إدارة الجلسة',
        clinical: 'سجل طبي'
      },
      en: {
        crisis_detection: 'Crisis Detection',
        cbt_techniques: 'CBT Techniques',
        emotional_analysis: 'Emotional Analysis',
        session_management: 'Session Management',
        clinical: 'Clinical Log'
      }
    }
    return names[language][toolName as keyof typeof names.en] || toolName
  }

  const formatTime = (timestamp: Date) => {
    return timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })
  }

  const texts = {
    ar: {
      title: 'مراقب الأدوات',
      noTools: 'لم يتم استخدام أدوات بعد',
      connectionStatus: 'حالة الاتصال',
      connected: 'متصل',
      disconnected: 'غير متصل',
      clickToView: 'انقر لعرض التفاصيل',
      result: 'النتيجة',
      culturalContext: 'السياق الثقافي'
    },
    en: {
      title: 'Tool Monitor',
      noTools: 'No tools used yet',
      connectionStatus: 'Connection Status',
      connected: 'Connected',
      disconnected: 'Disconnected',
      clickToView: 'Click to view details',
      result: 'Result',
      culturalContext: 'Cultural Context'
    }
  }

  const t = texts[language]

  return (
    <div className="h-full flex flex-col max-h-[500px]" ref={containerRef}>
      {/* Connection Status */}
      <div className="flex items-center justify-between mb-4 p-4 bg-gradient-to-r from-gray-50 to-blue-50 rounded-xl border border-gray-100 flex-shrink-0">
        <span className="text-sm font-medium text-gray-700">{t.connectionStatus}</span>
        <div className="flex items-center space-x-2 rtl:space-x-reverse">
          <div className={`w-3 h-3 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'} animate-pulse shadow-lg`} />
          <span className={`text-sm font-medium ${isConnected ? 'text-green-700' : 'text-red-700'}`}>
            {isConnected ? t.connected : t.disconnected}
          </span>
        </div>
      </div>

      {/* Tools List - Fixed height with scroll */}
      <div className="flex-1 overflow-y-auto space-y-3 max-h-80 pr-2 min-h-0">
        {toolCalls.length === 0 ? (
          <div className="text-center py-12 text-gray-500">
            <Activity className="w-12 h-12 mx-auto mb-4 text-gray-300" />
            <p className="text-sm font-medium">{t.noTools}</p>
            <p className="text-xs text-gray-400 mt-1">Tools will appear here when used</p>
          </div>
        ) : (
          toolCalls.map((toolCall) => (
            <div
              key={toolCall.id}
              id={`tool-${toolCall.id}`}
              className={`bg-white border border-gray-200 rounded-xl p-4 cursor-pointer transition-all duration-200 hover:shadow-lg hover:border-gray-300 ${
                selectedTool === toolCall.id ? 'ring-2 ring-purple-500 shadow-lg' : ''
              }`}
              onClick={() => setSelectedTool(selectedTool === toolCall.id ? null : toolCall.id)}
            >
              {/* Tool Header */}
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center space-x-3 rtl:space-x-reverse">
                  <div className={`p-2 rounded-lg ${getToolColor(toolCall.toolName)}`}>
                    {getToolIcon(toolCall.toolName)}
                  </div>
                  <span className="text-sm font-semibold text-gray-900">
                    {formatToolName(toolCall.toolName)}
                  </span>
                </div>
                <div className="flex items-center space-x-2 rtl:space-x-reverse">
                  {getStatusIcon(toolCall.status)}
                  <span className="text-xs text-gray-500 font-medium">
                    {formatTime(toolCall.timestamp)}
                  </span>
                </div>
              </div>

              {/* Tool Action */}
              <div className="text-sm text-gray-700 mb-3">
                <span className="font-medium text-gray-900">{t.clickToView}:</span> {toolCall.action}
              </div>

              {/* Expanded Details */}
              {selectedTool === toolCall.id && (
                <div className="mt-4 pt-4 border-t border-gray-100 space-y-3">
                  {toolCall.result && (
                    <div>
                      <span className="text-xs font-semibold text-gray-600 uppercase tracking-wide">{t.result}:</span>
                      <div className="text-sm text-gray-700 mt-2 p-3 bg-gray-50 rounded-lg border max-h-32 overflow-y-auto">
                        {typeof toolCall.result === 'object' ? (
                          <pre className="text-xs overflow-x-auto text-gray-800">
                            {JSON.stringify(toolCall.result, null, 2)}
                          </pre>
                        ) : (
                          String(toolCall.result)
                        )}
                      </div>
                    </div>
                  )}
                  
                  {toolCall.culturalContext && (
                    <div>
                      <span className="text-xs font-semibold text-gray-600 uppercase tracking-wide">{t.culturalContext}:</span>
                      <div className="text-sm text-gray-700 mt-2 p-3 bg-blue-50 rounded-lg border border-blue-100 max-h-32 overflow-y-auto">
                        {typeof toolCall.culturalContext === 'object' ? (
                          <pre className="text-xs overflow-x-auto text-blue-800">
                            {JSON.stringify(toolCall.culturalContext, null, 2)}
                          </pre>
                        ) : (
                          String(toolCall.culturalContext)
                        )}
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          ))
        )}
        <div ref={toolsEndRef} />
      </div>

      {/* Quick Actions */}
      {isConnected && (
        <div className="mt-4 pt-4 border-t border-gray-200">
          <div className="grid grid-cols-2 gap-2">
            <button
              onClick={() => {
                if (wsRef.current) {
                  wsRef.current.send(JSON.stringify({ type: 'get_agent_status' }))
                }
              }}
              className="px-3 py-2 text-xs bg-blue-100 text-blue-700 rounded-lg hover:bg-blue-200 transition-colors"
            >
              {language === 'ar' ? 'حالة الوكيل' : 'Agent Status'}
            </button>
            <button
              onClick={() => {
                if (wsRef.current) {
                  wsRef.current.send(JSON.stringify({ type: 'check_crisis_status' }))
                }
              }}
              className="px-3 py-2 text-xs bg-red-100 text-red-700 rounded-lg hover:bg-red-200 transition-colors"
            >
              {language === 'ar' ? 'حالة الأزمة' : 'Crisis Status'}
            </button>
          </div>
        </div>
      )}
    </div>
  )
}

export { ToolMonitor } 