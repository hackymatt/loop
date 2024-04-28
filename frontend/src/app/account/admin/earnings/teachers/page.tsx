import packageInfo from "package.json";

import AccountEarningsTeachersView from "src/sections/view/account/admin/earnings-teachers/account-earnings-teachers-view";

// ----------------------------------------------------------------------

export const metadata = {
  title: `${packageInfo.name}: Konto - Zarobki wykładowców`,
};

export default function AccountEarningsTeachersPage() {
  return <AccountEarningsTeachersView />;
}
