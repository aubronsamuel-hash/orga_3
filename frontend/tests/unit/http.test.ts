// frontend/tests/unit/http.test.ts
import { describe, it, expect, vi, beforeEach } from "vitest";
import { http } from "../../src/lib/http";

describe("http()", () => {
  const originalFetch: typeof fetch = globalThis.fetch;

  beforeEach(() => {
    globalThis.fetch = originalFetch;
    // jsdom sait gérer document.cookie
    document.cookie = "csrf=abc";
  });

  it("retries on 500 then succeeds", async () => {
    const spy = vi.fn<Parameters<typeof fetch>, Promise<Response>>();
    spy
      .mockResolvedValueOnce(new Response("err", { status: 500 }))
      .mockResolvedValueOnce(
        new Response(JSON.stringify({ ok: true }), {
          status: 200,
          headers: { "content-type": "application/json" },
        })
      );

    // cast sûr: on fournit bien une fn compatible fetch
    globalThis.fetch = spy as unknown as typeof fetch;

    const res = await http<{ ok: boolean }>("/x");
    expect(res.ok).toBe(true);
    expect(spy).toHaveBeenCalledTimes(2);
  });

  it("throws on 400", async () => {
    const spy = vi
      .fn<Parameters<typeof fetch>, Promise<Response>>()
      .mockResolvedValue(
        new Response("nope", { status: 400, statusText: "Bad Request" })
      );

    globalThis.fetch = spy as unknown as typeof fetch;

    await expect(http("/y")).rejects.toMatchObject({ status: 400 });
  });
});
