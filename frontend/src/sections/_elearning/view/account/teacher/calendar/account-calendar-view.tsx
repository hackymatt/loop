"use client";

import { useMemo } from "react";
import { format, startOfDay } from "date-fns";
import { DatesSetArg } from "@fullcalendar/core";

import { useQueryParams } from "src/hooks/use-query-params";

import { useSchedules } from "src/api/schedule/schedules";

import Calendar from "src/components/calendar/calendar";

// ----------------------------------------------------------------------
export default function AccountScheduleView() {
  const { setQueryParam, getQueryParams } = useQueryParams();

  const allFilters = useMemo(() => getQueryParams(), [getQueryParams]);

  const { view, ...filters } = allFilters;

  const { data: schedules } = useSchedules(filters);

  const getViewName = (dateInfo: DatesSetArg): string | undefined => {
    switch (dateInfo.view.type) {
      case "dayGridMonth":
        return "month";
      case "timeGridWeek":
        return "week";
      case "timeGridDay":
        return "day";
      default:
        return undefined;
    }
  };

  const getViewType = (viewName: string | undefined): string | undefined => {
    switch (viewName) {
      case "month":
        return "dayGridMonth";
      case "week":
        return "timeGridWeek";
      case "day":
        return "timeGridDay";
      default:
        return undefined;
    }
  };

  const handleTimeChange = (dateInfo: DatesSetArg) => {
    const dateStart = dateInfo.start;
    if (dateInfo.view.type === "dayGridMonth") {
      if (dateStart.getDate() !== 1) {
        dateStart.setMonth(dateStart.getMonth() + 1, 1);
        setQueryParam("time_from", format(startOfDay(dateStart), "yyyy-MM-dd"));
        return;
      }
    }
    setQueryParam("time_from", dateInfo.startStr.slice(0, 10));
  };

  const handleViewChange = (dateInfo: DatesSetArg) => {
    setQueryParam("view", getViewName(dateInfo));
  };

  return (
    <Calendar
      initialView={getViewType(view) || "timeGridWeek"}
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
      initialDate={filters?.time_from ?? undefined}
      datesSet={(dateInfo) => {
        handleTimeChange(dateInfo);
        handleViewChange(dateInfo);
      }}
    />
  );
}
