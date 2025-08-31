import type { CalendarStatus } from "./store";

export type CalendarEvent = {
  id: string;
  title: string;
  start: string;
  end: string;
  status: CalendarStatus;
  userId?: string;
  orgId?: string;
  projectId?: string;
};
