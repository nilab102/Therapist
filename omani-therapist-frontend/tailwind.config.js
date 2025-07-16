/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        // OMANI therapy brand colors
        'therapy-primary': '#2E7D32',      // Calming green
        'therapy-secondary': '#4A90E2',    // Trust blue  
        'therapy-accent': '#F39C12',       // Warm orange
        'therapy-background': '#F8F9FA',   // Light background
        'therapy-text': '#2C3E50',         // Dark text
        'therapy-muted': '#6C757D',        // Muted text
        'therapy-success': '#28A745',      // Success green
        'therapy-warning': '#FFC107',      // Warning yellow
        'therapy-danger': '#DC3545',       // Danger red
        'therapy-crisis': '#E74C3C',       // Crisis red
      },
      fontFamily: {
        // Arabic fonts
        'arabic': ['Amiri', 'Noto Sans Arabic', 'sans-serif'],
        'english': ['Inter', 'system-ui', 'sans-serif'],
      },
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'breath': 'breath 4s ease-in-out infinite',
      },
      keyframes: {
        breath: {
          '0%, 100%': { transform: 'scale(1)' },
          '50%': { transform: 'scale(1.05)' },
        }
      }
    },
  },
  plugins: [
    // RTL support for Arabic
    function({ addUtilities }) {
      addUtilities({
        '.rtl': {
          direction: 'rtl',
        },
        '.ltr': {
          direction: 'ltr',
        },
      })
    }
  ],
} 