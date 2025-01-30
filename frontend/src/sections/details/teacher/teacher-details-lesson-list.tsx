import { useState, useCallback } from "react";

import Typography from "@mui/material/Typography";

import { useLesson } from "src/api/lessons/lesson";

import { ITeamMemberProps } from "src/types/team";
import { ICourseLessonProp } from "src/types/course";

import TeacherDetailsLessonItem from "./teacher-details-lesson-item";

// ----------------------------------------------------------------------

type Props = {
  teacher: ITeamMemberProps;
  lessons: ICourseLessonProp[];
};

export default function TeacherDetailsLessonList({ teacher, lessons }: Props) {
  const [lessonId, setLessonId] = useState<string>(lessons[0].id);
  const [expanded, setExpanded] = useState<string | false>(false);

  const { data: details, isLoading } = useLesson(lessonId);

  const handleExpandedLesson = useCallback(
    (panel: string) => (event: React.SyntheticEvent, isExpanded: boolean) => {
      setLessonId(panel);
      setExpanded(isExpanded ? panel : false);
    },
    [],
  );

  return (
    <div>
      <Typography variant="h4" sx={{ mb: 3 }}>
        Lekcje
      </Typography>

      {lessons.map((lesson) => (
        <TeacherDetailsLessonItem
          key={lesson.id}
          teacher={teacher}
          lesson={lesson}
          details={details}
          expanded={expanded === lesson.id}
          onExpanded={handleExpandedLesson(lesson.id)}
          loading={isLoading}
        />
      ))}
    </div>
  );
}
