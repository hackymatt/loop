import { createMetadata } from "src/utils/create-metadata";

import AccountCouponsView from "src/sections/view/account/admin/coupons/account-coupons-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Konto - Spis kuponów");

export default function AccountCouponsPage() {
  return <AccountCouponsView />;
}
