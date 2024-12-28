/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["**/*.py"],
  theme: {
    extend: {
      fontFamily: {
        inter: ['Inter', 'sans-serif'],
        rubik: ['Rubik', 'sans-serif'],
      },
      colors: {
        // Primary tints
        primary: {
          0: '#27529a',
          10: '#4563a5',
          20: '#5f75b0',
          30: '#7687bc',
          40: '#8d9ac7',
          50: '#a4aed2',
        },
        // Surface colors
        surface: {
          0: '#121212',
          10: '#282828',
          20: '#3f3f3f',
          30: '#575757',
          40: '#717171',
          50: '#8b8b8b',
        },
      },
    },
  },
  plugins: [ ]
}
