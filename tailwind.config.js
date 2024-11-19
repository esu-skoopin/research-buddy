module.exports = {
	content: [
		'./app/templates/**/*.html',
		'./app/static/js/**/*.js',
		'./node_modules/preline/dist/*.js'
	],
	theme: {
		extend: {}
	},
	plugins: [
		require('preline/plugin')
	]
};