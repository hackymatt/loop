import { createMetadata } from "src/utils/create-metadata";
import { ComingSoonViewUtil } from "src/utils/coming-soon-utils";

import CoursesView from "src/sections/view/courses-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Kursy");

export default function CoursesPage() {
  return <ComingSoonViewUtil defaultView={<CoursesView />} />;
}
