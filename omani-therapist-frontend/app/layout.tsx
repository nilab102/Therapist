import './globals.css'
import React from 'react'
import { Inter } from 'next/font/google'

const inter = Inter({ subsets: ['latin'] })

export const metadata = {
  title: 'OMANI Therapist Voice | معالج صوتي عُماني',
  description: 'Culturally-sensitive AI voice therapy platform for Gulf Arabic speakers | منصة العلاج النفسي الصوتي المدعومة بالذكاء الاصطناعي للناطقين بالعربية الخليجية',
  keywords: 'therapy, mental health, AI, voice, Arabic, Gulf, Oman, Islamic therapy, علاج نفسي, صحة نفسية',
  author: 'OMANI Therapist Voice Team',
  robots: 'index, follow',
  'og:title': 'OMANI Therapist Voice | معالج صوتي عُماني',
  'og:description': 'AI-powered voice therapy respecting Gulf Arabic culture and Islamic values',
  'og:type': 'website',
  'og:locale': 'ar_OM',
  'og:locale:alternate': 'en_US',
}

export const viewport = {
  width: 'device-width',
  initialScale: 1,
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="ar" dir="rtl" className="scroll-smooth">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          href="https://fonts.googleapis.com/css2?family=Amiri:ital,wght@0,400;0,700;1,400;1,700&family=Inter:wght@300;400;500;600;700&family=Noto+Sans+Arabic:wght@300;400;500;600;700&display=swap"
          rel="stylesheet"
        />
        <meta name="theme-color" content="#2E7D32" />
        <meta name="apple-mobile-web-app-capable" content="yes" />
        <meta name="apple-mobile-web-app-status-bar-style" content="default" />
        <meta name="apple-mobile-web-app-title" content="OMANI Therapist" />
      </head>
      <body className={`${inter.className} bg-therapy-background min-h-screen`}>
        <div className="islamic-pattern min-h-screen">
          {children}
        </div>
      </body>
    </html>
  )
} 