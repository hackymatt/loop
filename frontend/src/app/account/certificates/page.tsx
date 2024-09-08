import { createMetadata } from "src/utils/create-metadata";

import AccountCertificatesView from "src/sections/view/account/student/certificates/account-certificates-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Konto - Certyfikaty");

export default function AccountCertificatesPage() {
  return <AccountCertificatesView />;
}
