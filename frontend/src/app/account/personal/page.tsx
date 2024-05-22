import { createMetadata } from "src/utils/create-metadata";

import AccountPersonalView from "src/sections/view/account/user/account-personal-view";
// ----------------------------------------------------------------------

export const metadata = createMetadata("Konto - Dane osobowe");

export default function AccountPersonalPage() {
  return <AccountPersonalView />;
}
