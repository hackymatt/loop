"use client";

import Calendar from "src/components/calendar/calendar";

// ----------------------------------------------------------------------

export default function AccountScheduleView() {
  return (
    <Calendar
      initialView="timeGridWeek"
      slotDuration="00:15:00"
      slotLabelInterval="00:15"
      headerToolbar={{
        left: "prev,next",
        center: "title",
        right: "today dayGridMonth,timeGridWeek,timeGridDay",
      }}
      selectable
      select={(selectionInfo) => {
        if (selectionInfo.view.type !== "dayGridMonth") {
          console.log(selectionInfo);
        }
      }}
    />
  );
}
