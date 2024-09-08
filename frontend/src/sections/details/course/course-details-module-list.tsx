import { useState, useCallback } from "react";

import { ICourseModuleProp } from "src/types/course";

import CourseDetailsModuleItem from "./course-details-module-item";

// ----------------------------------------------------------------------

type Props = {
  modules: ICourseModuleProp[];
};

export default function CourseDetailsModuleList({ modules }: Props) {
  const [expanded, setExpanded] = useState<string | false>(false);

  const handleExpandedModule = useCallback(
    (panel: string) => (event: React.SyntheticEvent, isExpanded: boolean) => {
      setExpanded(isExpanded ? panel : false);
    },
    [],
  );

  return (
    <div>
      {modules.map((module, index) => (
        <CourseDetailsModuleItem
          key={module.id}
          index={index + 1}
          module={module}
          expanded={expanded === module.id}
          onExpanded={handleExpandedModule(module.id)}
        />
      ))}
    </div>
  );
}
