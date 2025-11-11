// This is eslint.config.js
module.exports = [
  {
    files: ["src/**/*.js"], // Tell ESLint to check all .js files in the src folder
    rules: {
      "semi": "error", // Enforce semicolons (just an example rule)
      "no-unused-vars": "warn" // Warn about unused variables
    }
  }
];