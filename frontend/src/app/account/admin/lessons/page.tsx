import packageInfo from "package.json";

import AdminLessonsView from "src/sections/_elearning/view/admin/account-lessons-view";

// ----------------------------------------------------------------------

export const metadata = {
  title: `${packageInfo.name}: Konto - Lekcje`,
};

export default function AccountLessonsPage() {
  return <AdminLessonsView />;
}
