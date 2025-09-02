import { test, expect } from "@playwright/test";

test("@smoke Accounting monthly users page smoke", async ({ page }) => {
  await page.goto("/accounting/monthly-users");
  await expect(
    page.getByText("Comptabilite - Totaux mensuels par user")
  ).toBeVisible();
  await expect(page.getByRole("button", { name: "Charger" })).toBeVisible();
  await expect(page.getByRole("button", { name: "Export CSV" })).toBeVisible();
});
