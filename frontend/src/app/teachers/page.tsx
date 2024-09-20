import { createMetadata } from "src/utils/create-metadata";
import { ViewUtil } from "src/utils/page-utils";

import TeachersView from "src/sections/view/teachers-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Instruktorzy");
export default function CoursesPage() {
  return <ViewUtil defaultView={<TeachersView />} />;
}
