/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'gemini-bg': '#f8fafc',
        'gemini-card': '#ffffff',
        'gemini-accent': '#1a73e8',
        'gemini-text': '#1f1f1f',
        'gemini-blue': '#4285f4',
        'gemini-purple': '#a142f4',
        'gemini-orange': '#f4b400',
      },
      fontFamily: {
        'sans': ['"Plus Jakarta Sans"', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
