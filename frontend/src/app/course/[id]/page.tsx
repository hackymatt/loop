import packageInfo from "package.json";

import CourseView from "src/sections/view/course-view";

// ----------------------------------------------------------------------

export const metadata = {
  title: `${packageInfo.name}: Kurs`,
};

export default function CoursePage({ params }: { params: { id: string } }) {
  return <CourseView id={params.id} />;
}
