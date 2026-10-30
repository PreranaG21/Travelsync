/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        sand: {
          50: '#FAF9F6',
          100: '#F8F7F4', // Core Canvas Background
          200: '#F0EFEA',
          300: '#E8E7E3', // Core Borders
          400: '#D5D3CC',
          500: '#B0ADA4',
          600: '#8C897F',
          700: '#666660', // Secondary Muted Text
          800: '#3D3D39',
          900: '#222222', // Primary Deep Charcoal Text
          950: '#141413',
        },
        sage: {
          50: '#F4F7F5',
          100: '#EBF2EE', // Sage light tint
          200: '#D5E5DC',
          300: '#CADCD2', // Sage border
          400: '#7FA894',
          500: '#55886E',
          600: '#3D6E57', // Sage Primary Action
          700: '#2F5844', // Sage Dark Action
          800: '#234233',
          900: '#182C22',
        },
        // Retain brand alias mapped to sage for backwards-compatibility
        brand: {
          50: '#F4F7F5',
          100: '#EBF2EE',
          200: '#D5E5DC',
          300: '#CADCD2',
          400: '#7FA894',
          500: '#3D6E57',
          600: '#2F5844',
          700: '#234233',
          800: '#182C22',
          900: '#112018',
        },
        surface: {
          50: '#FFFFFF',
          100: '#FAF9F7',
          200: '#F8F7F4',
          300: '#E8E7E3',
          400: '#D8D6CE',
          500: '#8C897F',
          600: '#666660',
          700: '#444440',
          800: '#2A2A28',
          900: '#222222',
          950: '#141413',
        }
      },
      fontFamily: {
        sans: ['Inter', 'Outfit', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
        display: ['Outfit', 'Inter', 'sans-serif'],
      },
      boxShadow: {
        'subtle': '0 1px 3px 0 rgba(0, 0, 0, 0.04), 0 1px 2px -1px rgba(0, 0, 0, 0.04)',
        'card': '0 4px 12px -2px rgba(0, 0, 0, 0.05), 0 2px 6px -1px rgba(0, 0, 0, 0.02)',
        'elevated': '0 12px 28px -4px rgba(0, 0, 0, 0.08), 0 4px 10px -2px rgba(0, 0, 0, 0.03)',
        'sage': '0 4px 14px 0 rgba(61, 110, 87, 0.25)',
      },
      borderRadius: {
        'sm': '6px',
        'md': '8px',
        'lg': '10px',
        'xl': '14px',
        '2xl': '18px',
      }
    },
  },
  plugins: [],
}
