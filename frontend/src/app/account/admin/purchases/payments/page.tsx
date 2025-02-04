import { createMetadata } from "src/utils/create-metadata";

import AccountPaymentsView from "src/sections/view/account/admin/purchase-payments/account-payments-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Konto - Płatności");

export default function AccountCategoriesPage() {
  return <AccountPaymentsView />;
}
