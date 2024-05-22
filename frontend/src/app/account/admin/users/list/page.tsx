import { createMetadata } from "src/utils/create-metadata";

import AccountUsersView from "src/sections/view/account/admin/users/account-users-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Konto - Spis użytkowników");

export default function AccountUsersPage() {
  return <AccountUsersView />;
}
