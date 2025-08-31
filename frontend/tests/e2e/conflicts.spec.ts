import { test, expect } from "@playwright/test";

test("resolution d un conflit via UI", async ({ page }) => {
  const base = process.env.PLAYWRIGHT_BASE_URL || "http://localhost:5173";
  await page.goto(`${base}/conflicts`);
  await page.waitForTimeout(500);
  const buttons = page.locator("button:has-text('Remplacer par')");
  const count = await buttons.count();
  if (count === 0) {
    test.skip(true, "Aucun conflit dans le dataset");
  } else {
    const firstCard = page.locator("[class*='ConflictCard']").first();
    await buttons.first().click();
    await expect(firstCard).toBeHidden({ timeout: 5000 });
  }
});
