import Box from "@mui/material/Box";
import { Link } from "@mui/material";
import Chip from "@mui/material/Chip";
import Stack from "@mui/material/Stack";
import { alpha } from "@mui/material/styles";
import Typography from "@mui/material/Typography";

import { paths } from "src/routes/paths";
import { RouterLink } from "src/routes/components";

import Iconify, { isIconExists } from "src/components/iconify";
import { CircularProgressWithLabel } from "src/components/progress-label/circle-progress";

import { ICourseProps, ICourseByTechnologyProps } from "src/types/course";

import CourseDetailsModuleList from "./course-details-module-list";

// ----------------------------------------------------------------------

type Props = {
  course: ICourseProps;
};

export default function CourseDetailsSummary({ course }: Props) {
  return (
    <Stack spacing={5}>
      <Stack direction="row" spacing={1} alignItems="center">
        {course.progress !== undefined ? (
          <CircularProgressWithLabel value={course.progress ?? 0} size={40} />
        ) : null}
        <Typography variant="h4">Program szkolenia</Typography>
      </Stack>

      {course.modules && <CourseDetailsModuleList modules={course.modules ?? []} />}

      <Box>
        <Typography component="h6" variant="h4" sx={{ mb: 2 }}>
          Dlaczego ten kurs?
        </Typography>
        <Typography sx={{ textAlign: "justify" }}>
          {course?.overview?.split("\n").map((line, index) => (
            <Typography key={index}>
              {line}
              <br />
            </Typography>
          )) ?? ""}
        </Typography>
      </Box>

      <Stack spacing={3}>
        <Typography variant="h4">Dla kogo ten kurs?</Typography>

        <Stack spacing={1}>
          {course.candidateList?.map((candidate) => (
            <Stack key={candidate} direction="row" alignItems="center" spacing={1.5}>
              <Box
                sx={{
                  width: 20,
                  height: 20,
                  flexShrink: 0,
                  display: "flex",
                  borderRadius: "50%",
                  alignItems: "center",
                  justifyContent: "center",
                  bgcolor: (theme) => alpha(theme?.palette?.primary?.main, 0.08),
                }}
              >
                <Iconify
                  icon="carbon:checkmark"
                  sx={{ width: 16, height: 16, color: "primary.main" }}
                />
              </Box>
              {candidate}
            </Stack>
          ))}
        </Stack>
      </Stack>

      <Stack spacing={3}>
        <Typography variant="h4">Czego się nauczysz?</Typography>

        <Stack spacing={1}>
          {course.learnList?.map((learn) => (
            <Stack key={learn} direction="row" alignItems="center" spacing={1.5}>
              <Box
                sx={{
                  width: 20,
                  height: 20,
                  flexShrink: 0,
                  display: "flex",
                  borderRadius: "50%",
                  alignItems: "center",
                  justifyContent: "center",
                  bgcolor: (theme) => alpha(theme?.palette?.primary?.main, 0.08),
                }}
              >
                <Iconify
                  icon="carbon:checkmark"
                  sx={{ width: 16, height: 16, color: "primary.main" }}
                />
              </Box>
              {learn}
            </Stack>
          ))}
        </Stack>
      </Stack>

      <Stack spacing={3}>
        <Typography variant="h4">O technologiach w tym kursie</Typography>

        <Stack spacing={2}>
          {course.technologies?.map((technology: ICourseByTechnologyProps) => {
            const defaultIcon = `bxl:${technology.name.toLowerCase()}`;
            const icon = isIconExists(defaultIcon) ? defaultIcon : "carbon:code";
            return (
              <Stack key={technology.id} spacing={0}>
                <Stack direction="row" alignItems="center" spacing={1.5}>
                  <Box
                    sx={{
                      width: 20,
                      height: 20,
                      flexShrink: 0,
                      display: "flex",
                      borderRadius: "50%",
                      alignItems: "center",
                      justifyContent: "center",
                      bgcolor: (theme) => alpha(theme?.palette?.primary?.main, 0.08),
                    }}
                  >
                    <Iconify icon={icon} sx={{ width: 16, height: 16, color: "primary.main" }} />
                  </Box>
                  {technology.name}
                </Stack>
                <Typography
                  variant="body2"
                  color="text.secondary"
                  ml={4}
                  sx={{ textAlign: "justify" }}
                >
                  {technology.description?.split("\n").map((line, index) => (
                    <Typography key={index}>
                      {line}
                      <br />
                    </Typography>
                  )) ?? ""}
                </Typography>
              </Stack>
            );
          })}
        </Stack>
      </Stack>

      <Box display="flex" alignItems="center" flexWrap="wrap">
        <Typography variant="subtitle2" sx={{ mr: 1 }}>
          Tagi
        </Typography>

        <Box gap={1} display="flex" flexWrap="wrap">
          {course.tags?.map((tag) => (
            <Link component={RouterLink} key={tag} href={`${paths.courses}?tags_in=${tag}`}>
              <Chip key={tag} size="small" variant="soft" label={tag} />
            </Link>
          ))}
        </Box>
      </Box>
    </Stack>
  );
}
