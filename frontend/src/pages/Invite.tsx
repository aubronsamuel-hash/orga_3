import { useEffect, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { verifyInvitation } from "../lib/api/invitations";
import { acceptAssignment, declineAssignment } from "../lib/api/assignments";

export default function InviteLanding() {
  const [sp] = useSearchParams();
  const token = sp.get("token") || "";
  const [info, setInfo] = useState<any>();
  const [error, setError] = useState<string | undefined>();
  const nav = useNavigate();

  useEffect(() => {
    async function run() {
      try {
        setInfo(await verifyInvitation(token));
      } catch (e: any) {
        setError(e?.message || "invalid token");
      }
    }
    if (token) run();
  }, [token]);

  async function doAccept() {
    if (!info) return;
    await acceptAssignment(info.assignment_id, token);
    nav("/login?accepted=1");
  }

  async function doDecline() {
    if (!info) return;
    const reason = window.prompt("Reason?") || undefined;
    await declineAssignment(info.assignment_id, reason, token);
    nav("/thanks?declined=1");
  }

  if (!token) return <div className="p-6 text-red-600">Missing token</div>;
  if (error) return <div className="p-6 text-red-600">{error}</div>;
  if (!info) return <div className="p-6">Loading...</div>;

  return (
    <div className="p-6 space-y-4 max-w-xl">
      <h1 className="text-2xl font-bold">Invitation</h1>
      <div className="p-4 rounded border">
        <div>
          Project: <b>{info.project_title || "-"}</b>
        </div>
        <div>
          Mission: <b>{info.mission_title || "-"}</b>
        </div>
        <div>Expires: {new Date(info.expires_at).toLocaleString()}</div>
      </div>
      <div className="space-x-2">
        <button
          className="px-3 py-1 rounded bg-green-600 text-white"
          onClick={doAccept}
        >
          Accept
        </button>
        <button
          className="px-3 py-1 rounded bg-red-600 text-white"
          onClick={doDecline}
        >
          Decline
        </button>
      </div>
    </div>
  );
}
