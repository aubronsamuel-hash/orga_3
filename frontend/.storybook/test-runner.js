// Config Storybook test-runner (Playwright + Jest)
// Remplace les hooks deprecies preRender/postRender par preVisit/postVisit.
// Docs: https://storybook.js.org/docs/writing-tests/test-runner
const { getStoryContext } = require("@storybook/test-runner");

module.exports = {
  // Nouveau hook: appele avant la visite de l'iframe de la story
  async preVisit(page, context) {
    // Exemple: fixer viewport pour rendre les captures et interactions deterministes
    await page.setViewportSize({ width: 1280, height: 800 });
  },

  // Nouveau hook: appele apres la visite et rendu de la story
  async postVisit(page, context) {
    // Exemple: verifier absence d'erreurs console (faible bruit)
    const logs = [];
    page.on("console", (msg) => logs.push({ type: msg.type(), text: msg.text() }));
    // noop: laisse place a d'autres verifs si necessaire
  },

  // Optionnel: filtrer/autoriser certaines stories si besoin
  async prepare() {
    // noop
  },

  // Exemple utilitaire: obtenir le contexte d'une story (non utilise mais pret)
  async getContext(page, context) {
    const storyContext = await getStoryContext(page, context);
    return storyContext;
  }
};
