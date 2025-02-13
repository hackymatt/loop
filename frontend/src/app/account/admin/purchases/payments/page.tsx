import { createMetadata } from "src/utils/create-metadata";

import AccountPaymentView from "src/sections/view/account/admin/payments/account-payments-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Konto - Płatności");

export default function AccountPaymentPage() {
  return <AccountPaymentView />;
}
