import { create } from "zustand";

export type CalendarStatus = "INVITED" | "ACCEPTED" | "DECLINED" | "CANCELLED";

type Filters = {
  status: Record<CalendarStatus, boolean>;
  userId?: string;
  orgId?: string;
  projectId?: string;
  timezone: string;
  setStatus: (s: CalendarStatus, v: boolean) => void;
  setFilter: (k: "userId" | "orgId" | "projectId", v?: string) => void;
  setTimezone: (tz: string) => void;
  reset: () => void;
};

export const useCalendarFilters = create<Filters>((set) => ({
  status: { INVITED: true, ACCEPTED: true, DECLINED: false, CANCELLED: false },
  timezone: Intl.DateTimeFormat().resolvedOptions().timeZone || "UTC",
  setStatus: (s, v) => set((st) => ({ status: { ...st.status, [s]: v } })),
  setFilter: (k, v) => set(() => ({ [k]: v }) as Partial<Filters>),
  setTimezone: (tz) => set(() => ({ timezone: tz })),
  reset: () =>
    set({
      status: {
        INVITED: true,
        ACCEPTED: true,
        DECLINED: false,
        CANCELLED: false,
      },
      userId: undefined,
      orgId: undefined,
      projectId: undefined,
    }),
}));
