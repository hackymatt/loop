"use client";

import FullCalendar from "@fullcalendar/react";
import dayGridPlugin from "@fullcalendar/daygrid";
import timeGridPlugin from "@fullcalendar/timegrid";
import plLocale from "@fullcalendar/core/locales/pl";
import { CalendarOptions } from "@fullcalendar/core";
import interactionPlugin from "@fullcalendar/interaction";

import { styled } from "@mui/material/styles";

// ----------------------------------------------------------------------

export default function Calendar(props: CalendarOptions) {
  const StyledContent = styled("div")(
    ({ theme }) => `
    .fc .fc-button {
      font-family: ${theme.typography.body2.fontFamily};
      font-size: ${theme.typography.body2.fontSize};
      line-height: ${theme.typography.body2.lineHeight};
    }
    .fc .fc-button-primary {
      background-color: ${theme.palette.primary.main};
      border-color: ${theme.palette.primary.main};
    }
    .fc .fc-button-primary:not(:disabled).fc-button-active,
    .fc .fc-button-primary:not(:disabled):active {
      background-color: ${theme.palette.primary.darker};
      border-color: ${theme.palette.primary.darker};
    }
    .fc .fc-day-today {
      background-color: ${theme.palette.grey[200]};
    }
    .fc-timegrid-slot:hover {
      background: ${theme.palette.primary.lighter}; 
      cursor: pointer;
    }
    .fc-event {
      cursor: pointer;
    }
    .fc-toolbar-title {
      font-family: ${theme.typography.h4.fontFamily};
      font-size: ${theme.typography.h4.fontSize};
      line-height: ${theme.typography.h4.lineHeight};
    }
    .fc-col-header-cell-cushion,
    .fc-timegrid-slot-label-cushion{
      font-family: ${theme.typography.body2.fontFamily};
      font-size: ${theme.typography.body2.fontSize};
      line-height: ${theme.typography.body2.lineHeight};
    }
    @media (max-width: 800px) {
      .fc-header-toolbar {
        flex-direction: column;
      }
    }
  `,
  );

  return (
    <StyledContent>
      <FullCalendar
        plugins={[dayGridPlugin, timeGridPlugin, interactionPlugin]}
        locale={plLocale}
        allDaySlot={false}
        slotLabelFormat={{
          hour: "numeric",
          minute: "2-digit",
          omitZeroMinute: false,
        }}
        eventTimeFormat={{
          hour: "numeric",
          minute: "2-digit",
          omitZeroMinute: false,
        }}
        nowIndicator
        navLinks
        {...props}
      />
    </StyledContent>
  );
}
