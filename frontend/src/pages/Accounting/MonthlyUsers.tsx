import React from "react";
import {
  fetchMonthlyUsers,
  exportCSV,
  type MonthlyUserItem,
} from "../../api/reports";
import CSVButton from "../../components/CSVButton";

export default function MonthlyUsers() {
  const [orgId, setOrgId] = React.useState<string>("");
  const [projectId, setProjectId] = React.useState<string>("");
  const [dateFrom, setDateFrom] = React.useState<string>("");
  const [dateTo, setDateTo] = React.useState<string>("");
  const [items, setItems] = React.useState<MonthlyUserItem[]>([]);
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);

  const onLoad = async () => {
    setError(null);
    setLoading(true);
    try {
      const data = await fetchMonthlyUsers({
        org_id: orgId,
        project_id: projectId || undefined,
        date_from: dateFrom,
        date_to: dateTo,
      });
      setItems(data.items);
    } catch (e) {
      const msg = e instanceof Error ? e.message : String(e);
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  const onExport = () => {
    exportCSV({
      org_id: orgId,
      project_id: projectId || undefined,
      date_from: dateFrom,
      date_to: dateTo,
    });
  };

  return (
    <div className="p-6 space-y-4">
      <h1 className="text-xl font-semibold">
        Comptabilite - Totaux mensuels par user
      </h1>
      <div className="grid grid-cols-2 md:grid-cols-5 gap-2 items-end">
        <div>
          <label className="text-xs">Org ID</label>
          <input
            value={orgId}
            onChange={(e) => setOrgId(e.target.value)}
            className="w-full border rounded p-2"
            placeholder="org-uuid"
          />
        </div>
        <div>
          <label className="text-xs">Project ID (opt)</label>
          <input
            value={projectId}
            onChange={(e) => setProjectId(e.target.value)}
            className="w-full border rounded p-2"
            placeholder="project-uuid"
          />
        </div>
        <div>
          <label className="text-xs">Date from (YYYY-MM-DD)</label>
          <input
            value={dateFrom}
            onChange={(e) => setDateFrom(e.target.value)}
            className="w-full border rounded p-2"
            placeholder="2025-08-01"
          />
        </div>
        <div>
          <label className="text-xs">Date to (YYYY-MM-DD)</label>
          <input
            value={dateTo}
            onChange={(e) => setDateTo(e.target.value)}
            className="w-full border rounded p-2"
            placeholder="2025-08-31"
          />
        </div>
        <div className="flex gap-2">
          <button
            onClick={onLoad}
            className="px-3 py-2 rounded-2xl shadow border text-sm"
          >
            Charger
          </button>
          <CSVButton onClick={onExport} disabled={!items.length} />
        </div>
      </div>
      {error && <div className="text-red-600 text-sm">{error}</div>}
      {loading ? (
        <div>Chargement...</div>
      ) : (
        <div className="overflow-auto border rounded">
          <table className="min-w-full text-sm">
            <thead className="bg-gray-50">
              <tr>
                <th className="text-left p-2">User</th>
                <th className="text-left p-2">Mois</th>
                <th className="text-right p-2">H Prevues</th>
                <th className="text-right p-2">H Confirmees</th>
                <th className="text-right p-2">Montant EUR</th>
              </tr>
            </thead>
            <tbody>
              {items.map((it, idx) => (
                <tr key={idx} className="odd:bg-white even:bg-gray-50">
                  <td className="p-2">{it.user_name}</td>
                  <td className="p-2">{it.month}</td>
                  <td className="p-2 text-right">
                    {it.hours_planned.toFixed(2)}
                  </td>
                  <td className="p-2 text-right">
                    {it.hours_confirmed.toFixed(2)}
                  </td>
                  <td className="p-2 text-right">{it.amount.toFixed(2)}</td>
                </tr>
              ))}
              {!items.length && (
                <tr>
                  <td className="p-4" colSpan={5}>
                    Aucune donnee
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
