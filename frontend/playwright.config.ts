import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
testDir: "tests/e2e",
timeout: 30_000,
retries: 0,
webServer: {
command: "npm run preview",
port: 5173,
reuseExistingServer: true
},
use: {
baseURL: "http://localhost:5173",
trace: "off",
headless: true
},
projects: [
{ name: "chromium", use: { ...devices["Desktop Chrome"] } }
]
});
