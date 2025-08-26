import { Navigate, useLocation } from "react-router-dom";
import { useAuth } from "../auth";

export function Protected({ children }: { children: JSX.Element }) {
  const { status } = useAuth();
  const loc = useLocation();
  if (status === "loading") return <p>Chargement...</p>;
  if (status !== "auth") return <Navigate to="/login" state={{ from: loc }} replace />;
  return children;
}
