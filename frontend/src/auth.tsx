import { createContext, useContext, useEffect, useState, ReactNode } from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { api } from "./lib/api";

type User = { id: string; email: string };
type AuthCtx = {
  user: User | null;
  status: "idle"|"loading"|"auth"|"guest";
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
};
const Ctx = createContext<AuthCtx | null>(null);

function useMeQuery() {
  return useQuery({
    queryKey: ["me"],
    queryFn: async () => {
      return await api.get<User>("/auth/me");
    },
    retry: false
  });
}

function AuthInner({ children }: { children: ReactNode }) {
  const qc = useQueryClient();
  const { data, isLoading, isError } = useMeQuery();
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => { if (data) setUser(data); }, [data]);

  const login = async (email: string, password: string) => {
    await api.post("/auth/login", { email, password });
    await qc.invalidateQueries({ queryKey: ["me"] });
    const me = await qc.fetchQuery({ queryKey: ["me"], queryFn: () => api.get<User>("/auth/me") });
    setUser(me);
  };

  const logout = async () => {
    await api.post("/auth/logout");
    setUser(null);
    await qc.setQueryData(["me"], null);
  };

  const status: AuthCtx["status"] =
    isLoading ? "loading" : user ? "auth" : isError ? "guest" : user ? "auth" : "guest";

  return (
    <Ctx.Provider value={{ user, status, login, logout }}>
      {children}
    </Ctx.Provider>
  );
}

export function AuthProvider({ children }: { children: ReactNode }) {
  return <AuthInner>{children}</AuthInner>;
}

export function useAuth(): AuthCtx {
  const ctx = useContext(Ctx);
  if (!ctx) throw new Error("AuthProvider manquant");
  return ctx;
}
