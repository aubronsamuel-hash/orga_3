import { Outlet, Link } from "react-router-dom";
import { ThemeToggle } from "./ThemeToggle";
import { Shortcuts } from "./Shortcuts";

export function AppLayout() {
  return (
    <div className="min-h-screen flex flex-col">
      <Shortcuts />
      <header className="border-b bg-white/70 backdrop-blur">
        <div className="max-w-6xl mx-auto px-4 h-14 flex items-center justify-between">
          <Link to="/" className="font-semibold">Coulisses Crew</Link>
          <nav className="flex items-center gap-4">
            <Link to="/login" className="hover:underline">Login</Link>
            <ThemeToggle/>
          </nav>
        </div>
      </header>
      <main className="flex-1 max-w-6xl mx-auto px-4 py-6">
        <Outlet />
      </main>
      <footer className="border-t text-sm text-gray-500 py-3">
        <div className="max-w-6xl mx-auto px-4">v0.1.0</div>
      </footer>
    </div>
  );
}
