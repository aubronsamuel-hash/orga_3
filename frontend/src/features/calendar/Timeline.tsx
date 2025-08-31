import { useMemo } from "react";
import { useCalendarEvents } from "./api";
import { useCalendarFilters } from "./store";
import { STATUS_CLASS } from "./status";

export default function TimelineDay() {
  const { timezone } = useCalendarFilters();
  const { data } = useCalendarEvents({ tz: timezone });
  const hours = useMemo(() => Array.from({ length: 24 }, (_, i) => i), []);
  return (
    <div className="p-4">
      <div className="mb-2 font-semibold">Timeline (Day)</div>
      <div className="relative border rounded overflow-hidden">
        <div
          className="grid"
          style={{ gridTemplateColumns: "repeat(24, minmax(60px,1fr))" }}
        >
          {hours.map((h) => (
            <div key={h} className="border-r text-xs text-center py-1">
              {h}:00
            </div>
          ))}
        </div>
        <div className="relative">
          {(data ?? []).map((e) => {
            const start = new Date(e.start);
            const end = new Date(e.end);
            const left =
              (start.getHours() + start.getMinutes() / 60) * (100 / 24);
            const width =
              ((end.getTime() - start.getTime()) / (1000 * 60 * 60)) *
              (100 / 24);
            return (
              <div
                key={e.id}
                className={`absolute top-2 h-8 text-white px-2 flex items-center fc-event ${STATUS_CLASS[e.status]}`}
                style={{ left: `${left}%`, width: `${width}%` }}
                title={e.title}
              >
                {e.title}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
