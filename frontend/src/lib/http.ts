// http.ts - fetch client avec retries, CSRF, cookies httpOnly
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
  // CSRF: header basique (road book: cookies httpOnly + header CSRF cote FE)
  const csrf = readCookie("csrf") || (document.querySelector('meta[name="csrf"]') as HTMLMetaElement)?.content;
  if (csrf) headers.set("x-csrf", csrf);

  const res = await fetch(url, {
    ...opts,
    credentials: "include",
    headers,
  });

  if (res.status >= 500 && retry > 0) {
    // backoff simple
    await new Promise(r => setTimeout(r, 300 * (3 - retry)));
    return http<T>(url, { ...opts, retry: retry - 1 });
  }

  if (!res.ok) {
    let body: unknown = undefined;
    try { body = await res.json(); } catch {}
    const err: HttpError = { status: res.status, message: res.statusText, body };
    throw err;
  }

  const text = await res.text();
  try { return JSON.parse(text) as T; } catch { return text as unknown as T; }
}
