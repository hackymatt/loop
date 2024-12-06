import { ICourseModuleProp } from "src/types/course";

import CourseDetailsModuleItem from "./course-details-module-item";

// ----------------------------------------------------------------------

type Props = {
  modules: ICourseModuleProp[];
};

export default function CourseDetailsModuleList({ modules }: Props) {
  return (
    <div>
      {modules.map((module, index) => (
        <CourseDetailsModuleItem key={module.id} index={index + 1} module={module} />
      ))}
    </div>
  );
}
