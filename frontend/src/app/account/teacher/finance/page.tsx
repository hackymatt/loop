import packageInfo from "package.json";

import AccountFinanceView from "src/sections/view/account/teacher/finance/account-finance-view";

// ----------------------------------------------------------------------

export const metadata = {
  title: `${packageInfo.name}: Konto - Dane finansowe`,
};

export default function AccountFinancePage() {
  return <AccountFinanceView />;
}
