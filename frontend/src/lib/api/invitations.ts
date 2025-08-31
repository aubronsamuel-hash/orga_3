// frontend/src/lib/api/invitations.ts
import { http } from "../http";

export type InvitationPreview = {
  assignment_id: string;
  mission_title?: string;
  project_title?: string;
  status?: string;
  expires_at: string;
};

export async function verifyInvitation(token: string): Promise<InvitationPreview> {
  return http(`/api/v1/invitations/verify?token=${encodeURIComponent(token)}`);
}

export async function createInvitation(assignment_id: string) {
  return http<{ id: string; token: string; expires_at: string }>(`/api/v1/invitations`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ assignment_id }),
  });
}
