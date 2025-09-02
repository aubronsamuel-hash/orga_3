import http from "k6/http";
import { check, sleep } from "k6";

/**
 * k6 smoke minimal: ping /healthz
 * Vars via env:
 * - K6_BASE_URL (default http://localhost:8000)
 * - K6_VUS (default 5)
 * - K6_DURATION (default 30s)
 */
export const options = {
  vus: __ENV.K6_VUS ? parseInt(__ENV.K6_VUS) : 5,
  duration: __ENV.K6_DURATION || "30s",
  thresholds: {
    http_req_duration: ["p(95)<300"], // cible baseline CI
    http_req_failed: ["rate<0.01"],
  },
};

const BASE = __ENV.K6_BASE_URL || "http://localhost:8000";

export default function () {
  const res = http.get(`${BASE}/healthz`);
  check(res, {
    "status is 200": (r) => r.status === 200,
    "json ok": (r) => (r.json() || {}).status === "ok",
  });
  sleep(1);
}
