/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/templates/**/*.html",
    "./app/static/js/**/*.js",
    "./app/templates/*.html"
  ],
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
    { pattern: /focus:.*/ }
  ],
  theme: {
    extend: {
      animation: {
        'gradient': 'gradient 8s linear infinite',
        'float': 'float 6s ease-in-out infinite',
        'pulse': 'pulse 4s ease-in-out infinite',
        'glow': 'glow 2s ease-in-out infinite alternate',
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
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
          '0%, 100%': { opacity: 0.5 },
          '50%': { opacity: 1 }
        },
        glow: {
          'from': {
            boxShadow: '0 0 10px 1px rgba(59, 130, 246, 0.2)'
          },
          'to': {
            boxShadow: '0 0 20px 3px rgba(59, 130, 246, 0.4)'
          }
        }
      },
    }
  },
  plugins: [],
}
