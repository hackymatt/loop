import { createMetadata } from "src/utils/create-metadata";
import { ComingSoonViewUtil } from "src/utils/coming-soon-utils";

import TeachersView from "src/sections/view/teachers-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Instruktorzy");
export default function CoursesPage() {
  return <ComingSoonViewUtil defaultView={<TeachersView />} />;
}
