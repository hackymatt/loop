import { createMetadata } from "src/utils/create-metadata";

import AccountEarningsCompanyView from "src/sections/view/account/admin/earnings-company/account-earnings-company-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Konto - Zarobki firmy");
export default function AccountEarningsCompanyPage() {
  return <AccountEarningsCompanyView />;
}
