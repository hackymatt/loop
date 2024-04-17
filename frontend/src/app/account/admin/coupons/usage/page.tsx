import packageInfo from "package.json";

import AdminCouponUsageView from "src/sections/_elearning/view/account/admin/coupon-usage/account-coupon-usage-view";

// ----------------------------------------------------------------------

export const metadata = {
  title: `${packageInfo.name}: Konto - Wykorzystanie kuponów`,
};

export default function AccountCouponUsagePage() {
  return <AdminCouponUsageView />;
}
