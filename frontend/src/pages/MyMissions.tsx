import { useEffect, useState } from "react";
import {
  listMyAssignments,
  acceptAssignment,
  declineAssignment,
  type MyAssignment,
} from "../lib/api/assignments";

export default function MyMissions() {
  const [rows, setRows] = useState<MyAssignment[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | undefined>();

  async function refresh() {
    try {
      setLoading(true);
      setRows(await listMyAssignments());
    } catch (e: any) {
      setError(e?.message || "error");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    refresh();
  }, []);

  async function onAccept(id: string) {
    await acceptAssignment(id);
    await refresh();
  }

  async function onDecline(id: string) {
    const reason = window.prompt("Reason for decline?") || undefined;
    await declineAssignment(id, reason);
    await refresh();
  }

  if (loading) return <div className="p-6">Loading...</div>;
  if (error) return <div className="p-6 text-red-600">{error}</div>;

  return (
    <div className="p-6 space-y-4">
      <h1 className="text-2xl font-bold">My Missions</h1>
      <table className="w-full text-sm">
        <thead>
          <tr>
            <th>Mission</th>
            <th>Project</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((r) => (
            <tr key={r.id} className="border-t">
              <td>{r.mission_title}</td>
              <td>{r.project_title || "-"}</td>
              <td>{r.status}</td>
              <td className="space-x-2">
                {r.status === "INVITED" && (
                  <>
                    <button
                      className="px-3 py-1 rounded bg-green-600 text-white"
                      onClick={() => onAccept(r.id)}
                    >
                      Accept
                    </button>
                    <button
                      className="px-3 py-1 rounded bg-red-600 text-white"
                      onClick={() => onDecline(r.id)}
                    >
                      Decline
                    </button>
                  </>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
