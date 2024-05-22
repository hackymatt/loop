import { createMetadata } from "src/utils/create-metadata";

import AccountFinanceView from "src/sections/view/account/teacher/finance/account-finance-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Konto - Dane finansowe");
export default function AccountFinancePage() {
  return <AccountFinanceView />;
}
