import { test, expect } from "@playwright/test";

test("@smoke Accounting monthly users page smoke", async ({ page }) => {
  await page.goto("/accounting/monthly-users");
  await expect(
    page.getByText("Comptabilite - Totaux mensuels par user")
  ).toBeVisible();
  await expect(page.getByRole("button", { name: "Charger" })).toBeVisible();

  // Le bouton est desactive tant qu'il n'y a pas de donnees mais doit etre present.
  const exportBtn = page.getByRole("button", { name: /export csv/i });
  await expect(exportBtn).toBeVisible();
});
