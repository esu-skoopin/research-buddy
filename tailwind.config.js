const defaultTheme = require('tailwindcss/defaultTheme');

module.exports = {
	content: [
		'./app/templates/**/*.html',
		'./app/static/js/**/*.js',
		'./node_modules/preline/dist/*.js'
	],
	theme: {
		extend: {
			fontFamily: {
				sans: ['Inter', ...defaultTheme.fontFamily.sans]
			}
		}
	},
	plugins: [
		require('preline/plugin')
	]
};