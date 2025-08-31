import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { http } from "../../lib/http";
import type { CalendarEvent } from "./types";

export function useCalendarEvents(params: {
  from?: string;
  to?: string;
  tz?: string;
  status?: string[];
  userId?: string;
  orgId?: string;
  projectId?: string;
}) {
  return useQuery({
    queryKey: ["calendar", params],
    queryFn: () =>
      http<CalendarEvent[]>("/api/v1/calendar", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(params),
      }),
    refetchInterval: 30_000,
  });
}

export function useMoveEvent() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (p: { id: string; start: string; end: string }) =>
      http(`/api/v1/assignments/${p.id}/move`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(p),
      }),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["calendar"] }),
  });
}

export function useResizeEvent() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (p: { id: string; start: string; end: string }) =>
      http(`/api/v1/assignments/${p.id}/resize`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(p),
      }),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["calendar"] }),
  });
}
