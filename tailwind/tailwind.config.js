module.exports = {
  content: [
    "../pub/apps/**/templates/**/*.{html,py,js}",
    "../pub/**/templates/**/*.{html,py,js}",
    "../pub/static/js/**/*.js",
  ],
  theme: {
    extend: {
      animation: {
        'fade-in-up': 'fade-in-up 0.6s ease-out forwards',
        'float': 'float 3s ease-in-out infinite',
      },
      keyframes: {
        'fade-in-up': {
          '0%': {
            opacity: '0',
            transform: 'translateY(20px)'
          },
          '100%': {
            opacity: '1',
            transform: 'translateY(0)'
          }
        },
        'float': {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-10px)' }
        }
      }
    }
  },
  media: false,
};
