import Box from "@mui/material/Box";
import Chip from "@mui/material/Chip";
import Stack from "@mui/material/Stack";
import { alpha } from "@mui/material/styles";
import Typography from "@mui/material/Typography";

import Iconify from "src/components/iconify";
import { CircularProgressWithLabel } from "src/components/progress-label/circle-progress";

import { ICourseProps } from "src/types/course";

import CourseDetailsModuleList from "./course-details-module-list";

// ----------------------------------------------------------------------

type Props = {
  course: ICourseProps;
};

export default function CourseDetailsSummary({ course }: Props) {
  return (
    <Stack spacing={5}>
      <Stack direction="row" spacing={1} alignItems="center">
        <CircularProgressWithLabel value={course.progress ?? 0} size={40} />
        <Typography variant="h4">Program szkolenia</Typography>
      </Stack>

      {course.modules && <CourseDetailsModuleList modules={course.modules ?? []} />}

      <Stack spacing={3}>
        <Typography variant="h4">Czego się nauczysz</Typography>

        <Stack spacing={1}>
          {course.learnList?.map((learn) => (
            <Stack key={learn} direction="row" alignItems="center">
              <Box
                sx={{
                  mr: 1.5,
                  width: 20,
                  height: 20,
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
        <Typography variant="h4">Umiejętności, które zdobędziesz</Typography>

        <Stack direction="row" flexWrap="wrap" spacing={1}>
          {course.skills?.map((skill) => (
            <Chip key={skill} label={skill} size="small" variant="soft" onClick={() => {}} />
          ))}
        </Stack>
      </Stack>
    </Stack>
  );
}
