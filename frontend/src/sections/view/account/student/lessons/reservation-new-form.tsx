import { format } from "date-fns";
import { AxiosError } from "axios";
import { formatInTimeZone } from "date-fns-tz";
import { useMemo, useState, useEffect } from "react";

import {
  Dialog,
  Button,
  DialogTitle,
  DialogProps,
  DialogContent,
  DialogActions,
} from "@mui/material";

import { useBoolean } from "src/hooks/use-boolean";

import { getTimezone } from "src/utils/get-timezone";
import { getGenderAvatar } from "src/utils/get-gender-avatar";

import { useLessonDates } from "src/api/lesson-dates/lesson-dates";
import { useCreateReservation } from "src/api/reservations/reservations";
import { useLessonLecturers } from "src/api/lesson-lecturers/lesson-lecturers";
import { useLessonSchedules } from "src/api/lesson-schedules/lesson-schedules";

import Schedule from "src/components/schedule";
import { useToastContext } from "src/components/toast";

import { IScheduleProp } from "src/types/course";
import { ITeamMemberProps } from "src/types/team";
import { IPurchaseItemProp } from "src/types/purchase";

import ReservationConfirmForm from "./reservation-confirm-form";

// ----------------------------------------------------------------------

interface Props extends DialogProps {
  purchase: IPurchaseItemProp;
  onClose: VoidFunction;
}

type SlotProps = { time: string; studentsRequired: number };

const DEFAULT_USER = { id: "", avatarUrl: "", name: "Wszyscy" } as const;

// ----------------------------------------------------------------------

export default function ReservationNewForm({ purchase, onClose, ...other }: Props) {
  const confirmReservationFormOpen = useBoolean();

  const { enqueueSnackbar } = useToastContext();

  const { mutateAsync: createReservation, isLoading: isSubmitting } = useCreateReservation();
  const { data: lessonLecturers, isLoading: isLoadingUsers } = useLessonLecturers({
    lesson_id: purchase?.lessonId,
    page_size: 1000,
  });

  const users = useMemo(
    () =>
      lessonLecturers
        ? [
            DEFAULT_USER,
            ...lessonLecturers.map((teacher: ITeamMemberProps) => ({
              ...teacher,
              avatarUrl: teacher.avatarUrl || getGenderAvatar(teacher.gender),
            })),
          ]
        : [],
    [lessonLecturers],
  );

  const today = useMemo(() => format(new Date(), "yyyy-MM-dd"), []);
  const currentYearMonth = useMemo(() => format(new Date(), "yyyy-MM"), []);
  const [error, setError] = useState<string | undefined>();
  const [user, setUser] = useState<ITeamMemberProps>(DEFAULT_USER);
  const [date, setDate] = useState<string>(today);
  const [yearMonth, setYearMonth] = useState<string>(currentYearMonth);

  const queryParams = useMemo(
    () => ({
      lecturer_id: user.id,
      lesson_id: purchase?.lessonId,
      duration: purchase?.lessonDuration,
      time: date,
      sort_by: "start_time",
      page_size: 48,
    }),
    [date, purchase?.lessonDuration, purchase?.lessonId, user.id],
  );

  const dateQueryParams = useMemo(
    () => ({
      lecturer_id: queryParams.lecturer_id,
      lesson_id: queryParams.lesson_id,
      duration: queryParams.duration,
      year_month: yearMonth,
      page_size: -1,
    }),
    [queryParams.duration, queryParams.lecturer_id, queryParams.lesson_id, yearMonth],
  );

  const { data: lessonSchedules, isLoading: isLoadingTimeSlots } = useLessonSchedules(
    date === today ? { ...queryParams, reserved: "True" } : queryParams,
  );

  const { data: lessonDates, isLoading: isLoadingDates } = useLessonDates(dateQueryParams);

  const slots = useMemo(() => {
    const allSlots = lessonSchedules?.map((lessonSchedule: IScheduleProp) => {
      const dt = new Date(lessonSchedule.startTime);
      return {
        time: formatInTimeZone(dt, getTimezone(), "HH:mm"),
        studentsRequired: lessonSchedule.studentsRequired,
      };
    });

    const filteredSlots = Object.values(
      allSlots?.reduce((acc: { [key: string]: SlotProps }, slot) => {
        if (!acc[slot.time] || slot.studentsRequired < acc[slot.time].studentsRequired) {
          acc[slot.time] = slot;
        }
        return acc;
      }, {}) ?? {},
    );

    return Array.from(new Set(filteredSlots)).sort();
  }, [lessonSchedules]);

  const [slot, setSlot] = useState<string>(slots?.[0]?.time);

  useEffect(() => {
    if (slots) {
      setSlot(slots[0]?.time);
    }
  }, [slots]);

  const onSubmit = async () => {
    if (date && slot) {
      const dt = new Date(`${date}T${slot}:00Z`);
      const time = new Date(dt.valueOf() + dt.getTimezoneOffset() * 60 * 1000);
      const startTime = formatInTimeZone(time, "UTC", "yyyy-MM-dd'T'HH:mm:ss'Z'");
      const schedules = lessonSchedules.filter(
        (lessonSchedule: IScheduleProp) => lessonSchedule.startTime === startTime,
      );
      const schedule = schedules.reduce((min: IScheduleProp, lessonSchedule: IScheduleProp) =>
        lessonSchedule.studentsRequired < min.studentsRequired ? lessonSchedule : min,
      );
      if (schedule) {
        try {
          await createReservation({
            lesson: purchase.lessonId,
            schedule: schedule.id,
            purchase: purchase.id,
          });
          setError(undefined);
          confirmReservationFormOpen.onFalse();
          onClose();
          enqueueSnackbar("Rezerwacja została dodana", { variant: "success" });
        } catch (err) {
          setError((err as AxiosError).message);
        }
      }
    }
  };

  return (
    <>
      <Dialog fullWidth maxWidth="sm" onClose={onClose} sx={{ height: "fit-content" }} {...other}>
        <DialogTitle sx={{ typography: "h5", pb: 3 }}>{purchase?.lessonTitle}</DialogTitle>

        <DialogContent sx={{ py: 0 }}>
          <Schedule
            availableUsers={users}
            currentUser={user}
            onUserChange={(event, userId) => setUser(users.find((u) => u.id === userId)!)}
            currentDate={date}
            onDateChange={(selectedDate) => setDate(format(selectedDate, "yyyy-MM-dd"))}
            availableTimeSlots={slots ?? []}
            currentSlot={slot}
            onSlotChange={(event, selectedSlot) => setSlot(selectedSlot)}
            availableDates={lessonDates ?? []}
            onMonthChange={(month) => {
              setYearMonth(month);
            }}
            isLoadingUsers={isLoadingUsers}
            isLoadingTimeSlots={isLoadingTimeSlots || isLoadingDates}
            error={error}
          />
        </DialogContent>

        <DialogActions>
          <Button variant="outlined" onClick={onClose} color="inherit">
            Anuluj
          </Button>
          <Button
            color="success"
            type="submit"
            variant="contained"
            onClick={() => confirmReservationFormOpen.onToggle()}
            disabled={!slot}
          >
            Zarezerwuj
          </Button>
        </DialogActions>
      </Dialog>

      <ReservationConfirmForm
        loading={isSubmitting}
        open={confirmReservationFormOpen.value}
        onConfirm={onSubmit}
        onClose={confirmReservationFormOpen.onFalse}
      />
    </>
  );
}
