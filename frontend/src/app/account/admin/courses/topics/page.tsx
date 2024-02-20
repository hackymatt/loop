import packageInfo from "package.json";

import AdminCoursesTopicsView from "src/sections/_elearning/view/account/admin/account-courses-topics-view";

// ----------------------------------------------------------------------

export const metadata = {
  title: `${packageInfo.name}: Konto - Tematy`,
};

export default function AccountCoursesTopicsPage() {
  return <AdminCoursesTopicsView />;
}
