import React from "react";
import type { ConflictItem, Suggestion } from "../../services/conflicts";

type Props = {
  item: ConflictItem;
  suggestions: Suggestion[];
  onResolve: (missionId: number, replacementUserId: number) => void;
};

export default function ConflictCard({ item, suggestions, onResolve }: Props) {
  return (
    <div className="rounded-2xl shadow p-4 border">
      <div className="text-lg font-semibold">Conflit: {item.user_name} ({item.reason})</div>
      <div className="text-sm mt-1">Missions: {item.mission_ids.join(", ")}</div>
      <div className="text-sm">Fenetre: {new Date(item.window.start).toLocaleString()} - {new Date(item.window.end).toLocaleString()}</div>
      <div className="mt-3">
        <div className="font-medium">Suggestions</div>
        <div className="flex flex-wrap gap-2 mt-2">
          {suggestions.map((s) => (
            <button
              key={s.user_id}
              className="px-3 py-1 rounded-xl border"
              onClick={() => onResolve(item.mission_ids[0], s.user_id)}
            >
              Remplacer par {s.user_name}
            </button>
          ))}
          {suggestions.length === 0 && (
            <span className="text-gray-500 text-sm">Aucune suggestion</span>
          )}
        </div>
      </div>
    </div>
  );
}
