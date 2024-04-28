import packageInfo from "package.json";

import AdminCoursesTopicsView from "src/sections/view/account/admin/topics/account-courses-topics-view";

// ----------------------------------------------------------------------

export const metadata = {
  title: `${packageInfo.name}: Konto - Tematy`,
};

export default function AccountCoursesTopicsPage() {
  return <AdminCoursesTopicsView />;
}
