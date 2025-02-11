import { createMetadata } from "src/utils/create-metadata";

import AccountServicePaymentView from "src/sections/view/account/admin/purchase-payments/account-services-payments-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Konto - Płatności");

export default function AccountServicePaymentPage() {
  return <AccountServicePaymentView />;
}
