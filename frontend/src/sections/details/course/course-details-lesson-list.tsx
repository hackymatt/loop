import { useState, useCallback } from "react";

import { useLesson } from "src/api/lessons/lesson";

import { ICourseProps, ICourseLessonProp } from "src/types/course";

import CourseDetailsLessonItem from "./course-details-lesson-item";

// ----------------------------------------------------------------------

type Props = {
  course: ICourseProps;
  lessons: ICourseLessonProp[];
};

export default function CourseDetailsLessonList({ course, lessons }: Props) {
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
      {lessons.map((lesson, index) => (
        <CourseDetailsLessonItem
          key={lesson.id}
          index={index + 1}
          course={course}
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
