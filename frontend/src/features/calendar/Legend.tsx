import { useCalendarFilters, type CalendarStatus } from "./store";
import { STATUS_LABEL } from "./status";

export default function Legend() {
  const { status, setStatus } = useCalendarFilters();
  const items: CalendarStatus[] = [
    "INVITED",
    "ACCEPTED",
    "DECLINED",
    "CANCELLED",
  ];
  return (
    <div className="flex gap-4 items-center text-sm">
      {items.map((s) => (
        <label key={s} className="inline-flex items-center gap-2">
          <input
            type="checkbox"
            checked={status[s]}
            onChange={(e) => setStatus(s, e.target.checked)}
          />
          <span>{STATUS_LABEL[s]}</span>
        </label>
      ))}
    </div>
  );
}
