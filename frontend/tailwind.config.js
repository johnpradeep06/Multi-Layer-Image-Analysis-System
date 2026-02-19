/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                'crime-black': '#0a0a0a',
                'crime-gray': '#1a1a1a',
                'terminal-green': '#00ff00',
                'alert-red': '#ff0000',
                'warning-yellow': '#ffff00',
            },
            fontFamily: {
                mono: ['"Courier New"', 'Courier', 'monospace'],
            }
        },
    },
    plugins: [],
}
