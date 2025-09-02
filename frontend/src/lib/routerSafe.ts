import * as React from "react";

// React Router 6: certains consumers lisent le contexte interne.
// Hors Router, le useContext retourne null -> on retourne des valeurs par defaut.
export function useSafeBasename(defaultBase: string = "/"): string {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const ctx: any = (React as unknown as { useContext: typeof React.useContext }).useContext(
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    (React as any)?.Router ?? ({} as any)
  );
  // Fallback generique: si le contexte est null/undefined, on renvoie defaultBase
  // et on n'essaie pas de destructurer.
  const base = (ctx && (ctx as { basename?: string }).basename) ?? defaultBase;
  return typeof base === "string" ? base : defaultBase;
}

