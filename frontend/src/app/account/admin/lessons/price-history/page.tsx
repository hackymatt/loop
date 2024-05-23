import { createMetadata } from "src/utils/create-metadata";

import AdminLessonsPriceHistoryView from "src/sections/view/account/admin/lesson-price-history/account-lessons-price-history-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Konto - Historia cen lekcji");
export default function AccountLessonsPriceHistoryPage() {
  return <AdminLessonsPriceHistoryView />;
}
