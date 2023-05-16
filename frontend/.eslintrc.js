module.exports = {
  root: true,
  env: {
    node: true
  },
  extends: [
    "plugin:vue/essential",
    "@vue/standard",
    "plugin:cypress/recommended"
  ],
  parserOptions: {
    parser: "@babel/eslint-parser"
  },
  rules: {
    "no-console": "off",
    "no-debugger": "off",
    quotes: ["off", "double"],
    semi: ["off", "never"],

    "vue/no-parsing-error": ["error", {
      "x-invalid-end-tag": false
    }]
  }
}
