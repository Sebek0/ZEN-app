/** @type {import('tailwindcss').Config} */
export default {
	content: ["./index.html", "./src/**/*.{js,jsx,ts,tsx}"],
	theme: {
		extend: {
			dropShadow: {
				custom: "0 1.2px 1.2px rgba(0,0,0,0.8)",
			},
			colors: {
				primary: "#36393f",
				secondary: "#202225",
				accent: "#b42c24",
			},
			fontSize: {
				xxs: ".5rem",
			},
		},
	},
	plugins: [],
};
