import { format } from "date-fns";
import { polishPlurals } from "polish-plurals";
import { formatInTimeZone } from "date-fns-tz";
import { useMemo, useState, useEffect } from "react";

import { LoadingButton } from "@mui/lab";
import Typography from "@mui/material/Typography";
import AccordionDetails from "@mui/material/AccordionDetails";
import Accordion, { accordionClasses } from "@mui/material/Accordion";
import AccordionSummary, { accordionSummaryClasses } from "@mui/material/AccordionSummary";
import {
  Box,
  Link,
  Stack,
  Avatar,
  Button,
  Dialog,
  Divider,
  DialogProps,
  DialogTitle,
  DialogActions,
  DialogContent,
  LinearProgress,
} from "@mui/material";

import { paths } from "src/routes/paths";
import { useRouter } from "src/routes/hooks/use-router";

import { useBoolean } from "src/hooks/use-boolean";

import { encodeUrl } from "src/utils/url-utils";
import { getTimezone } from "src/utils/get-timezone";
import { trackEvents } from "src/utils/track-events";
import { getGenderAvatar } from "src/utils/get-gender-avatar";
import { fCurrency, fShortenNumber } from "src/utils/format-number";

import { useCreateCart } from "src/api/carts/carts";
import { useCreateWishlist } from "src/api/wishlists/wishlists";
import { useLessonDates } from "src/api/lesson-dates/lesson-dates";
import { useLessonLecturers } from "src/api/lesson-lecturers/lesson-lecturers";
import { useLessonSchedules } from "src/api/lesson-schedules/lesson-schedules";

import Iconify from "src/components/iconify";
import Schedule from "src/components/schedule";
import { useUserContext } from "src/components/user";
import { useToastContext } from "src/components/toast";

import { UserType } from "src/consts/user-type";
import { ITeamMemberProps } from "src/types/team";
import { IScheduleProp, ICourseLessonProp, ICourseByTechnologyProps } from "src/types/course";

// ----------------------------------------------------------------------

interface Props extends DialogProps {
  lesson: ICourseLessonProp;
  onClose: VoidFunction;
}

type LessonItemProps = {
  teacher: ITeamMemberProps;
  lesson: Pick<
    ICourseLessonProp,
    "id" | "title" | "price" | "priceSale" | "lowest30DaysPrice" | "progress"
  >;
  details: ICourseLessonProp;
  expanded: boolean;
  onExpanded: (event: React.SyntheticEvent, isExpanded: boolean) => void;
  loading: boolean;
};

type SlotProps = { time: string; studentsRequired: number };

const DEFAULT_USER = { id: "", avatarUrl: "", name: "Wszyscy" } as const;

// ----------------------------------------------------------------------

function CheckTimeSlots({ lesson, onClose, ...other }: Props) {
  const { data: lessonLecturers, isLoading: isLoadingUsers } = useLessonLecturers({
    lesson_id: lesson?.id,
    page_size: -1,
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
  const [user, setUser] = useState<ITeamMemberProps>(DEFAULT_USER);
  const [date, setDate] = useState<string>(today);
  const [yearMonth, setYearMonth] = useState<string>(currentYearMonth);

  const queryParams = useMemo(
    () => ({
      lecturer_id: user.id,
      lesson_id: lesson?.id,
      duration: lesson?.duration,
      time: date,
      sort_by: "start_time",
      page_size: 48,
    }),
    [date, lesson?.duration, lesson?.id, user.id],
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

  return (
    <Dialog fullWidth maxWidth="sm" onClose={onClose} sx={{ height: "fit-content" }} {...other}>
      <DialogTitle sx={{ typography: "h5", pb: 3 }}>{lesson?.title}</DialogTitle>

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
        />
      </DialogContent>

      <DialogActions>
        <Button variant="outlined" onClick={onClose} color="inherit">
          Zamknij
        </Button>
      </DialogActions>
    </Dialog>
  );
}

export default function TeacherDetailsLessonItem({
  teacher,
  lesson,
  details,
  expanded,
  onExpanded,
  loading,
}: LessonItemProps) {
  const { enqueueSnackbar } = useToastContext();
  const { isLoggedIn, userType } = useUserContext();
  const { push } = useRouter();

  const checkTimeSlotsForm = useBoolean();

  const { mutateAsync: createWishlistItem, isLoading: isAddingToFavorites } = useCreateWishlist();
  const { mutateAsync: createCartItem, isLoading: isAddingToCart } = useCreateCart();

  const genderAvatarUrl = getGenderAvatar(details?.teachers?.[0]?.gender);

  const avatarUrl = details?.teachers?.[0]?.avatarUrl || genderAvatarUrl;

  const path = useMemo(
    () => `${paths.teacher}/${encodeUrl(`${teacher.name}-${teacher.id}`)}/`,
    [teacher.id, teacher.name],
  );

  const handleAddToFavorites = async () => {
    if (!isLoggedIn) {
      push(`${paths.login}?redirect=${path}`);
      return;
    }
    try {
      await createWishlistItem({ lesson: lesson.id });
      enqueueSnackbar("Lekcja została dodana do ulubionych", { variant: "success" });
      trackEvents(
        "add_to_wishlist",
        "teacher_lesson",
        "Teacher lesson added to wishlist",
        lesson.title,
      );
    } catch (error) {
      enqueueSnackbar("Wystąpił błąd podczas dodawania do ulubionych", { variant: "error" });
    }
  };

  const handleAddToCart = async () => {
    if (!isLoggedIn) {
      push(`${paths.login}?redirect=${path}`);
      return;
    }
    try {
      await createCartItem({ lesson: lesson.id });
      enqueueSnackbar("Lekcja została dodana do koszyka", { variant: "success" });
      trackEvents("add_to_cart", "teacher_lesson", "Teacher lesson added to cart", lesson.title);
    } catch (error) {
      enqueueSnackbar("Wystąpił błąd podczas dodawania do koszyka", { variant: "error" });
    }
  };

  return (
    <>
      <Accordion
        expanded={expanded}
        onChange={onExpanded}
        sx={{
          [`&.${accordionClasses.expanded}`]: {
            borderRadius: 0,
          },
        }}
      >
        <AccordionSummary
          sx={{
            px: 1,
            minHeight: 64,
            [`& .${accordionSummaryClasses.content}`]: {
              p: 0,
              m: 0,
              alignItems: "center",
            },
            [`&.${accordionSummaryClasses.expanded}`]: {
              bgcolor: "action.selected",
            },
          }}
        >
          <Typography
            variant="subtitle1"
            sx={{
              flexGrow: 1,
            }}
          >
            {lesson.title}
          </Typography>

          <Stack direction="row" alignItems="center" justifyContent="space-between">
            <Typography variant="h6" sx={{ textAlign: "right" }}>
              {lesson?.priceSale !== undefined && (
                <Box
                  component="span"
                  sx={{
                    mr: 0.5,
                    color: "text.disabled",
                    textDecoration: "line-through",
                  }}
                >
                  {fCurrency(lesson.priceSale)}
                </Box>
              )}
              {lesson?.price !== undefined ? fCurrency(lesson.price) : null}
              {lesson?.priceSale !== undefined &&
                lesson?.priceSale !== null &&
                lesson?.lowest30DaysPrice !== undefined &&
                lesson?.lowest30DaysPrice !== null && (
                  <Typography sx={{ fontSize: 10, color: "text.disabled", textAlign: "center" }}>
                    Najniższa cena z 30 dni przed: {fCurrency(lesson.lowest30DaysPrice)}
                  </Typography>
                )}
            </Typography>
          </Stack>

          <Iconify
            icon={expanded ? "carbon:chevron-down" : "carbon:chevron-right"}
            sx={{ ml: 2 }}
          />
        </AccordionSummary>

        <AccordionDetails
          sx={{
            p: 2,
            typography: "body",
          }}
        >
          {loading ? (
            <LinearProgress />
          ) : (
            <Stack spacing={3}>
              {details.technologies && (
                <Stack
                  spacing={0.5}
                  direction="row"
                  alignItems="center"
                  flexWrap="wrap"
                  divider={
                    <Box
                      sx={{
                        width: 4,
                        height: 4,
                        bgcolor: "text.disabled",
                        borderRadius: "50%",
                      }}
                    />
                  }
                >
                  {details.technologies.map((technology: ICourseByTechnologyProps) => (
                    <Typography
                      key={technology.id}
                      variant="overline"
                      sx={{ color: "primary.main" }}
                    >
                      {technology.name}
                    </Typography>
                  ))}
                </Stack>
              )}

              <Typography sx={{ color: "text.secondary" }}>{details?.description}</Typography>

              <Stack
                spacing={1.5}
                direction="row"
                alignItems="center"
                divider={<Divider orientation="vertical" sx={{ height: 20 }} />}
              >
                {details?.duration && (
                  <Stack spacing={2}>
                    <Stack
                      direction="row"
                      flexWrap="wrap"
                      sx={{
                        "& > *": { my: 0.5 },
                      }}
                    >
                      <Stack direction="row" alignItems="center" sx={{ typography: "body2" }}>
                        <Iconify icon="carbon:time" sx={{ mr: 1 }} /> {details.duration}{" "}
                        {polishPlurals("minuta", "minuty", "minut", details.duration)}
                      </Stack>
                    </Stack>
                  </Stack>
                )}

                {details?.totalReviews && (
                  <Stack spacing={0.5} direction="row" alignItems="center">
                    <Iconify icon="carbon:star-filled" sx={{ color: "warning.main" }} />
                    <Box sx={{ typography: "h6" }}>
                      {Number.isInteger(details.ratingNumber)
                        ? `${details.ratingNumber}.0`
                        : details.ratingNumber}
                    </Box>

                    {details?.totalReviews && (
                      <Typography variant="body2" sx={{ color: "text.secondary" }}>
                        ({fShortenNumber(details.totalReviews)}{" "}
                        {polishPlurals("recenzja", "recenzje", "recenzji", details.totalReviews)})
                      </Typography>
                    )}
                  </Stack>
                )}

                {details?.totalStudents && (
                  <Stack direction="row" sx={{ typography: "subtitle2" }}>
                    {fShortenNumber(details.totalStudents)}
                    <Box component="span" typography="body2" sx={{ ml: 0.5 }}>
                      {polishPlurals("student", "studentów", "studentów", details.totalStudents)}
                    </Box>
                  </Stack>
                )}
              </Stack>

              {details?.teachers && details.teachers.length > 0 && (
                <Stack direction="row" alignItems="center">
                  <Avatar src={avatarUrl} />
                  <Typography variant="body2" sx={{ ml: 1, mr: 0.5 }}>
                    {details.teachers[0]?.name}
                  </Typography>
                  {details.teachers?.length > 1 && (
                    <Link underline="always" color="text.secondary" variant="body2">
                      + {details.teachers.length - 1}{" "}
                      {polishPlurals(
                        "nauczyciel",
                        "nauczycieli",
                        "nauczycieli",
                        details.teachers.length - 1,
                      )}
                    </Link>
                  )}
                </Stack>
              )}

              <Divider sx={{ borderStyle: "dashed" }} />

              <Stack direction="row" spacing={0.5} flexWrap="wrap" justifyContent="right">
                <Button
                  size="medium"
                  color="info"
                  variant="contained"
                  onClick={() => checkTimeSlotsForm.onToggle()}
                >
                  <Iconify icon="carbon:calendar" />
                </Button>
                <LoadingButton
                  size="medium"
                  color="error"
                  variant="contained"
                  onClick={handleAddToFavorites}
                  loading={isAddingToFavorites}
                  disabled={userType !== UserType.Student}
                >
                  <Iconify icon="carbon:favorite" />
                </LoadingButton>
                <LoadingButton
                  size="medium"
                  color="inherit"
                  variant="contained"
                  onClick={handleAddToCart}
                  loading={isAddingToCart}
                  disabled={userType !== UserType.Student}
                >
                  <Iconify icon="carbon:shopping-cart-plus" />
                </LoadingButton>
              </Stack>
            </Stack>
          )}
        </AccordionDetails>
      </Accordion>
      <CheckTimeSlots
        lesson={details}
        open={checkTimeSlotsForm.value}
        onClose={checkTimeSlotsForm.onFalse}
      />
    </>
  );
}
