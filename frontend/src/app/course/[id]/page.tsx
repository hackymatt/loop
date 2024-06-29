import { createMetadata } from "src/utils/create-metadata";
import { ComingSoonViewUtil } from "src/utils/coming-soon-utils";

import CourseView from "src/sections/view/course-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Kurs");
export default function CoursePage({ params }: { params: { id: string } }) {
  return <ComingSoonViewUtil defaultView={<CourseView id={params.id} />} />;
}
