import { createMetadata } from "src/utils/create-metadata";

import AdminPurchaseView from "src/sections/view/account/admin/purchase/account-purchase-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Konto - Zakupy");

export default function AccountPurchasePage() {
  return <AdminPurchaseView />;
}
