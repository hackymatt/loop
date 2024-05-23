import { createMetadata } from "src/utils/create-metadata";

import AdminFinanceHistoryView from "src/sections/view/account/admin/finance-history/account-finance-history-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Konto - Historia danych finansowych");

export default function AccountFinanceHistoryPage() {
  return <AdminFinanceHistoryView />;
}
