import packageInfo from "package.json";

import AccountNewsletterView from "src/sections/_elearning/view/account/admin/newsletter/account-newsletter-view";

// ----------------------------------------------------------------------

export const metadata = {
  title: `${packageInfo.name}: Konto - Newsletter`,
};

export default function AccountNewsletterPage() {
  return <AccountNewsletterView />;
}
