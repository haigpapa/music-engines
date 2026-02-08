/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                'pro-black': '#121212',
                'pro-gray': '#1E1E1E',
                'electric-cyan': '#00FFFF',
                'warning-orange': '#FF5722',
                'volt-green': '#C0FF00',
            },
            fontFamily: {
                mono: ['"JetBrains Mono"', 'monospace'],
                sans: ['"Inter"', 'sans-serif'],
            },
        },
    },
    plugins: [],
}
