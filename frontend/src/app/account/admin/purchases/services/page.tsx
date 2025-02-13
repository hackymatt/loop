import { createMetadata } from "src/utils/create-metadata";

import AccountServicesPurchaseView from "src/sections/view/account/admin/purchase/account-services-purchase-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Konto - Zakupy usług");

export default function AccountPurchasePage() {
  return <AccountServicesPurchaseView />;
}
