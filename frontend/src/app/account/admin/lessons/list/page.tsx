import packageInfo from "package.json";

import AdminLessonsView from "src/sections/view/account/admin/lesson/account-lessons-view";

// ----------------------------------------------------------------------

export const metadata = {
  title: `${packageInfo.name}: Konto - Lekcje`,
};

export default function AccountLessonsPage() {
  return <AdminLessonsView />;
}
