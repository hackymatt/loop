import packageInfo from "package.json";

import AccountCouponsView from "src/sections/view/account/admin/coupons/account-coupons-view";

// ----------------------------------------------------------------------

export const metadata = {
  title: `${packageInfo.name}: Konto - Spis kuponów`,
};

export default function AccountCouponsPage() {
  return <AccountCouponsView />;
}
