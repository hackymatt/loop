import packageInfo from "package.json";

import AccountEarningsView from "src/sections/view/account/teacher/earnings/account-earnings-view";

// ----------------------------------------------------------------------

export const metadata = {
  title: `${packageInfo.name}: Konto - Zarobki`,
};

export default function AccountEarningsPage() {
  return <AccountEarningsView />;
}
