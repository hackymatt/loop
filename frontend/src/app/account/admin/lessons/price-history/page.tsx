import packageInfo from "package.json";

import AdminLessonsPriceHistoryView from "src/sections/_elearning/view/account/admin/account-lessons-price-history-view";

// ----------------------------------------------------------------------

export const metadata = {
  title: `${packageInfo.name}: Konto - Historia cen lekcji`,
};

export default function AccountLessonsPriceHistoryPage() {
  return <AdminLessonsPriceHistoryView />;
}
