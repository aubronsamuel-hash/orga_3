import { test, expect } from "@playwright/test";

test.describe("Calendar DnD", () => {
  test("drag & drop event and keep colors/legend", async ({ page }) => {
    await page.route("**/api/v1/calendar", async (route) => {
      const body = [
        {
          id: "a1",
          title: "Mission A",
          start: "2025-09-01T09:00:00Z",
          end: "2025-09-01T11:00:00Z",
          status: "ACCEPTED",
        },
        {
          id: "b1",
          title: "Mission B",
          start: "2025-09-01T13:00:00Z",
          end: "2025-09-01T14:00:00Z",
          status: "INVITED",
        },
      ];
      await route.fulfill({ json: body });
    });

    let moved = false;
    await page.route("**/api/v1/assignments/*/move", async (route) => {
      moved = true;
      await route.fulfill({ json: { ok: true } });
    });

    await page.goto("/calendar");
    await expect(page.locator(".fc")).toBeVisible();

    await expect(page.locator(".fc-event.cc-evt-accepted")).toHaveCount(1);
    await expect(page.locator(".fc-event.cc-evt-invited")).toHaveCount(1);

    const event = page.locator(".fc-event").first();
    const calendarGrid = page.locator(".fc-timegrid-body").first();
    const box = await calendarGrid.boundingBox();
    if (box) {
      await event.dragTo(calendarGrid, {
        targetPosition: { x: box.width * 0.6, y: box.height * 0.5 },
      });
    }
    expect(moved).toBeTruthy();

    await expect(page.locator(".fc")).toHaveScreenshot({
      animations: "disabled",
      maxDiffPixelRatio: 0.02,
    });
  });
});
