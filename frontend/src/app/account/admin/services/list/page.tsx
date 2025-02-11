import { createMetadata } from "src/utils/create-metadata";

import AccountServicesView from "src/sections/view/account/admin/service/account-services-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Konto - Usługi");

export default function AccountServicesPage() {
  return <AccountServicesView />;
}
