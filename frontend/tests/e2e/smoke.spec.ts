import { test, expect } from "@playwright/test";

const BASE = process.env.E2E_BASE_URL ?? "http://localhost:5173";

test("@smoke home responds and renders something", async ({ page }) => {
  const resp = await page.goto(BASE, { waitUntil: "domcontentloaded" });
  expect(resp?.ok(), "root should respond 2xx").toBeTruthy();
  const bodyText = (await page.textContent("body")) ?? "";
  expect(bodyText.length, "page should not be empty").toBeGreaterThan(0);
});

