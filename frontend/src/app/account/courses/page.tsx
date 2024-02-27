import packageInfo from "package.json";

import AccountCoursesView from "src/sections/_elearning/view/account-courses-view";

// ----------------------------------------------------------------------

export const metadata = {
  title: `${packageInfo.name}: Konto - Kursy`,
};

export default function AccountCoursesPage() {
  return <AccountCoursesView />;
}
