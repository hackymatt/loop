import { createMetadata } from "src/utils/create-metadata";

import AccountCertificatesView from "src/sections/view/account/student/reviews/account-reviews-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Konto - Certyfikaty");

export default function AccountCertificatesPage() {
  return <AccountCertificatesView />;
}
