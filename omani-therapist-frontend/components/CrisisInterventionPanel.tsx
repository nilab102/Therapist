'use client'

import React from 'react'

interface CrisisInterventionPanelProps {
  language: 'ar' | 'en'
  onClose: () => void
  onAssessmentComplete: (assessment: any) => void
}

export function CrisisInterventionPanel({ language, onClose, onAssessmentComplete }: CrisisInterventionPanelProps) {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
        <h2 className="text-xl font-bold mb-4 text-red-600">Crisis Intervention</h2>
        <p className="mb-4">Crisis intervention form will be implemented here.</p>
        <button onClick={onClose} className="therapy-button-crisis">Close</button>
      </div>
    </div>
  )
} 