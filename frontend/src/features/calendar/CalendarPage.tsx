import Legend from "./Legend";
import CalendarFC from "./CalendarFC";
import TimelineDay from "./Timeline";

export default function CalendarPage() {
  return (
    <div className="space-y-4">
      <h1 className="text-xl font-bold">Planning</h1>
      <Legend />
      <CalendarFC />
      <TimelineDay />
    </div>
  );
}
