export type TimeWindow = { start: string; end: string };
export type ConflictItem = {
  conflict_id: string;
  user_id: number;
  user_name: string;
  mission_ids: number[];
  window: TimeWindow;
  reason: string;
};
export type Suggestion = { user_id: number; user_name: string };
export type ConflictDetail = { conflict: ConflictItem; suggestions: Suggestion[] };

const API = import.meta.env.VITE_API_BASE || "http://localhost:8000";

export async function fetchConflicts(fromIso: string, toIso: string): Promise<ConflictItem[]> {
  const r = await fetch(`${API}/api/v1/conflicts?from=${encodeURIComponent(fromIso)}&to=${encodeURIComponent(toIso)}`);
  if (!r.ok) throw new Error("Erreur API conflits");
  return r.json();
}

export async function fetchConflict(id: string, fromIso: string, toIso: string): Promise<ConflictDetail> {
  const r = await fetch(`${API}/api/v1/conflicts/${encodeURIComponent(id)}?from=${encodeURIComponent(fromIso)}&to=${encodeURIComponent(toIso)}`);
  if (!r.ok) throw new Error("Erreur API conflit");
  return r.json();
}

export async function resolveConflict(conflict_id: string, mission_id: number, replacement_user_id: number): Promise<boolean> {
  const r = await fetch(`${API}/api/v1/conflicts/resolve`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ conflict_id, replace_assignment_mission_id: mission_id, replacement_user_id })
  });
  if (!r.ok) return false;
  const data = await r.json();
  return !!data.resolved;
}
