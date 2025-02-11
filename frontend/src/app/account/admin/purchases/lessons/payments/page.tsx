import { createMetadata } from "src/utils/create-metadata";

import AccountPaymentsView from "src/sections/view/account/admin/purchase-payments/account-lessons-payments-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Konto - Płatności lekcji");

export default function AccountLessonsPaymentsPage() {
  return <AccountPaymentsView />;
}
