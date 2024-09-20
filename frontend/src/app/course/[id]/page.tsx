import { createMetadata } from "src/utils/create-metadata";
import { ViewUtil } from "src/utils/coming-soon-utils";

import CourseView from "src/sections/view/course-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Kurs");
export default function CoursePage({ params }: { params: { id: string } }) {
  return <ViewUtil defaultView={<CourseView id={params.id} />} />;
}
