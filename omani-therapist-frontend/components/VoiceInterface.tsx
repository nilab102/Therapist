'use client'

import React, { useState, useCallback } from 'react'
import { useTherapyVoiceClient } from '@/lib/therapyVoiceClient'

interface VoiceInterfaceProps {
  language: 'ar' | 'en'
  crisisMode: boolean
  onCrisisDetected: () => void
  // Connection functions and state from parent
  connect: () => void
  disconnect: () => void
  startConversation: () => void
  stopConversation: () => void
  isConnected: boolean
  isInConversation: boolean
}

export function VoiceInterface({ 
  language, 
  crisisMode, 
  onCrisisDetected,
  connect,
  disconnect,
  startConversation,
  stopConversation,
  isConnected,
  isInConversation
}: VoiceInterfaceProps) {
  // Remove the useTherapyVoiceClient hook since we're getting props from parent
  // const {
  //   isConnected,
  //   isInConversation,
  //   connectionStatus,
  //   connect,
  //   disconnect,
  //   startConversation,
  //   stopConversation
  // } = useTherapyVoiceClient()

  const [isConnecting, setIsConnecting] = useState(false)

  const handleConnect = useCallback(async () => {
    setIsConnecting(true)
    try {
      await connect()
    } catch (error) {
      console.error('Connection failed:', error)
    } finally {
      setIsConnecting(false)
    }
  }, [connect])

  const texts = {
    ar: {
      connectButton: 'الاتصال بالمعالج',
      disconnectButton: 'قطع الاتصال',
      startButton: 'بدء المحادثة',
      stopButton: 'إيقاف المحادثة',
      connecting: 'جاري الاتصال...',
      connected: 'متصل',
      disconnected: 'غير متصل',
      speaking: 'جاري التحدث...',
      listening: 'جاري الاستماع...',
      ready: 'جاهز للمحادثة',
      crisis: 'وضع الأزمة مفعل',
      instructions: 'اضغط للتحدث أو ابدأ المحادثة الصوتية المستمرة',
      privacy: 'محادثتك سرية ومحمية',
      cultural: 'نحترم قيمك الإسلامية وثقافتك الخليجية'
    },
    en: {
      connectButton: 'Connect to Therapist',
      disconnectButton: 'Disconnect',
      startButton: 'Start Conversation',
      stopButton: 'Stop Conversation',
      connecting: 'Connecting...',
      connected: 'Connected',
      disconnected: 'Disconnected',
      speaking: 'Speaking...',
      listening: 'Listening...',
      ready: 'Ready to Talk',
      crisis: 'Crisis Mode Active',
      instructions: 'Press to talk or start continuous voice conversation',
      privacy: 'Your conversation is private and protected',
      cultural: 'We respect your Islamic values and Gulf culture'
    }
  }

  const currentTexts = texts[language]

  const getStatusText = () => {
    if (isConnecting) return currentTexts.connecting
    if (!isConnected) return currentTexts.disconnected
    if (isInConversation) return currentTexts.listening
    return currentTexts.connected
  }

  const getStatusColor = () => {
    if (crisisMode) return 'text-therapy-crisis'
    if (isConnecting) return 'text-therapy-accent'
    if (!isConnected) return 'text-therapy-muted'
    if (isInConversation) return 'text-therapy-primary'
    return 'text-therapy-secondary'
  }

  return (
    <div className={`space-y-6 ${language === 'ar' ? 'arabic-text' : 'english-text'}`}>
      
      {/* Status Display */}
      <div className="text-center">
        <div className={`text-2xl font-semibold mb-2 ${getStatusColor()}`}>
          {crisisMode ? currentTexts.crisis : getStatusText()}
        </div>
        
        {/* Visual Indicator */}
        <div className="flex justify-center mb-4">
          <div className={`relative ${crisisMode ? 'crisis-mode' : ''}`}>
            {isInConversation ? (
              <div className="voice-indicator" />
            ) : isConnected ? (
              <div className="w-16 h-16 rounded-full bg-therapy-secondary breathing opacity-80" />
            ) : (
              <div className="w-16 h-16 rounded-full bg-gray-300" />
            )}
          </div>
        </div>

        <p className="text-therapy-muted text-sm mb-4">
          {currentTexts.instructions}
        </p>
      </div>

      {/* Control Buttons */}
      <div className="flex flex-col space-y-3">
        {!isConnected ? (
          <button
            onClick={handleConnect}
            disabled={isConnecting}
            className={`therapy-button-primary ${isConnecting ? 'opacity-50 cursor-not-allowed' : ''}`}
          >
            {currentTexts.connectButton}
          </button>
        ) : (
          <>
            <div className="flex space-x-3">
              {!isInConversation ? (
                <button
                  onClick={startConversation}
                  className="flex-1 therapy-button-primary"
                >
                  {currentTexts.startButton}
                </button>
              ) : (
                <button
                  onClick={stopConversation}
                  className="flex-1 therapy-button-secondary"
                >
                  {currentTexts.stopButton}
                </button>
              )}
              
              <button
                onClick={disconnect}
                className="px-4 py-3 bg-gray-500 text-white rounded-lg hover:bg-gray-600 transition-colors"
              >
                {currentTexts.disconnectButton}
              </button>
            </div>
          </>
        )}
      </div>

      {/* Privacy & Cultural Notice */}
      {isConnected && (
        <div className="bg-green-50 border border-green-200 rounded-lg p-4 text-sm">
          <div className="flex items-center mb-2">
            <div className="w-2 h-2 bg-therapy-primary rounded-full mr-2" />
            <span className="text-therapy-text font-medium">{currentTexts.privacy}</span>
          </div>
          <div className="flex items-center">
            <div className="w-2 h-2 bg-therapy-secondary rounded-full mr-2" />
            <span className="text-therapy-text font-medium">{currentTexts.cultural}</span>
          </div>
        </div>
      )}

      {/* Crisis Mode Warning */}
      {crisisMode && (
        <div className="bg-red-50 border border-red-300 rounded-lg p-4 animate-pulse-slow">
          <div className="flex items-center">
            <div className="text-therapy-crisis mr-2">🚨</div>
            <div>
              <p className="text-therapy-crisis font-semibold">
                {language === 'ar' ? 'تم تفعيل وضع التدخل في الأزمة' : 'Crisis Intervention Mode Activated'}
              </p>
              <p className="text-red-600 text-sm">
                {language === 'ar' 
                  ? 'نحن هنا لمساعدتك. سيتم توصيلك بمختص إذا لزم الأمر.' 
                  : 'We are here to help you. You will be connected to a specialist if needed.'
                }
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  )
} 