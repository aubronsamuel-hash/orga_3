// Config minimale; axe a11y active par defaut via test-runner.
// On durcira les regles plus tard (promotion gate).
/* eslint-disable */
module.exports = {
  // Example: filtrer certaines stories lourdes via `parameters: { test: { disable: true } }`
  async preRender(page, context) {
    // noop
  },
  async postRender(page, context) {
    // noop
  },
};
