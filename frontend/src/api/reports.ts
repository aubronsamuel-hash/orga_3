export type MonthlyUserItem = {
  user_id: string;
  user_name: string;
  month: string; // YYYY-MM
  hours_planned: number;
  hours_confirmed: number;
  amount: number;
};

export type MonthlyUsersResponse = {
  org_id: string;
  project_id?: string | null;
  date_from: string; // YYYY-MM-DD
  date_to: string; // YYYY-MM-DD
  items: MonthlyUserItem[];
  currency: "EUR";
};

const API_BASE = import.meta.env.VITE_API_BASE ?? "http://localhost:8000";

export async function fetchMonthlyUsers(params: {
  org_id: string;
  project_id?: string;
  date_from: string;
  date_to: string;
}): Promise<MonthlyUsersResponse> {
  const url = new URL("/api/v1/reports/monthly-users", API_BASE);
  Object.entries(params).forEach(([k, v]) => {
    if (v !== undefined && v !== null) url.searchParams.set(k, String(v));
  });
  const r = await fetch(url.toString(), { headers: { Accept: "application/json" } });
  if (!r.ok) throw new Error(`HTTP ${r.status}`);
  return r.json();
}

export function exportCSV(params: {
  org_id: string;
  project_id?: string;
  date_from: string;
  date_to: string;
}): void {
  const url = new URL("/api/v1/exports/csv", API_BASE);
  url.searchParams.set("type", "monthly-users");
  Object.entries(params).forEach(([k, v]) => v != null && url.searchParams.set(k, String(v)));
  window.location.href = url.toString();
}
