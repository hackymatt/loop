import { createMetadata } from "src/utils/create-metadata";

import AccountManageView from "src/sections/view/account/user/account-manage-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Konto - Zarządzaj kontem");

export default function AccountManagePage() {
  return <AccountManageView />;
}
