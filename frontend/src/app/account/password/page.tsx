import packageInfo from "package.json";

import AccountPasswordView from "src/sections/_elearning/view/account/account-password-view";

// ----------------------------------------------------------------------

export const metadata = {
  title: `${packageInfo.name}: Konto - Zarządzaj hasłem`,
};

export default function AccountPasswordPage() {
  return <AccountPasswordView />;
}
