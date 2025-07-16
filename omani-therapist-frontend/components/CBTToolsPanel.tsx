'use client'

import React from 'react'

interface CBTToolsPanelProps {
  language: 'ar' | 'en'
  onClose: () => void
  onTechniqueApplied: (technique: string, data: any) => void
}

export function CBTToolsPanel({ language, onClose, onTechniqueApplied }: CBTToolsPanelProps) {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
        <h2 className="text-xl font-bold mb-4">CBT Tools</h2>
        <p className="mb-4">CBT techniques panel will be implemented here.</p>
        <button onClick={onClose} className="therapy-button-secondary">Close</button>
      </div>
    </div>
  )
} 