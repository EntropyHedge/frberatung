/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/templates/**/*.html",
    "./app/static/js/**/*.js",
    "./app/templates/*.html"
  ],
  darkMode: 'class',
  safelist: [
    // Colors
    { pattern: /bg-.*/ },
    { pattern: /text-.*/ },
    { pattern: /border-.*/ },

    // Spacing
    { pattern: /p-.*/ },
    { pattern: /px-.*/ },
    { pattern: /py-.*/ },
    { pattern: /m-.*/ },
    { pattern: /mx-.*/ },
    { pattern: /my-.*/ },
    { pattern: /gap-.*/ },

    // Typography
    { pattern: /font-.*/ },
    { pattern: /text-.*/ },

    // Layout
    { pattern: /grid-.*/ },
    { pattern: /flex-.*/ },
    { pattern: /col-.*/ },

    // Effects
    { pattern: /shadow-.*/ },
    { pattern: /rounded-.*/ },

    // Other common patterns
    { pattern: /hover:.*/ },
    { pattern: /focus:.*/ },
    { pattern: /dark:.*/ }
  ],
  theme: {
    extend: {
      colors: {
        accent: {
          DEFAULT: '#0000af',
          dark: '#5555ff'
        },
        ink: {
          DEFAULT: '#0B1220',
          muted: '#475569',
          dark: {
            DEFAULT: '#E8EDF4',
            muted: '#94A3B8'
          }
        },
        surface: {
          50: '#F8FAFC',
          100: '#F1F5F9',
          200: '#E2E8F0',
          dark: {
            50: '#1E293B',
            100: '#0F172A',
            200: '#020617'
          }
        }
      },
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui'],
        display: ['Plus Jakarta Sans', 'Inter', 'ui-sans-serif'],
        mono: ['JetBrains Mono', 'ui-monospace', 'monospace']
      },
      boxShadow: {
        soft: '0 10px 30px rgba(2,6,23,0.06)',
        'soft-dark': '0 10px 30px rgba(0,0,0,0.3)',
        glow: '0 0 0 3px rgba(0,0,175,0.12), 0 0 36px rgba(0,0,175,0.18)',
        'glow-dark': '0 0 0 3px rgba(85,85,255,0.15), 0 0 36px rgba(85,85,255,0.25)',
        s: 'inset 0 1px 2px rgba(255,255,255,0.2), 0 1px 2px rgba(0,0,0,0.2), 0 2px 4px rgba(0,0,0,0.1)',
        'm': 'inset 0 1px 2px rgba(255,255,255,0.3), 0 2px 4px rgba(0,0,0,0.2), 0 4px 8px rgba(0,0,0,0.1)',
        'l': 'inset 0 1px 2px rgba(255,255,255,0.4), 0 4px 6px rgba(0,0,0,0.2), 0 6px 10px rgba(0,0,0,0.1)',
        's-dark': 'inset 0 1px 2px rgba(255,255,255,0.05), 0 1px 2px rgba(0,0,0,0.5), 0 2px 4px rgba(0,0,0,0.3)',
        'm-dark': 'inset 0 1px 2px rgba(255,255,255,0.08), 0 2px 4px rgba(0,0,0,0.5), 0 4px 8px rgba(0,0,0,0.3)',
        'l-dark': 'inset 0 1px 2px rgba(255,255,255,0.1), 0 4px 6px rgba(0,0,0,0.5), 0 6px 10px rgba(0,0,0,0.3)'
      },
      animation: {
        'gradient': 'gradient 8s linear infinite',
        'float': 'float 6s ease-in-out infinite',
        'pulse': 'pulse 4s ease-in-out infinite',
        'glow': 'glow 2s ease-in-out infinite alternate',
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'accent-pulse': 'accent-pulse 3s ease-in-out infinite'
      },
      keyframes: {
        gradient: {
          '0%, 100%': {
            'background-size': '200% 200%',
            'background-position': 'left center'
          },
          '50%': {
            'background-size': '200% 200%',
            'background-position': 'right center'
          }
        },
        float: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-20px)' }
        },
        pulse: {
          '0%, 100%': { opacity: '0.5' },
          '50%': { opacity: '1' }
        },
        glow: {
          'from': {
            boxShadow: '0 0 10px 1px rgba(59, 130, 246, 0.2)'
          },
          'to': {
            boxShadow: '0 0 20px 3px rgba(59, 130, 246, 0.4)'
          }
        },
        'accent-pulse': {
          '0%, 100%': { opacity: '0.25' },
          '50%': { opacity: '0.5' }
        }
      },
    }
  },
  plugins: [],
}
