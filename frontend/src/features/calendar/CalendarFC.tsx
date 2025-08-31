import { useMemo, useRef } from "react";
import FullCalendar, {
  EventDropArg,
  EventResizeDoneArg,
} from "@fullcalendar/react";
import dayGridPlugin from "@fullcalendar/daygrid";
import timeGridPlugin from "@fullcalendar/timegrid";
import interactionPlugin from "@fullcalendar/interaction";
import { useCalendarEvents } from "./api";
import { useCalendarFilters } from "./store";
import { STATUS_CLASS } from "./status";
import type { CalendarEvent } from "./types";

function toFc(ev: CalendarEvent) {
  return {
    id: ev.id,
    title: ev.title,
    start: ev.start,
    end: ev.end,
    classNames: STATUS_CLASS[ev.status],
  };
}

export default function CalendarFC() {
  const calRef = useRef<FullCalendar>(null!);
  const { status, userId, orgId, projectId, timezone } = useCalendarFilters();
  const activeStatus = useMemo(
    () =>
      Object.entries(status)
        .filter(([, v]) => v)
        .map(([k]) => k),
    [status],
  );

  const { data } = useCalendarEvents({
    tz: timezone,
    status: activeStatus,
    userId,
    orgId,
    projectId,
  });

  return (
    <div className="p-4">
      <FullCalendar
        ref={calRef}
        plugins={[dayGridPlugin, timeGridPlugin, interactionPlugin]}
        initialView="timeGridWeek"
        headerToolbar={{
          left: "prev,next today",
          center: "title",
          right: "dayGridMonth,timeGridWeek,timeGridDay",
        }}
        timeZone={timezone || "local"}
        editable
        droppable={false}
        selectable={false}
        events={(info, success) => {
          const list = (data ?? []).map(toFc);
          success(list);
        }}
        eventDrop={(arg: EventDropArg) => {
          fetch(`/api/v1/assignments/${arg.event.id}/move`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              id: arg.event.id,
              start: arg.event.start?.toISOString(),
              end: arg.event.end?.toISOString(),
            }),
          }).catch(() => arg.revert());
        }}
        eventResize={(arg: EventResizeDoneArg) => {
          fetch(`/api/v1/assignments/${arg.event.id}/resize`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              id: arg.event.id,
              start: arg.event.start?.toISOString(),
              end: arg.event.end?.toISOString(),
            }),
          }).catch(() => arg.revert());
        }}
        height="auto"
      />
    </div>
  );
}
