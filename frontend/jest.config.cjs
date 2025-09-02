// Jest config pour Storybook test-runner et unit tests (frontend)
// Force @swc/jest a utiliser une cible supportee par @swc/core present en CI.
module.exports = {
  testEnvironment: "jsdom",
  transform: {
    "^.+\\.(t|j)sx?$": [
      "@swc/jest",
      {
        sourceMaps: "inline",
        module: { type: "commonjs" },
        jsc: {
          target: "es2022",
          transform: {
            react: { runtime: "automatic" },
            hidden: { jest: true }
          }
        }
      }
    ]
  },
  moduleFileExtensions: ["ts", "tsx", "js", "jsx", "json"],
  testPathIgnorePatterns: ["/node_modules/", "/dist/", "/storybook-static/"]
};
