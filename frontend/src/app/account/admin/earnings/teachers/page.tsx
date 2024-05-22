import { createMetadata } from "src/utils/create-metadata";

import AccountEarningsTeachersView from "src/sections/view/account/admin/earnings-teachers/account-earnings-teachers-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Konto - Zarobki wykładowców");
export default function AccountEarningsTeachersPage() {
  return <AccountEarningsTeachersView />;
}
