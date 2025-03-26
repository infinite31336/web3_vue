module.exports = {
  root: true,
  env: {
    browser: true,
    node: true
  },
  extends: [
    'plugin:vue/essential',
    'eslint:recommended'
  ],
  plugins: ['vue'],
  rules: {
    'no-unused-vars': 'warn'
  }
};