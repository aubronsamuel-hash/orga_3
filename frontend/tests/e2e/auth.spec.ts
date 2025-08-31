import { test, expect } from "@playwright/test";

test.describe("auth flow (login, garde, refresh)", () => {
  test("redir -> login, puis login OK, puis refresh 401", async ({ page }) => {
    let authed = false;
    let projects401Once = true;

    await page.route("**/api/v1/auth/me", async route => {
      if (!authed) {
        return route.fulfill({ status: 401, contentType: "application/json", body: JSON.stringify({ error: "unauth" }) });
      }
      return route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ id: "a1", email: "sam@example.com" }) });
    });

    await page.route("**/api/v1/auth/login", async route => {
      authed = true;
      return route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ ok: true }) });
    });

    await page.route("**/api/v1/auth/refresh", async route => {
      authed = true;
      return route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ ok: true }) });
    });

    await page.route("**/api/v1/projects", async route => {
      if (projects401Once) {
        projects401Once = false;
        return route.fulfill({ status: 401, contentType: "application/json", body: JSON.stringify({}) });
      }
      return route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ items: [{ id: "p1" }] }) });
    });

    // aller sur une page protegee -> redir login
    await page.goto("/app");
    await expect(page).toHaveURL(/\/login/);
    await expect(page.getByLabel("Email")).toBeVisible();

    // login
    await page.getByLabel("Email").fill("sam@example.com");
    await page.getByLabel("Mot de passe").fill("secret");
    await page.getByRole("button", { name: "Se connecter" }).click();

    // arrive sur /app
    await expect(page).toHaveURL(/\/app/);
    await expect(page.getByText("Bonjour sam@example.com")).toBeVisible();

    // declencher un 401 -> refresh -> retry
    await page.getByRole("button", { name: "Charger projets" }).click();
    await expect(page.getByText("Projets: 1")).toBeVisible();
  });
});
