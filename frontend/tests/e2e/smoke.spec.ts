import { test, expect } from "@playwright/test";

test("home loads and shows title", async ({ page }) => {
  await page.goto("/");
  await expect(page).toHaveTitle(/Coulisses Crew/);
  await expect(page.locator("header")).toBeVisible();
});
