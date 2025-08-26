export type HttpMethod = "GET"|"POST"|"PUT"|"PATCH"|"DELETE";

function getCsrfToken(): string {
  const meta = document.querySelector('meta[name="csrf-token"]') as HTMLMetaElement | null;
  return meta?.content || "dev";
}

export class ApiClient {
  private base: string;
  private refreshing = false;
  private queue: Array<() => void> = [];

  constructor(base: string) {
    this.base = base.replace(/\/+$/, "");
  }

  private async _fetch(method: HttpMethod, path: string, body?: unknown): Promise<Response> {
    const url = `${this.base}${path}`;
    const headers: Record<string,string> = {};
    if (body != null) {
      headers["Content-Type"] = "application/json";
      headers["X-CSRF"] = getCsrfToken();
    }
    return fetch(url, {
      method,
      credentials: "include",
      headers,
      body: body != null ? JSON.stringify(body) : undefined
    });
  }

  private _enqueue(fn: () => void) {
    this.queue.push(fn);
  }
  private _drain() {
    const q = [...this.queue];
    this.queue = [];
    q.forEach(fn => fn());
  }

  async request<T=unknown>(method: HttpMethod, path: string, body?: unknown): Promise<T> {
    const res = await this._fetch(method, path, body);
    if (res.status !== 401) {
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return (await res.json()) as T;
    }
    // 401 -> tenter refresh sauf sur login/refresh
    if (path.startsWith("/auth/login") || path.startsWith("/auth/refresh")) {
      throw new Error("Unauthenticated");
    }
    // anti stampede
    if (this.refreshing) {
      await new Promise<void>(resolve => this._enqueue(resolve));
    } else {
      this.refreshing = true;
      const r = await this._fetch("POST", "/auth/refresh");
      this.refreshing = false;
      this._drain();
      if (!r.ok) {
        throw new Error("Refresh failed");
      }
    }
    // retry
    const retry = await this._fetch(method, path, body);
    if (!retry.ok) throw new Error(`HTTP ${retry.status}`);
    return (await retry.json()) as T;
  }

  get<T=unknown>(path: string) { return this.request<T>("GET", path); }
  post<T=unknown>(path: string, body?: unknown) { return this.request<T>("POST", path, body); }
  del<T=unknown>(path: string) { return this.request<T>("DELETE", path); }
}

export const api = new ApiClient((import.meta.env.VITE_API_BASE as string) ?? "/api/v1");
