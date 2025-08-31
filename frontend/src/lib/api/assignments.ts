// frontend/src/lib/api/assignments.ts
import { http } from "../http";

export async function acceptAssignment(id: string, token?: string) {
  const qs = token ? `?token=${encodeURIComponent(token)}` : "";
  return http<{ status: string }>(`/api/v1/assignments/${id}/accept${qs}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({}),
  });
}

export async function declineAssignment(id: string, reason?: string, token?: string) {
  const qs = token ? `?token=${encodeURIComponent(token)}` : "";
  return http<{ status: string }>(`/api/v1/assignments/${id}/decline${qs}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ reason }),
  });
}

export type MyAssignment = {
  id: string;
  mission_title: string;
  project_title?: string;
  status: string;
};

export async function listMyAssignments(): Promise<MyAssignment[]> {
  return http(`/api/v1/assignments?me=1`);
}
