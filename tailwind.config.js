/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './core/templates/**/*.html',
    './apps/**/templates/**/*.html',
    './**/*.py',  // optional: untuk mendeteksi class di Python strings
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
