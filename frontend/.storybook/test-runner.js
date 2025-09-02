// @ts-check
// Runner Storybook v8 — utilise preVisit/postVisit (remplace preRender/postRender)
const { getStoryContext } = require("@storybook/test-runner");
const { injectAxe, checkA11y } = require("axe-playwright");

/** @type {import('@storybook/test-runner').TestRunnerConfig} */
module.exports = {
  async preVisit(page, context) {
    // Attendre que l iframe soit pret avant axe
    await page.waitForLoadState("domcontentloaded");
    await injectAxe(page);
  },

  async postVisit(page, context) {
    // Accessibility de base: on ignore les stories marquées a11y: { disable: true }
    const storyContext = await getStoryContext(page, context);
    if (storyContext && storyContext.parameters?.a11y?.disable) return;
    await checkA11y(page, "#storybook-root", {
      detailedReport: false,
      detailedReportOptions: { html: false },
    });
  },

  // Stabilite CI (utile en runners ephemeres)
  concurrency: 2,
  // Timeout raisonnable mais strict
  // (la CI affichait ~4-5s totaux; on laisse marge)
  storyTimeout: 20000,
};
