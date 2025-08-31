import { describe, it, expect, vi, beforeEach } from "vitest";
import { http } from "../../src/lib/http";

describe("http()", () => {
  const originalFetch = global.fetch;
  beforeEach(() => { global.fetch = originalFetch as any; document.cookie = "csrf=abc"; });

  it("retries on 500 then succeeds", async () => {
    const spy = vi.fn()
      .mockResolvedValueOnce(new Response("err", { status: 500 }))
      .mockResolvedValueOnce(new Response(JSON.stringify({ ok: true }), { status: 200, headers: { "content-type":"application/json" } }));
    // @ts-ignore
    global.fetch = spy;

    const res = await http<{ ok: boolean }>("/x");
    expect(res.ok).toBe(true);
    expect(spy).toHaveBeenCalledTimes(2);
  });

  it("throws on 400", async () => {
    // @ts-ignore
    global.fetch = vi.fn().mockResolvedValue(new Response("nope", { status: 400, statusText: "Bad Request" }));
    await expect(http("/y")).rejects.toMatchObject({ status: 400 });
  });
});
