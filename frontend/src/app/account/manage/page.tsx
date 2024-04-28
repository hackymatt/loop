import packageInfo from "package.json";

import AccountManageView from "src/sections/view/account/user/account-manage-view";

// ----------------------------------------------------------------------

export const metadata = {
  title: `${packageInfo.name}: Konto - Zarządzaj kontem`,
};

export default function AccountManagePage() {
  return <AccountManageView />;
}
