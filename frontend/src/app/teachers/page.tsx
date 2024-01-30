import packageInfo from "package.json";

import TeachersView from "src/sections/_elearning/view/teachers-view";

// ----------------------------------------------------------------------

export const metadata = {
  title: `${packageInfo.name}: Instruktorzy`,
};

export default function CoursesPage() {
  return <TeachersView />;
}
