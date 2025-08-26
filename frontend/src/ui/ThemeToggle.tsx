import { useEffect, useState } from "react";

export function ThemeToggle() {
  const [dark, setDark] = useState(false);
  useEffect(() => {
    const el = document.documentElement;
    if (dark) el.classList.add("dark");
    else el.classList.remove("dark");
  }, [dark]);
  return (
    <button
      aria-label="Toggle theme"
      className="px-3 py-1 rounded border"
      onClick={() => setDark(d => !d)}
    >
      {dark ? "Dark" : "Light"}
    </button>
  );
}
