import { createMetadata } from "src/utils/create-metadata";

import AccountLessonsPurchaseView from "src/sections/view/account/admin/purchase/account-lessons-purchase-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Konto - Zakupy lekcji");

export default function AccountLessonsPurchasePage() {
  return <AccountLessonsPurchaseView />;
}
