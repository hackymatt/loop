import packageInfo from "package.json";

import AdminFinanceHistoryView from "src/sections/view/account/admin/finance-history/account-finance-history-view";

// ----------------------------------------------------------------------

export const metadata = {
  title: `${packageInfo.name}: Konto - Historia danych finansowych`,
};

export default function AccountFinanceHistoryPage() {
  return <AdminFinanceHistoryView />;
}
