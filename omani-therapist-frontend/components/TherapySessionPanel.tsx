'use client'

import React from 'react'

interface TherapySessionPanelProps {
  language: 'ar' | 'en'
  session: any
  onClose: () => void
  onSave: (session: any) => void
}

export function TherapySessionPanel({ language, session, onClose, onSave }: TherapySessionPanelProps) {
  const texts = {
    ar: {
      title: 'إدارة الجلسة العلاجية',
      close: 'إغلاق'
    },
    en: {
      title: 'Therapy Session Management',
      close: 'Close'
    }
  }

  const currentTexts = texts[language]

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
        <h2 className={`text-xl font-bold mb-4 ${language === 'ar' ? 'arabic-text' : 'english-text'}`}>
          {currentTexts.title}
        </h2>
        <p className="mb-4">Session management form will be implemented here.</p>
        <button
          onClick={onClose}
          className="therapy-button-primary"
        >
          {currentTexts.close}
        </button>
      </div>
    </div>
  )
} 