import { format } from "date-fns";
import { useMemo, useState } from "react";
import { polishPlurals } from "polish-plurals";
import { formatInTimeZone } from "date-fns-tz";

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

import { useBoolean } from "src/hooks/use-boolean";

import { getTimezone } from "src/utils/get-timezone";
import { fCurrency, fShortenNumber } from "src/utils/format-number";

import { useLessonLecturers } from "src/api/lesson-lecturers/lesson-lecturers";
import { useLessonSchedules } from "src/api/lesson-schedules/lesson-schedules";

import Iconify from "src/components/iconify";
import Schedule from "src/components/schedule";

import { ITeamMemberProps } from "src/types/team";
import { IScheduleProp, ICourseLessonProp } from "src/types/course";

import Repository from "../repository/repository";

// ----------------------------------------------------------------------

interface Props extends DialogProps {
  lesson: ICourseLessonProp;
  onClose: VoidFunction;
}

type LessonItemProps = {
  lesson: Pick<ICourseLessonProp, "id" | "title" | "price" | "priceSale" | "lowest30DaysPrice">;
  details: ICourseLessonProp;
  expanded: boolean;
  onExpanded: (event: React.SyntheticEvent, isExpanded: boolean) => void;
  loading: boolean;
};

const DEFAULT_USER = { id: "", avatarUrl: "", name: "Wszyscy" } as const;

// ----------------------------------------------------------------------

function CheckTimeSlots({ lesson, onClose, ...other }: Props) {
  const { data: lessonLecturers, isLoading: isLoadingUsers } = useLessonLecturers({
    lesson_id: lesson?.id,
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

  const today = useMemo(() => format(new Date(), "yyyy-MM-dd"), []);
  const [user, setUser] = useState<ITeamMemberProps>(DEFAULT_USER);
  const [date, setDate] = useState<string>(today);

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

  const { data: lessonSchedules, isLoading: isLoadingTimeSlots } = useLessonSchedules(
    date === today ? { ...queryParams, reserved: "True" } : queryParams,
  );

  const slots = useMemo(() => {
    const allSlots = lessonSchedules?.map((lessonSchedule: IScheduleProp) => {
      const dt = new Date(lessonSchedule.startTime);
      return {
        time: formatInTimeZone(dt, getTimezone(), "HH:mm"),
        studentsCount: lessonSchedule.studentsCount,
      };
    });

    return Array.from(new Set(allSlots)).sort();
  }, [lessonSchedules]);

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
          currentSlot={slots?.[0]?.time}
          isLoadingUsers={isLoadingUsers}
          isLoadingTimeSlots={isLoadingTimeSlots}
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

export default function CourseDetailsLessonItem({
  lesson,
  details,
  expanded,
  onExpanded,
  loading,
}: LessonItemProps) {
  const checkTimeSlotsForm = useBoolean();

  const genderAvatarUrl =
    details?.teachers?.[0]?.gender === "Kobieta"
      ? "/assets/images/avatar/avatar_female.jpg"
      : "/assets/images/avatar/avatar_male.jpg";

  const avatarUrl = details?.teachers?.[0]?.avatarUrl || genderAvatarUrl;
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
              {lesson?.priceSale && (
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
              {lesson?.price ? fCurrency(lesson.price) : null}
              {lesson?.priceSale && lesson?.lowest30DaysPrice && (
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
              {details.category && (
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
                  {details.category.map((category: string) => (
                    <Typography key={category} variant="overline" sx={{ color: "primary.main" }}>
                      {category}
                    </Typography>
                  ))}
                </Stack>
              )}

              <Typography sx={{ color: "text.secondary", textAlign: "justify" }}>
                {details?.description}
              </Typography>

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
                      <Link variant="body2" sx={{ color: "text.secondary" }}>
                        ({fShortenNumber(details.totalReviews)}{" "}
                        {polishPlurals("recenzja", "recenzje", "recenzji", details.totalReviews)})
                      </Link>
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

              {details?.githubUrl && (
                <Stack direction="row" flexWrap="wrap">
                  <Repository githubUrl={details.githubUrl} />
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
                <Button size="medium" color="error" variant="contained">
                  <Iconify icon="carbon:favorite" />
                </Button>
                <Button size="medium" color="inherit" variant="contained">
                  <Iconify icon="carbon:shopping-cart-plus" />
                </Button>
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
