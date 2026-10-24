/** @type {import('tailwindcss').Config} */
export default {
  content: ['./**/*.html'],
  theme: {
    extend: {
      colors: {
        graphite: {
          DEFAULT: '#141613',
          2: '#1d201b',
          3: '#2a2e27',
          4: '#363b32',
        },
        paper: {
          DEFAULT: '#f7f4ec',
          2: '#ede8dc',
          3: '#e2dccf',
        },
        amber: {
          DEFAULT: '#ffc21a',
          deep: '#e0a400',
          soft: '#ffd75a',
          line: 'rgba(255,194,26,0.35)',
        },
        ink: '#191b17',
        muted: '#6c7066',
        accent: '#ff8a3d',
      },
      fontFamily: {
        display: ['"Space Grotesk"', 'ui-sans-serif', 'system-ui', 'sans-serif'],
        body: ['"Inter"', 'ui-sans-serif', 'system-ui', 'sans-serif'],
      },
      maxWidth: {
        prose: '1180px',
      },
      animation: {
        'fade-up': 'fade-up 0.7s cubic-bezier(0.22,1,0.36,1) both',
        'fade-in': 'fade-in 0.6s ease both',
        'amber-pulse': 'amber-pulse 3.4s ease-in-out infinite',
      },
      keyframes: {
        'fade-up': {
          '0%': { opacity: '0', transform: 'translateY(18px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        'fade-in': {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        'amber-pulse': {
          '0%,100%': { opacity: '0.55' },
          '50%': { opacity: '0.95' },
        },
      },
    },
  },
  plugins: [],
};
