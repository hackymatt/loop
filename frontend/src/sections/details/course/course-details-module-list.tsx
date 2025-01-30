import { ICourseProps, ICourseModuleProp } from "src/types/course";

import CourseDetailsModuleItem from "./course-details-module-item";

// ----------------------------------------------------------------------

type Props = {
  course: ICourseProps;
  modules: ICourseModuleProp[];
};

export default function CourseDetailsModuleList({ course, modules }: Props) {
  return (
    <div>
      {modules.map((module, index) => (
        <CourseDetailsModuleItem
          key={module.id}
          index={index + 1}
          course={course}
          module={module}
        />
      ))}
    </div>
  );
}
