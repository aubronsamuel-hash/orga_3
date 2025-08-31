import type { CalendarStatus } from "./store";

export const STATUS_LABEL: Record<CalendarStatus, string> = {
  INVITED: "Invited",
  ACCEPTED: "Accepted",
  DECLINED: "Declined",
  CANCELLED: "Cancelled",
};

export const STATUS_CLASS: Record<CalendarStatus, string> = {
  INVITED: "cc-evt-invited",
  ACCEPTED: "cc-evt-accepted",
  DECLINED: "cc-evt-declined",
  CANCELLED: "cc-evt-cancelled",
};
