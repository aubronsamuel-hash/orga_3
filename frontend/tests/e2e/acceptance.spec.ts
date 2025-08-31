import { test, expect } from "@playwright/test";

const runAcceptance = !!process.env.E2E_ACCEPTANCE;

(runAcceptance ? test : test.skip)("invite page shows error on missing token", async ({ page }) => {
  await page.goto("/invite");
  await expect(page.locator("text=Missing token")).toBeVisible();
});

(runAcceptance ? test : test.skip)("my missions lists invited items", async ({ page }) => {
  await page.goto("/my-missions");
  await expect(page.locator("text=My Missions")).toBeVisible();
});
