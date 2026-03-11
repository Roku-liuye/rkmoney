/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: '#ffffff',
        'dark-background': '#1a1a1a',
        primary: '#1a1a1a',
        'dark-primary': '#ffffff',
        secondary: '#f3f4f6',
        'dark-secondary': '#2d2d2d',
        accent: '#3b82f6',
      }
    },
  },
  plugins: [],
}
