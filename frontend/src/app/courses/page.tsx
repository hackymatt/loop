import { createMetadata } from "src/utils/create-metadata";
import { ViewUtil } from "src/utils/page-utils";

import CoursesView from "src/sections/view/courses-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Kursy");

export default function CoursesPage() {
  return <ViewUtil defaultView={<CoursesView />} />;
}
