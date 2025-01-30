import Stack from "@mui/material/Stack";

import { ITeamMemberProps } from "src/types/team";

import TeacherDetailsLessonList from "./teacher-details-lesson-list";

// ----------------------------------------------------------------------

type Props = {
  teacher: ITeamMemberProps;
};

export default function TeacherDetailsSummary({ teacher }: Props) {
  return (
    <Stack spacing={5}>
      {teacher.lessons && (
        <TeacherDetailsLessonList teacher={teacher} lessons={teacher.lessons ?? []} />
      )}
    </Stack>
  );
}
