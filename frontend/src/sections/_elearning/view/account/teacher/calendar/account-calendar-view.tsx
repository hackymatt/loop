"use client";

import { format, startOfDay } from "date-fns";
import { useMemo, useState, useCallback } from "react";
import { DatesSetArg, DateSelectArg, EventClickArg } from "@fullcalendar/core";

import { useQueryParams } from "src/hooks/use-query-params";

import { useDeleteSchedule } from "src/api/schedule/schedule";
import { useSchedules, useCreateSchedule } from "src/api/schedule/schedules";

import Calendar from "src/components/calendar/calendar";

import { IScheduleProp } from "src/types/course";

// ----------------------------------------------------------------------

const AVAILABLE_STATUS = "Dostępny" as const;

const SLOT_SIZE = 30 as number;

// ----------------------------------------------------------------------
export default function AccountScheduleView() {
  const getViewName = useCallback((dateInfo: DatesSetArg): string | undefined => {
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
  }, []);

  const getViewType = useCallback((viewName: string | undefined): string | undefined => {
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
  }, []);

  const getSlotsCount = useCallback((viewName: string | undefined): number => {
    switch (viewName) {
      case "month":
        return 31;
      case "week":
        return 7;
      case "day":
        return 1;
      default:
        return 10;
    }
  }, []);

  const getTime = useCallback((datePoint: Date): string => {
    datePoint.setHours(datePoint.getHours() - 3);
    return format(datePoint, "HH:mm:ss");
  }, []);

  const [scrollTime, setScrollTime] = useState<string>();
  const [eventId, setEventId] = useState<string>();

  const { setQueryParam, getQueryParams } = useQueryParams();

  const allFilters = useMemo(() => getQueryParams(), [getQueryParams]);

  const { view, ...filters } = allFilters;

  const slotsCount = useMemo(() => getSlotsCount(view), [getSlotsCount, view]);

  const { data: schedules } = useSchedules({
    ...filters,
    reserved: (view === "month").toString(),
    page_size: slotsCount * (60 / SLOT_SIZE) * 24,
    sort_by: "start_time",
  });
  const { mutateAsync: addTimeSlot } = useCreateSchedule();
  const { mutateAsync: deleteTimeSlot } = useDeleteSchedule(eventId!);

  const events = useMemo(
    () =>
      schedules?.map((schedule: IScheduleProp) => ({
        id: schedule.id,
        groupId: "1",
        title: schedule.lesson?.title ?? AVAILABLE_STATUS,
        start: schedule.startTime,
        end: schedule.endTime,
      })),
    [schedules],
  );

  const handleTimeChange = useCallback(
    (dateInfo: DatesSetArg) => {
      const dateStart = dateInfo.start;
      if (dateInfo.view.type === "dayGridMonth") {
        if (dateStart.getDate() !== 1) {
          dateStart.setMonth(dateStart.getMonth() + 1, 1);
          setQueryParam("time_from", format(startOfDay(dateStart), "yyyy-MM-dd"));
          return;
        }
      }
      setQueryParam("time_from", dateInfo.startStr.slice(0, 10));
    },
    [setQueryParam],
  );

  const handleViewChange = useCallback(
    (dateInfo: DatesSetArg) => {
      setQueryParam("view", getViewName(dateInfo));
    },
    [getViewName, setQueryParam],
  );

  const handleChange = useCallback(
    (dateInfo: DatesSetArg) => {
      handleTimeChange(dateInfo);
      handleViewChange(dateInfo);
    },
    [handleTimeChange, handleViewChange],
  );

  const handleAddTimeSlot = async (selectionInfo: DateSelectArg) => {
    await addTimeSlot({ start_time: selectionInfo.startStr, end_time: selectionInfo.endStr });
    setScrollTime(getTime(selectionInfo.start));
  };

  const handleDeleteTimeSlot = async (eventInfo: EventClickArg) => {
    if (eventInfo.event.title === AVAILABLE_STATUS) {
      setEventId(eventInfo.event.id);
      await deleteTimeSlot({});
      setScrollTime(getTime(new Date(eventInfo.event.start!)));
    }
  };

  return (
    <Calendar
      initialView={getViewType(view) || "timeGridWeek"}
      slotDuration={`00:${SLOT_SIZE}:00`}
      slotLabelInterval={`00:${SLOT_SIZE}`}
      headerToolbar={{
        left: "prev,next",
        center: "title",
        right: "today dayGridMonth,timeGridWeek,timeGridDay",
      }}
      selectable
      select={handleAddTimeSlot}
      initialDate={filters?.time_from ?? undefined}
      datesSet={handleChange}
      events={events}
      eventClick={handleDeleteTimeSlot}
      displayEventTime={view === "month"}
      scrollTime={scrollTime}
      slotMinTime="06:00:00"
      slotMaxTime="22:00:00"
    />
  );
}
