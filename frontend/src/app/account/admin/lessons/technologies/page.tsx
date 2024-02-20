import packageInfo from "package.json";

import AccountTechnologiesView from "src/sections/_elearning/view/account/admin/account-technologies-view";

// ----------------------------------------------------------------------

export const metadata = {
  title: `${packageInfo.name}: Konto - Technologie`,
};

export default function AccountTechnologiesPage() {
  return <AccountTechnologiesView />;
}
