'use client'

import React from 'react'

interface LanguageSwitcherProps {
  currentLanguage: 'ar' | 'en'
  onLanguageChange: (language: 'ar' | 'en') => void
}

export function LanguageSwitcher({ currentLanguage, onLanguageChange }: LanguageSwitcherProps) {
  return (
    <div className="flex bg-gray-100 rounded-lg p-1">
      <button
        onClick={() => onLanguageChange('ar')}
        className={`px-3 py-1 rounded text-sm font-medium transition-colors ${
          currentLanguage === 'ar' 
            ? 'bg-white text-therapy-primary shadow-sm' 
            : 'text-gray-600 hover:text-therapy-primary'
        }`}
      >
        العربية
      </button>
      <button
        onClick={() => onLanguageChange('en')}
        className={`px-3 py-1 rounded text-sm font-medium transition-colors ${
          currentLanguage === 'en' 
            ? 'bg-white text-therapy-primary shadow-sm' 
            : 'text-gray-600 hover:text-therapy-primary'
        }`}
      >
        English
      </button>
    </div>
  )
} 