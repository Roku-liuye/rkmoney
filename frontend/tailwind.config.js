/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: '#ffffff',
        primary: '#1a1a1a',
        secondary: '#f3f4f6',
        accent: '#3b82f6',
      }
    },
  },
  plugins: [],
}
