// ui.ts - petit store UI (toasts, theme, sidebar)
import { create } from "zustand";

type Toast = { id: string; kind: "info"|"success"|"error"; text: string };

type UiState = {
  theme: "light" | "dark";
  sidebarOpen: boolean;
  toasts: Toast[];
  setTheme: (t: UiState["theme"]) => void;
  toggleSidebar: () => void;
  pushToast: (t: Omit<Toast,"id">) => void;
  removeToast: (id: string) => void;
};

export const useUi = create<UiState>((set) => ({
  theme: "light",
  sidebarOpen: true,
  toasts: [],
  setTheme: (t) => set({ theme: t }),
  toggleSidebar: () => set(s => ({ sidebarOpen: !s.sidebarOpen })),
  pushToast: (t) => set(s => ({ toasts: [...s.toasts, { ...t, id: Math.random().toString(36).slice(2) }] })),
  removeToast: (id) => set(s => ({ toasts: s.toasts.filter(x => x.id !== id) })),
}));
