import packageInfo from "package.json";

import AccountFinanceView from "src/sections/_elearning/view/account/teacher/account-finance-view";

// ----------------------------------------------------------------------

export const metadata = {
  title: `${packageInfo.name}: Konto - Dane finansowe`,
};

export default function AccountFinancePage() {
  return <AccountFinanceView />;
}
