import { useMemo } from "react";
import { polishPlurals } from "polish-plurals";

import Box from "@mui/material/Box";
import Link from "@mui/material/Link";
import Paper from "@mui/material/Paper";
import Stack from "@mui/material/Stack";
import Avatar from "@mui/material/Avatar";
import Typography from "@mui/material/Typography";

import { paths } from "src/routes/paths";
import { RouterLink } from "src/routes/components";

import { encodeUrl } from "src/utils/url-utils";
import { fShortenNumber } from "src/utils/format-number";
import { getGenderAvatar } from "src/utils/get-gender-avatar";

import Iconify from "src/components/iconify";

import { ICourseTeacherDetailsProps } from "src/types/course";

// ----------------------------------------------------------------------

type Props = {
  teachers: ICourseTeacherDetailsProps[];
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
  teacher: ICourseTeacherDetailsProps;
};

function TeacherItem({ teacher }: TeacherItemProps) {
  const { id, name, gender, role, image, totalLessons, ratingNumber, totalReviews } = teacher;

  const genderAvatarUrl = getGenderAvatar(gender);

  const avatarUrl = image || genderAvatarUrl;

  const path = useMemo(() => `${name}-${id}`, [id, name]);

  return (
    <Link
      component={RouterLink}
      href={`${paths.teacher}/${encodeUrl(path)}/`}
      color="inherit"
      underline="none"
    >
      <Paper variant="outlined" sx={{ p: 3, borderRadius: 2 }}>
        <Stack direction="row" spacing={3} flexWrap="nowrap">
          <Avatar src={avatarUrl} sx={{ width: 72, height: 72 }} />

          <Stack spacing={1} flexGrow={1}>
            <Stack spacing={0.5}>
              <Typography variant="h6">{name}</Typography>

              <Typography variant="body2" sx={{ color: "text.secondary" }}>
                {role}
              </Typography>
            </Stack>

            {totalLessons > 0 ? (
              <Stack
                direction="row"
                alignItems="center"
                sx={{ typography: "body2", color: "text.disabled" }}
              >
                <Iconify icon="carbon:notebook" sx={{ mr: 1 }} />
                <Box component="strong" sx={{ mr: 0.25 }}>
                  {teacher.totalLessons}
                </Box>
                {polishPlurals("lekcja", "lekcje", "lekcji", totalLessons)}
              </Stack>
            ) : null}

            {ratingNumber !== null ? (
              <Stack spacing={0.5} direction="row" alignItems="center">
                <Iconify icon="carbon:star-filled" sx={{ color: "warning.main" }} />
                <Box sx={{ typography: "h6" }}>
                  {Number.isInteger(ratingNumber) ? `${ratingNumber}.0` : ratingNumber}
                </Box>

                <Typography variant="body2" sx={{ color: "text.secondary" }}>
                  ({fShortenNumber(totalReviews)}{" "}
                  {polishPlurals("recenzja", "recenzje", "recenzji", totalReviews)})
                </Typography>
              </Stack>
            ) : null}
          </Stack>
        </Stack>
      </Paper>
    </Link>
  );
}
