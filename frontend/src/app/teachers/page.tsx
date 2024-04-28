import packageInfo from "package.json";

import TeachersView from "src/sections/view/teachers-view";

// ----------------------------------------------------------------------

export const metadata = {
  title: `${packageInfo.name}: Instruktorzy`,
};

export default function CoursesPage() {
  return <TeachersView />;
}
