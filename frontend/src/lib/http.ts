// frontend/src/lib/http.ts
export type HttpError = { status: number; message: string; body?: unknown };

function readCookie(name: string): string | null {
  const m = document.cookie.match(new RegExp("(^| )" + name + "=([^;]+)"));
  return m ? decodeURIComponent(m[2]) : null;
}

export async function http<T>(
  url: string,
  opts: RequestInit & { retry?: number } = {}
): Promise<T> {
  const retry = opts.retry ?? 2;
  const headers = new Headers(opts.headers || {});
  const csrf =
    readCookie("csrf") ||
    (document.querySelector('meta[name="csrf"]') as HTMLMetaElement | null)?.content ||
    null;
  if (csrf) headers.set("x-csrf", csrf);

  const res = await fetch(url, {
    ...opts,
    credentials: "include",
    headers,
  });

  if (res.status >= 500 && retry > 0) {
    await new Promise((r) => setTimeout(r, 300 * (3 - retry)));
    return http<T>(url, { ...opts, retry: retry - 1 });
  }

  const contentType = res.headers.get("content-type") || "";

  if (!res.ok) {
    let body: unknown = undefined;
    if (contentType.includes("json")) {
      try {
        body = await res.json();
      } catch (_e) {
        body = undefined; // non-JSON ou parse KO → ignore proprement
      }
    } else {
      try {
        body = await res.text();
      } catch (_e) {
        body = undefined;
      }
    }
    const err: HttpError = { status: res.status, message: res.statusText, body };
    throw err;
  }

  if (contentType.includes("json")) {
    // @ts-expect-error: si T n'est pas JSON, l'appelant sait ce qu'il fait
    return res.json();
  }
  // @ts-expect-error: idem ci-dessus
  return res.text();
}
