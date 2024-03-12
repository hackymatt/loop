"use client";

import FullCalendar from "@fullcalendar/react";
import dayGridPlugin from "@fullcalendar/daygrid";
import timeGridPlugin from "@fullcalendar/timegrid";
import plLocale from "@fullcalendar/core/locales/pl";
import interactionPlugin from "@fullcalendar/interaction";

// ----------------------------------------------------------------------

export default function AccountScheduleView() {
  return (
    <FullCalendar
      plugins={[dayGridPlugin, timeGridPlugin, interactionPlugin]}
      initialView="timeGridWeek"
      locale={plLocale}
      allDaySlot={false}
      slotDuration="00:15:00"
      slotLabelFormat={{
        hour: "numeric",
        minute: "2-digit",
        omitZeroMinute: false,
      }}
      slotLabelInterval="00:15"
      nowIndicator
      headerToolbar={{
        left: "prev,next today",
        center: "title",
        right: "dayGridMonth,timeGridWeek,timeGridDay",
      }}
      navLinks
      selectable
      select={(selectionInfo) => {
        if (selectionInfo.view.type !== "dayGridMonth") {
          console.log(selectionInfo);
        }
      }}
    />
  );
}
