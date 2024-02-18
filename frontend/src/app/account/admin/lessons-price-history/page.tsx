import packageInfo from "package.json";

import AdminLessonsPriceHistoryView from "src/sections/_elearning/view/admin/account-lessons-price-history-view";

// ----------------------------------------------------------------------

export const metadata = {
  title: `${packageInfo.name}: Konto - Lekcje`,
};

export default function AccountLessonsPriceHistoryPage() {
  return <AdminLessonsPriceHistoryView />;
}
