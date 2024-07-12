import Stack from "@mui/material/Stack";

import { ICourseTeacherProp } from "src/types/course";

import TeacherDetailsLessonList from "./teacher-details-lesson-list";

// ----------------------------------------------------------------------

type Props = {
  teacher: ICourseTeacherProp;
};

export default function TeacherDetailsSummary({ teacher }: Props) {
  return (
    <Stack spacing={5}>
      {teacher.lessons && <TeacherDetailsLessonList lessons={teacher.lessons ?? []} />}
    </Stack>
  );
}
