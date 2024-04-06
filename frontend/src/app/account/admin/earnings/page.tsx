import packageInfo from "package.json";

import AccountEarningsView from "src/sections/_elearning/view/account/admin/earnings/account-earnings-view";

// ----------------------------------------------------------------------

export const metadata = {
  title: `${packageInfo.name}: Konto - Zarobki`,
};

export default function AccountEarningsPage() {
  return <AccountEarningsView />;
}
