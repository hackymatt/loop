import packageInfo from "package.json";

import AccountCoursesView from "src/sections/_elearning/view/account/admin/course/account-courses-view";

// ----------------------------------------------------------------------

export const metadata = {
  title: `${packageInfo.name}: Konto - Lekcje`,
};

export default function AccountLessonsPage() {
  return <AccountCoursesView />;
}
