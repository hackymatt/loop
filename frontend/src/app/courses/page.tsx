import packageInfo from "package.json";

import CoursesView from "src/sections/_elearning/view/courses-view";

// ----------------------------------------------------------------------

export const metadata = {
  title: `${packageInfo.name}: Kursy`,
};

export default function CoursesPage() {
  return <CoursesView />;
}
