import packageInfo from "package.json";

import AccountCoursesView from "src/sections/view/account/admin/course/account-courses-view";

// ----------------------------------------------------------------------

export const metadata = {
  title: `${packageInfo.name}: Konto - Kursy`,
};

export default function AccountLessonsPage() {
  return <AccountCoursesView />;
}
