module.exports = {
root: true,
env: { browser: true, es2022: true, node: true },
parser: "@typescript-eslint/parser",
parserOptions: { ecmaVersion: 2022, sourceType: "module" },
plugins: ["@typescript-eslint", "react", "react-hooks"],
extends: [
"eslint:recommended",
"plugin:react/recommended",
"plugin:react-hooks/recommended",
"plugin:@typescript-eslint/recommended",
"prettier"
],
settings: { react: { version: "detect" } },
rules: {
"react/react-in-jsx-scope": "off",
"react/prop-types": "off",
"@typescript-eslint/no-unused-vars": ["error", { "argsIgnorePattern": "^_" }]
},
ignorePatterns: ["dist", "node_modules", "storybook-static"]
};
