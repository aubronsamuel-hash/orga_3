// Config Storybook test-runner (Playwright + Jest)
// Hooks non deprecies (preVisit/postVisit). Compatible Storybook 8.
const { getStoryContext } = require("@storybook/test-runner");

module.exports = {
async preVisit(page, context) {
await page.setViewportSize({ width: 1280, height: 800 });
},
async postVisit(page, context) {
// Placeholder: pas d assertion par defaut pour eviter le bruit.
},
// Utilitaire optionnel (dispo si besoin)
async getContext(page, context) {
const storyContext = await getStoryContext(page, context);
return storyContext;
}
};

