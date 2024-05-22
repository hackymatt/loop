import { createMetadata } from "src/utils/create-metadata";

import AccountTechnologiesView from "src/sections/view/account/admin/technologies/account-technologies-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Konto - Technologie");

export default function AccountTechnologiesPage() {
  return <AccountTechnologiesView />;
}
