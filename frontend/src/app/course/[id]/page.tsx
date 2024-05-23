import { createMetadata } from "src/utils/create-metadata";

import CourseView from "src/sections/view/course-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Kurs");
export default function CoursePage({ params }: { params: { id: string } }) {
  return <CourseView id={params.id} />;
}
