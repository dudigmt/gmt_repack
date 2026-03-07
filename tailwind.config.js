/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './core/templates/**/*.html',
    './apps/**/templates/**/*.html',
  ],
  safelist: [
    'max-w-7xl',
    'mx-auto',
    'w-full',
    'px-4',
    'md:px-6',
    'lg:px-8',
    'py-4',
    'md:py-6',
    'lg:py-8',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
