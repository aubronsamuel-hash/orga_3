import { test, expect } from "@playwright/test";

test("retry probe: 500 twice then 200 -> page shows OK", async ({ page }) => {
  let calls = 0;
  await page.route("**/__test/500-then-200", async route => {
    calls += 1;
    if (calls < 3) {
      await route.fulfill({ status: 500, body: "boom" });
    } else {
      await route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ ok: true }) });
    }
  });

  await page.goto("/dev/retry");
  await expect(page.getByTestId("retry-result")).toHaveText("OK");
});
