import packageInfo from "package.json";

import AccountTechnologiesView from "src/sections/view/account/admin/technologies/account-technologies-view";

// ----------------------------------------------------------------------

export const metadata = {
  title: `${packageInfo.name}: Konto - Technologie`,
};

export default function AccountTechnologiesPage() {
  return <AccountTechnologiesView />;
}
