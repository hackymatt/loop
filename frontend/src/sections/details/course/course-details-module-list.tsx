import { useState, useCallback } from "react";

import Typography from "@mui/material/Typography";

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
      <Typography variant="h4" sx={{ mb: 3 }}>
        Program szkolenia
      </Typography>

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
