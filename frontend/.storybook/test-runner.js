import { checkA11y, injectAxe } from "axe-playwright";

export const postVisit = async (page) => {
  // Guard to avoid running axe twice
  const already = await page.evaluate(() => {
    if (window.__axe_running__) return true;
    window.__axe_running__ = true;
    return false;
  });
  if (already) return;

  // Wait for the story to be fully rendered
  await page.waitForSelector("#storybook-root", {
    state: "attached",
    timeout: 5000,
  });
  await page.waitForLoadState("domcontentloaded");

  // Inject axe once
  await injectAxe(page);

  // Limit scope to story root
  await checkA11y(page, "#storybook-root", {
    detailedReport: true,
    detailedReportOptions: { html: true },
  });

  // Release guard
  await page.evaluate(() => {
    window.__axe_running__ = false;
  });
};

// No a11y in preVisit
export const preVisit = async (_page) => {};

