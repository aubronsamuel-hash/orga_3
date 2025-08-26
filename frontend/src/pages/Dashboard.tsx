import { useState } from "react";
import { useAuth } from "../auth";
import { api } from "../lib/api";

export function Dashboard() {
  const { user, logout } = useAuth();
  const [msg, setMsg] = useState<string>("");

  const loadProjects = async () => {
    try {
      const data = await api.get<{items: {id:string}[]}>('/projects');
      setMsg(`Projets: ${data.items.length}`);
    } catch (e) {
      setMsg("Erreur chargement projets");
    }
  };

  return (
    <section>
      <h1 className="text-2xl font-bold mb-2">Dashboard</h1>
      <p className="mb-2">Bonjour {user?.email}</p>
      <div className="flex gap-2">
        <button onClick={loadProjects} className="px-3 py-1 rounded border">Charger projets</button>
        <button onClick={() => void logout()} className="px-3 py-1 rounded border">Logout</button>
      </div>
      {msg && <p className="mt-2">{msg}</p>}
    </section>
  );
}
