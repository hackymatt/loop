import { createMetadata } from "src/utils/create-metadata";

import AdminCouponUsageView from "src/sections/view/account/admin/coupon-usage/account-coupon-usage-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Konto - Wykorzystanie kuponów");

export default function AccountCouponUsagePage() {
  return <AdminCouponUsageView />;
}
