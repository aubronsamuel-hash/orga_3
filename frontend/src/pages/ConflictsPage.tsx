import React, { useEffect, useState } from "react";
import ConflictCard from "../components/conflicts/ConflictCard";
import {
  fetchConflicts,
  fetchConflict,
  resolveConflict,
  type ConflictItem,
  type ConflictDetail,
} from "../services/conflicts";

export default function ConflictsPage() {
  const [fromIso] = useState(new Date(Date.now() - 24 * 3600 * 1000).toISOString());
  const [toIso] = useState(new Date(Date.now() + 7 * 24 * 3600 * 1000).toISOString());
  const [items, setItems] = useState<ConflictItem[]>([]);
  const [details, setDetails] = useState<Record<string, ConflictDetail>>({});
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    (async () => {
      setLoading(true);
      const cs = await fetchConflicts(fromIso, toIso);
      setItems(cs);
      const entries = await Promise.all(
        cs.map((c) => fetchConflict(c.conflict_id, fromIso, toIso))
      );
      const byId: Record<string, ConflictDetail> = {};
      entries.forEach((e) => (byId[e.conflict.conflict_id] = e));
      setDetails(byId);
      setLoading(false);
    })();
  }, [fromIso, toIso]);

  async function onResolve(conflictId: string, missionId: number, replacementUserId: number) {
    const ok = await resolveConflict(conflictId, missionId, replacementUserId);
    if (ok) {
      setItems((prev) => prev.filter((i) => i.conflict_id !== conflictId));
    } else {
      alert("Echec resolution");
    }
  }

  return (
    <div className="p-6 space-y-4">
      <h1 className="text-2xl font-bold">Resolution des Conflits</h1>
      {loading && <div>Chargement...</div>}
      {!loading && items.length === 0 && <div>Aucun conflit detecte</div>}
      <div className="grid gap-4">
        {items.map((item) => (
          <ConflictCard
            key={item.conflict_id}
            item={item}
            suggestions={details[item.conflict_id]?.suggestions || []}
            onResolve={(missionId, replacementUserId) =>
              onResolve(item.conflict_id, missionId, replacementUserId)
            }
          />
        ))}
      </div>
    </div>
  );
}
