import { polishPlurals } from "polish-plurals";

import Box from "@mui/material/Box";
import Link from "@mui/material/Link";
import Paper from "@mui/material/Paper";
import Stack from "@mui/material/Stack";
import Avatar from "@mui/material/Avatar";
import Typography from "@mui/material/Typography";

import { fShortenNumber } from "src/utils/format-number";

import Iconify from "src/components/iconify";

import { ICourseTeacherProp } from "src/types/course";

// ----------------------------------------------------------------------

type Props = {
  teachers: ICourseTeacherProp[];
};

export default function CourseDetailsTeachersInfo({ teachers = [] }: Props) {
  return (
    <>
      <Typography variant="h4" sx={{ mb: 5 }}>
        Instruktorzy ({teachers.length})
      </Typography>

      <Box
        sx={{
          display: "grid",
          gap: { xs: 3, md: 4 },
          gridTemplateColumns: {
            xs: "repeat(1, 1fr)",
            lg: "repeat(2, 1fr)",
          },
        }}
      >
        {teachers.map((teacher) => (
          <TeacherItem key={teacher.id} teacher={teacher} />
        ))}
      </Box>
    </>
  );
}

// ----------------------------------------------------------------------

type TeacherItemProps = {
  teacher: ICourseTeacherProp;
};

function TeacherItem({ teacher }: TeacherItemProps) {
  const genderAvatarUrl =
    teacher?.gender === "Kobieta"
      ? "/assets/images/avatar/avatar_female.jpg"
      : "/assets/images/avatar/avatar_male.jpg";

  const avatarUrl = teacher?.avatarUrl || genderAvatarUrl;

  return (
    <Paper variant="outlined" sx={{ p: 3, borderRadius: 2 }}>
      <Stack direction="row" spacing={3} flexWrap="wrap">
        <Avatar src={avatarUrl} sx={{ width: 72, height: 72 }} />

        <Stack spacing={1} flexGrow={1}>
          <Stack spacing={0.5}>
            <Typography variant="h6">{teacher.name}</Typography>
            <Typography variant="body2" sx={{ color: "text.secondary" }}>
              {teacher.role}
            </Typography>
          </Stack>

          {teacher.ratingNumber && (
            <Stack spacing={0.5} direction="row" alignItems="center">
              <Iconify icon="carbon:star-filled" sx={{ color: "warning.main" }} />
              <Box sx={{ typography: "h6" }}>
                {Number.isInteger(teacher.ratingNumber)
                  ? `${teacher.ratingNumber}.0`
                  : teacher.ratingNumber}
              </Box>

              {teacher.totalReviews && (
                <Link variant="body2" sx={{ color: "text.secondary" }}>
                  ({fShortenNumber(teacher.totalReviews)}{" "}
                  {polishPlurals("recenzja", "recenzje", "recenzji", teacher.totalReviews)})
                </Link>
              )}
            </Stack>
          )}

          {teacher.totalCourses && (
            <Stack
              direction="row"
              alignItems="center"
              sx={{ typography: "body2", color: "text.disabled" }}
            >
              <Iconify icon="carbon:notebook" sx={{ mr: 1 }} />
              <Box component="strong" sx={{ mr: 0.25 }}>
                {teacher.totalCourses}
              </Box>
              {polishPlurals("lekcja", "lekcje", "lekcji", teacher.totalCourses)}
            </Stack>
          )}
        </Stack>
      </Stack>
    </Paper>
  );
}
