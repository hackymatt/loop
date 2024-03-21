import { format } from "date-fns";
import { AxiosError } from "axios";
import { formatInTimeZone } from "date-fns-tz";
import { useMemo, useState, useEffect } from "react";

import { LoadingButton } from "@mui/lab";
import {
  Dialog,
  Button,
  DialogTitle,
  DialogProps,
  DialogContent,
  DialogActions,
} from "@mui/material";

import { getTimezone } from "src/utils/get-timezone";

import { useCreateReservation } from "src/api/reservations/reservations";
import { useLessonLecturers } from "src/api/lesson-lecturers/lesson-lecturers";
import { useLessonSchedules } from "src/api/lesson-schedules/lesson-schedules";

import Schedule from "src/components/schedule";
import { useToastContext } from "src/components/toast";

import { IScheduleProp } from "src/types/course";
import { ITeamMemberProps } from "src/types/team";
import { IPurchaseItemProp } from "src/types/purchase";

// ----------------------------------------------------------------------

interface Props extends DialogProps {
  purchase: IPurchaseItemProp;
  onClose: VoidFunction;
}

const DEFAULT_USER = { id: "", avatarUrl: "", name: "Wszyscy" } as const;

// ----------------------------------------------------------------------

export default function ReservationAddForm({ purchase, onClose, ...other }: Props) {
  const { enqueueSnackbar } = useToastContext();

  const { mutateAsync: createReservation, isLoading: isSubmitting } = useCreateReservation();
  const { data: lessonLecturers, isLoading: isLoadingUsers } = useLessonLecturers({
    lesson_id: purchase?.id,
    page_size: 1000,
  });

  const users = useMemo(
    () =>
      lessonLecturers
        ? [
            DEFAULT_USER,
            ...lessonLecturers.map((teacher: ITeamMemberProps) => ({
              ...teacher,
              avatarUrl:
                teacher.gender === "Kobieta"
                  ? "/assets/images/avatar/avatar_female.jpg"
                  : "/assets/images/avatar/avatar_male.jpg",
            })),
          ]
        : [],
    [lessonLecturers],
  );

  const [error, setError] = useState<string | undefined>();
  const [user, setUser] = useState<ITeamMemberProps>(DEFAULT_USER);
  const [date, setDate] = useState<string>(format(new Date(), "yyyy-MM-dd"));

  const { data: lessonSchedules, isLoading: isLoadingTimeSlots } = useLessonSchedules({
    lecturer_id: user.id,
    lesson_id: purchase?.id,
    duration: purchase?.lessonDuration,
    time: date,
    sort_by: "start_time",
    page_size: 48,
  });

  const slots = useMemo(
    () =>
      lessonSchedules?.map((lessonSchedule: IScheduleProp) => {
        const dt = new Date(lessonSchedule.startTime);
        return formatInTimeZone(dt, getTimezone(), "HH:mm");
      }),
    [lessonSchedules],
  );

  const [slot, setSlot] = useState<string>(slots?.[0]);

  useEffect(() => {
    if (slots) {
      setSlot(slots[0]);
    }
  }, [slots]);

  const onSubmit = async () => {
    if (date && slot) {
      const dt = new Date(`${date}T${slot}:00Z`);
      const time = new Date(dt.valueOf() + dt.getTimezoneOffset() * 60 * 1000);
      const startTime = formatInTimeZone(time, "UTC", "yyyy-MM-dd'T'HH:mm:ss'Z'");
      const schedule = lessonSchedules.find(
        (lessonSchedule: IScheduleProp) => lessonSchedule.startTime === startTime,
      );
      if (schedule) {
        try {
          await createReservation({ lesson: purchase.id, schedule: schedule.id });
          setError(undefined);
          onClose();
          enqueueSnackbar("Rezerwacja została dodana", { variant: "success" });
        } catch (err) {
          setError((err as AxiosError).message);
        }
      }
    }
  };

  return (
    <Dialog fullWidth maxWidth="sm" onClose={onClose} {...other}>
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
          isLoadingUsers={isLoadingUsers}
          isLoadingTimeSlots={isLoadingTimeSlots}
          error={error}
        />
      </DialogContent>

      <DialogActions>
        <Button variant="outlined" onClick={onClose} color="inherit">
          Anuluj
        </Button>
        <LoadingButton
          color="success"
          type="submit"
          variant="contained"
          onClick={onSubmit}
          disabled={!slot}
          loading={isSubmitting}
        >
          Zarezerwuj
        </LoadingButton>
      </DialogActions>
    </Dialog>
  );
}
