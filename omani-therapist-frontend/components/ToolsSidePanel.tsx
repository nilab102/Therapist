'use client'

import React, { useState } from 'react'
import { ToolCall, ToolResult } from '@/lib/enhancedTherapyClient'

interface ToolsSidePanelProps {
  activeToolCalls: ToolCall[]
  recentToolResults: ToolResult[]
  isToolsConnected: boolean
  language: 'ar' | 'en'
  onSendToolCommand?: (command: any) => void
}

export function ToolsSidePanel({ 
  activeToolCalls, 
  recentToolResults, 
  isToolsConnected, 
  language,
  onSendToolCommand 
}: ToolsSidePanelProps) {
  const [selectedTab, setSelectedTab] = useState<'active' | 'results' | 'test'>('active')
  const [selectedResult, setSelectedResult] = useState<ToolResult | null>(null)
  
  const texts = {
    ar: {
      title: 'لوحة الأدوات',
      activeCalls: 'الاستدعاءات النشطة',
      recentResults: 'النتائج الحديثة',
      testTools: 'اختبار الأدوات',
      noActiveCalls: 'لا توجد أدوات نشطة',
      noResults: 'لا توجد نتائج حديثة',
      toolName: 'اسم الأداة',
      action: 'الإجراء',
      status: 'الحالة',
      timestamp: 'الوقت',
      parameters: 'المعاملات',
      result: 'النتيجة',
      success: 'نجح',
      failed: 'فشل',
      completed: 'مكتمل',
      pending: 'معلق',
      executing: 'قيد التنفيذ',
      viewDetails: 'عرض التفاصيل',
      close: 'إغلاق',
      testCbtTool: 'اختبار أداة العلاج المعرفي',
      testCrisisTool: 'اختبار أداة الأزمة',
      testEmotionTool: 'اختبار أداة التحليل العاطفي',
      testSessionTool: 'اختبار أداة الجلسة',
      connectionStatus: 'حالة الاتصال',
      connected: 'متصل',
      disconnected: 'منقطع'
    },
    en: {
      title: 'Tools Panel',
      activeCalls: 'Active Calls',
      recentResults: 'Recent Results',
      testTools: 'Test Tools',
      noActiveCalls: 'No active tool calls',
      noResults: 'No recent results',
      toolName: 'Tool Name',
      action: 'Action',
      status: 'Status',
      timestamp: 'Timestamp',
      parameters: 'Parameters',
      result: 'Result',
      success: 'Success',
      failed: 'Failed',
      completed: 'Completed',
      pending: 'Pending',
      executing: 'Executing',
      viewDetails: 'View Details',
      close: 'Close',
      testCbtTool: 'Test CBT Tool',
      testCrisisTool: 'Test Crisis Tool',
      testEmotionTool: 'Test Emotion Tool',
      testSessionTool: 'Test Session Tool',
      connectionStatus: 'Connection Status',
      connected: 'Connected',
      disconnected: 'Disconnected'
    }
  }
  
  const currentTexts = texts[language]
  
  const formatTime = (timestamp: Date) => {
    return new Date(timestamp).toLocaleTimeString(language === 'ar' ? 'ar-OM' : 'en-US', {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    })
  }
  
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-800 border-green-200'
      case 'failed':
        return 'bg-red-100 text-red-800 border-red-200'
      case 'executing':
        return 'bg-blue-100 text-blue-800 border-blue-200'
      case 'pending':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200'
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200'
    }
  }
  
  const getStatusText = (status: string) => {
    switch (status) {
      case 'completed':
        return currentTexts.completed
      case 'failed':
        return currentTexts.failed
      case 'executing':
        return currentTexts.executing
      case 'pending':
        return currentTexts.pending
      default:
        return status
    }
  }
  
  const getToolDisplayName = (toolName: string) => {
    const toolNames: Record<string, { ar: string, en: string }> = {
      'crisis_detection': { ar: 'كشف الأزمة', en: 'Crisis Detection' },
      'cbt_techniques': { ar: 'تقنيات العلاج المعرفي', en: 'CBT Techniques' },
      'emotional_analysis': { ar: 'التحليل العاطفي', en: 'Emotional Analysis' },
      'session_management': { ar: 'إدارة الجلسة', en: 'Session Management' }
    }
    
    return toolNames[toolName]?.[language] || toolName
  }
  
  const sendTestCommand = (toolType: string) => {
    if (!onSendToolCommand) return
    
    const testCommands = {
      cbt: {
        type: 'test_cbt_tool',
        tool: 'cbt_techniques',
        action: 'apply_cbt_technique',
        data: {
          technique: 'thought_challenging',
          user_thoughts: 'I feel like everything is going wrong',
          mood_rating: 4,
          cultural_context: {
            religious_integration: true,
            arabic_preferred: language === 'ar'
          }
        }
      },
      crisis: {
        type: 'test_crisis_tool',
        tool: 'crisis_detection',
        action: 'assess_risk',
        data: {
          user_input: 'I feel hopeless sometimes',
          risk_factors: ['hopelessness', 'social_isolation'],
          urgency_level: 'moderate'
        }
      },
      emotion: {
        type: 'test_emotion_tool',
        tool: 'emotional_analysis',
        action: 'detect_emotions',
        data: {
          user_input: 'I am feeling sad and worried about my future',
          cultural_context: {
            arabic_language_used: language === 'ar',
            religious_expressions: true
          }
        }
      },
      session: {
        type: 'test_session_tool',
        tool: 'session_management',
        action: 'manage_session',
        data: {
          action: 'start_session',
          preferences: {
            language: language,
            culturalContext: 'gulf_arabic'
          }
        }
      }
    }
    
    const command = testCommands[toolType as keyof typeof testCommands]
    if (command) {
      onSendToolCommand(command)
    }
  }
  
  const renderActiveToolCalls = () => (
    <div className="space-y-3">
      {activeToolCalls.length === 0 ? (
        <div className="text-center text-gray-500 py-8">
          <div className="text-4xl mb-2">🔧</div>
          <p>{currentTexts.noActiveCalls}</p>
        </div>
      ) : (
        activeToolCalls.map((toolCall) => (
          <div key={toolCall.id} className="bg-white border rounded-lg p-4 shadow-sm">
            <div className="flex items-center justify-between mb-3">
              <h4 className="font-medium text-gray-800">
                {getToolDisplayName(toolCall.toolName)}
              </h4>
              <span className={`px-2 py-1 text-xs rounded border ${getStatusColor(toolCall.status)}`}>
                {getStatusText(toolCall.status)}
              </span>
            </div>
            
            <div className="text-sm text-gray-600 mb-2">
              <span className="font-medium">{currentTexts.action}:</span> {toolCall.action}
            </div>
            
            <div className="text-xs text-gray-500 mb-3">
              {formatTime(toolCall.timestamp)}
            </div>
            
            {Object.keys(toolCall.parameters).length > 0 && (
              <details className="mt-2">
                <summary className="text-xs cursor-pointer text-blue-600 hover:text-blue-800">
                  {currentTexts.parameters}
                </summary>
                <pre className="text-xs mt-2 p-2 bg-gray-100 rounded overflow-x-auto">
                  {JSON.stringify(toolCall.parameters, null, 2)}
                </pre>
              </details>
            )}
          </div>
        ))
      )}
    </div>
  )
  
  const renderRecentResults = () => (
    <div className="space-y-3">
      {recentToolResults.length === 0 ? (
        <div className="text-center text-gray-500 py-8">
          <div className="text-4xl mb-2">📋</div>
          <p>{currentTexts.noResults}</p>
        </div>
      ) : (
        recentToolResults.map((result) => (
          <div key={result.id} className="bg-white border rounded-lg p-4 shadow-sm">
            <div className="flex items-center justify-between mb-3">
              <h4 className="font-medium text-gray-800">
                {getToolDisplayName(result.toolName)}
              </h4>
              <span className={`px-2 py-1 text-xs rounded border ${
                result.success ? 'bg-green-100 text-green-800 border-green-200' : 'bg-red-100 text-red-800 border-red-200'
              }`}>
                {result.success ? currentTexts.success : currentTexts.failed}
              </span>
            </div>
            
            <div className="text-sm text-gray-700 mb-2">
              {result.displayData?.title || `${result.toolName} ${currentTexts.result}`}
            </div>
            
            <div className="text-sm text-gray-600 mb-3">
              {result.displayData?.summary || 'Tool completed successfully'}
            </div>
            
            <div className="flex items-center justify-between">
              <div className="text-xs text-gray-500">
                {formatTime(result.timestamp)}
              </div>
              
              {result.displayData?.details && (
                <button
                  onClick={() => setSelectedResult(result)}
                  className="text-xs bg-blue-500 text-white px-3 py-1 rounded hover:bg-blue-600 transition-colors"
                >
                  {currentTexts.viewDetails}
                </button>
              )}
            </div>
          </div>
        ))
      )}
    </div>
  )
  
  const renderTestTools = () => (
    <div className="space-y-3">
      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-3 mb-4">
        <div className="text-sm text-yellow-800">
          Use these buttons to test tool functionality and see how the system responds to different therapeutic scenarios.
        </div>
      </div>
      
      <button
        onClick={() => sendTestCommand('cbt')}
        disabled={!isToolsConnected}
        className="w-full bg-purple-500 text-white p-3 rounded-lg hover:bg-purple-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
      >
        🧠 {currentTexts.testCbtTool}
      </button>
      
      <button
        onClick={() => sendTestCommand('crisis')}
        disabled={!isToolsConnected}
        className="w-full bg-red-500 text-white p-3 rounded-lg hover:bg-red-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
      >
        🚨 {currentTexts.testCrisisTool}
      </button>
      
      <button
        onClick={() => sendTestCommand('emotion')}
        disabled={!isToolsConnected}
        className="w-full bg-blue-500 text-white p-3 rounded-lg hover:bg-blue-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
      >
        💭 {currentTexts.testEmotionTool}
      </button>
      
      <button
        onClick={() => sendTestCommand('session')}
        disabled={!isToolsConnected}
        className="w-full bg-green-500 text-white p-3 rounded-lg hover:bg-green-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
      >
        🏥 {currentTexts.testSessionTool}
      </button>
    </div>
  )
  
  return (
    <div className="bg-gray-50 border rounded-lg p-4 h-full flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <h3 className={`text-lg font-bold text-gray-800 ${language === 'ar' ? 'arabic-text' : 'english-text'}`}>
          {currentTexts.title}
        </h3>
        <div className={`text-xs px-2 py-1 rounded border ${
          isToolsConnected ? 'bg-green-100 text-green-800 border-green-200' : 'bg-red-100 text-red-800 border-red-200'
        }`}>
          {isToolsConnected ? currentTexts.connected : currentTexts.disconnected}
        </div>
      </div>
      
      {/* Tabs */}
      <div className="flex mb-4 bg-white rounded-lg p-1 border">
        <button
          onClick={() => setSelectedTab('active')}
          className={`flex-1 px-3 py-2 text-sm rounded transition-colors ${
            selectedTab === 'active'
              ? 'bg-blue-500 text-white'
              : 'text-gray-600 hover:text-gray-800'
          }`}
        >
          🔧 {currentTexts.activeCalls} ({activeToolCalls.length})
        </button>
        <button
          onClick={() => setSelectedTab('results')}
          className={`flex-1 px-3 py-2 text-sm rounded transition-colors ${
            selectedTab === 'results'
              ? 'bg-blue-500 text-white'
              : 'text-gray-600 hover:text-gray-800'
          }`}
        >
          📋 {currentTexts.recentResults} ({recentToolResults.length})
        </button>
        <button
          onClick={() => setSelectedTab('test')}
          className={`flex-1 px-3 py-2 text-sm rounded transition-colors ${
            selectedTab === 'test'
              ? 'bg-blue-500 text-white'
              : 'text-gray-600 hover:text-gray-800'
          }`}
        >
          🧪 {currentTexts.testTools}
        </button>
      </div>
      
      {/* Content */}
      <div className="flex-1 overflow-y-auto">
        {selectedTab === 'active' && renderActiveToolCalls()}
        {selectedTab === 'results' && renderRecentResults()}
        {selectedTab === 'test' && renderTestTools()}
      </div>
      
      {/* Result Details Modal */}
      {selectedResult && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-2xl w-full max-h-96 overflow-y-auto">
            <div className="p-6">
              <div className="flex items-center justify-between mb-4">
                <h4 className="text-lg font-bold text-gray-800">
                  {selectedResult.displayData?.title}
                </h4>
                <button
                  onClick={() => setSelectedResult(null)}
                  className="text-gray-500 hover:text-gray-700 text-xl"
                >
                  ✕
                </button>
              </div>
              
              <div className="space-y-4">
                <div>
                  <h5 className="font-medium text-gray-700 mb-2">Summary</h5>
                  <p className="text-gray-600">{selectedResult.displayData?.summary}</p>
                </div>
                
                <div>
                  <h5 className="font-medium text-gray-700 mb-2">Tool Details</h5>
                  <div className="bg-gray-100 p-3 rounded text-sm">
                    <div><strong>Tool:</strong> {getToolDisplayName(selectedResult.toolName)}</div>
                    <div><strong>Action:</strong> {selectedResult.action}</div>
                    <div><strong>Success:</strong> {selectedResult.success ? 'Yes' : 'No'}</div>
                    <div><strong>Time:</strong> {formatTime(selectedResult.timestamp)}</div>
                  </div>
                </div>
                
                <div>
                  <h5 className="font-medium text-gray-700 mb-2">Full Result Data</h5>
                  <pre className="text-sm bg-gray-100 p-3 rounded overflow-x-auto max-h-40">
                    {JSON.stringify(selectedResult.displayData?.details || selectedResult.result, null, 2)}
                  </pre>
                </div>
              </div>
              
              <div className="mt-6 flex justify-end">
                <button
                  onClick={() => setSelectedResult(null)}
                  className="px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600 transition-colors"
                >
                  {currentTexts.close}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
} 