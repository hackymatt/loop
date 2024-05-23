import { createMetadata } from "src/utils/create-metadata";

import AccountEarningsView from "src/sections/view/account/teacher/earnings/account-earnings-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Konto - Zarobki");
export default function AccountEarningsPage() {
  return <AccountEarningsView />;
}
