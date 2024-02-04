import { Box } from "@mui/material";
import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";
import { SelectChangeEvent } from "@mui/material/Select";

import { IQueryParamValue } from "src/types/query-params";
import { ICourseLessonProp, ICourseTeacherProp } from "src/types/course";

import Sorting from "./review-sorting";
import FilterLesson from "./review-filter-lesson";
import FilterTeacher from "./review-filter-teacher";

// ----------------------------------------------------------------------

const SORT_OPTIONS = [
  { value: "-created_at", label: "Najnowsze" },
  { value: "created_at", label: "Najstarsze" },
];

// ----------------------------------------------------------------------
type Props = {
  lesson: IQueryParamValue;
  lessonOptions: ICourseLessonProp[];
  teacher: string;
  teacherOptions: ICourseTeacherProp[];
  sort: string;
  onChangeLesson: (newValue: IQueryParamValue) => void;
  onChangeTeacher: (newValue: IQueryParamValue) => void;
  onChangeSort: (event: SelectChangeEvent) => void;
};

export default function ReviewToolbar({
  lesson,
  lessonOptions,
  teacher,
  teacherOptions,
  sort,
  onChangeLesson,
  onChangeTeacher,
  onChangeSort,
}: Props) {
  return (
    <Stack spacing={1} alignItems="left" direction="column" sx={{ mb: 3 }}>
      <Typography variant="h4" sx={{ width: 1 }}>
        Recenzje
      </Typography>

      <Box
        rowGap={2.5}
        columnGap={2}
        display="grid"
        gridTemplateColumns={{ xs: "repeat(1, 1fr)", md: "repeat(3, 1fr)" }}
      >
        <FilterLesson value={lesson} options={lessonOptions} onChange={onChangeLesson} />
        <FilterTeacher value={teacher} options={teacherOptions} onChange={onChangeTeacher} />
        <Sorting value={sort} options={SORT_OPTIONS} onChange={onChangeSort} />
      </Box>
    </Stack>
  );
}
