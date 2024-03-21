import packageInfo from "package.json";

import AccountLessonsView from "src/sections/_elearning/view/account/student/lessons/account-lessons-view";

// ----------------------------------------------------------------------

export const metadata = {
  title: `${packageInfo.name}: Konto - Lekcje`,
};

export default function AccountLessonsPage() {
  return <AccountLessonsView />;
}
