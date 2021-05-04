module.exports = {
  future: {
    removeDeprecatedGapUtilities: true,
    purgeLayersByDefault: true,
  },
  purge: {
    enabled: false, //true for production build
    content: [
      '../**/templates/*.html',
      '../**/templates/**/*.html'
    ]
  },
  theme: {
    backgroundColor: theme => ({
      'white': '#000',
      'primary': '#822020',
      'secondary': '#F1F1F1',
    })
  },
  variants: {},
  plugins: [],
}