/** @type {import('tailwindcss').Config} */
export default {
	content: ['./src/**/*.{html,js,svelte,ts}'],
	darkMode: 'class',
	theme: {
		extend: {}
	},
	plugins: [require('rippleui')],

	/** @type {import('rippleui').Config} */
	rippleui: {
		themes: [
			{
				themeName: 'light',
				colorScheme: 'light',
				colors: {
					backgroundPrimary: '#F3F3F3',
					secondary: '#EDF3FC',
				}
			},
			{
				themeName: 'dark',
				colorScheme: 'dark',
				colors: {
					// primary: '#573242',
					secondary: '#677180',

					// backgroundPrimary: '#1a1a1a'
				}
			}
		]
	}
	// 	{
	// 		themeName: 'custom',
	// 		colorScheme: 'dark' | 'light',
	// 		prefersColorScheme: true
	// 	}
	// ]
};
