import { createMetadata } from "src/utils/create-metadata";

import AccountNewsletterView from "src/sections/view/account/admin/newsletter/account-newsletter-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Konto - Newsletter");

export default function AccountNewsletterPage() {
  return <AccountNewsletterView />;
}
