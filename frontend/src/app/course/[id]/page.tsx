import { ViewUtil } from "src/utils/page-utils";

import CourseView from "src/sections/view/course-view";

// ----------------------------------------------------------------------

export default function CoursePage({ params }: { params: { id: string } }) {
  return <ViewUtil defaultView={<CourseView id={params.id} />} />;
}
