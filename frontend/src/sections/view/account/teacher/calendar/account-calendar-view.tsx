"use client";

import stc from "string-to-color";
import { format, startOfDay } from "date-fns";
import { formatInTimeZone } from "date-fns-tz";
import { useMemo, useState, useCallback } from "react";
import { DatesSetArg, DateSelectArg, EventClickArg } from "@fullcalendar/core";

import { useBoolean } from "src/hooks/use-boolean";
import { useQueryParams } from "src/hooks/use-query-params";

import { getTimezone } from "src/utils/get-timezone";

import { useDeleteSchedule } from "src/api/schedules/schedule";
import { useSchedules, useCreateSchedule } from "src/api/schedules/schedules";

import { useToastContext } from "src/components/toast";
import Calendar from "src/components/calendar/calendar";

import { IScheduleProp } from "src/types/course";

import DetailsForm from "./details-form";
// ----------------------------------------------------------------------

const AVAILABLE_STATUS = "Dostępny" as const;

const SLOT_SIZE = 30 as number;

// ----------------------------------------------------------------------
export default function AccountScheduleView() {
  const { enqueueSnackbar } = useToastContext();

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
    return formatInTimeZone(datePoint, getTimezone(), "HH:mm:ss");
  }, []);

  const detailsFormOpen = useBoolean();

  const [scrollTime, setScrollTime] = useState<string>();
  const [eventDetails, setEventDetails] = useState<EventClickArg>();

  const { setQueryParam, getQueryParams } = useQueryParams();

  const allFilters = useMemo(() => getQueryParams(), [getQueryParams]);

  const { view, ...filters } = allFilters;

  const slotsCount = useMemo(() => getSlotsCount(view), [getSlotsCount, view]);

  const { data: schedules } = useSchedules({
    ...filters,
    reserved: view === "month" ? "True" : "",
    page_size: slotsCount * (60 / SLOT_SIZE) * 24,
    sort_by: "start_time",
  });
  const { mutateAsync: addTimeSlot } = useCreateSchedule();
  const { mutateAsync: deleteTimeSlot, isLoading: isSubmitting } = useDeleteSchedule();

  const events = useMemo(
    () =>
      schedules?.map((schedule: IScheduleProp) => {
        const isConfirmed = !!schedule?.meetingUrl;
        const base = {
          id: schedule.id,
          groupId: "1",
          title: schedule.lesson?.title ?? AVAILABLE_STATUS,
          start: schedule.startTime,
          end: schedule.endTime,
          color: schedule.lesson?.title ? stc(schedule.lesson.title) : "",
          url: "",
        };
        const isReserved = base.title !== AVAILABLE_STATUS;
        const reserved = isReserved
          ? {
              ...base,
              extendedProps: {
                ready: schedule.studentsRequired === 0,
                students: schedule?.students ?? [],
              },
            }
          : base;
        return isConfirmed
          ? {
              ...reserved,
              url: schedule?.meetingUrl,
            }
          : reserved;
      }),
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

  const handleAddTimeSlot = useCallback(
    async (selectionInfo: DateSelectArg) => {
      try {
        await addTimeSlot({ start_time: selectionInfo.startStr, end_time: selectionInfo.endStr });
        setScrollTime(getTime(selectionInfo.start));
      } catch {
        enqueueSnackbar("Wystąpił błąd podczas dodawania terminu", { variant: "error" });
      }
    },
    [addTimeSlot, enqueueSnackbar, getTime],
  );

  const handleDeleteTimeSlot = useCallback(
    async (eventInfo: EventClickArg) => {
      try {
        await deleteTimeSlot({ id: eventInfo.event.id });
        setScrollTime(getTime(new Date(eventInfo.event.start!)));
      } catch {
        enqueueSnackbar("Wystąpił błąd podczas usuwania terminu", { variant: "error" });
      }
    },
    [deleteTimeSlot, enqueueSnackbar, getTime],
  );

  const handleEventClick = useCallback(
    async (eventInfo: EventClickArg) => {
      eventInfo.jsEvent.preventDefault();
      setEventDetails(eventInfo);
      if (eventInfo.event.title === AVAILABLE_STATUS) {
        handleDeleteTimeSlot(eventInfo);
      } else {
        detailsFormOpen.onToggle();
      }
    },
    [handleDeleteTimeSlot, detailsFormOpen],
  );

  return (
    <>
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
        selectAllow={(selectInfo) => {
          const duration = selectInfo.end.getTime() - selectInfo.start.getTime();
          return duration === SLOT_SIZE * 60 * 1000;
        }}
        select={handleAddTimeSlot}
        initialDate={filters?.time_from ?? undefined}
        datesSet={handleChange}
        events={events}
        eventClick={handleEventClick}
        displayEventTime={view === "month"}
        scrollTime={scrollTime}
        slotMinTime="06:00:00"
        slotMaxTime="22:00:00"
      />

      {eventDetails && (
        <DetailsForm
          eventDetails={eventDetails!}
          isLoading={isSubmitting}
          open={detailsFormOpen.value}
          onConfirm={handleDeleteTimeSlot}
          onClose={detailsFormOpen.onFalse}
        />
      )}
    </>
  );
}
