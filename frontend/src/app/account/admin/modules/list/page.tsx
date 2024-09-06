import { createMetadata } from "src/utils/create-metadata";

import AdminModulesView from "src/sections/view/account/admin/module/account-modules-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Konto - Moduły");

export default function AccountModulesPage() {
  return <AdminModulesView />;
}
