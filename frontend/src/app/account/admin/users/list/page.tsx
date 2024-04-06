import packageInfo from "package.json";

import AccountUsersView from "src/sections/_elearning/view/account/admin/users/account-users-view";

// ----------------------------------------------------------------------

export const metadata = {
  title: `${packageInfo.name}: Konto - Spis użytkowników`,
};

export default function AccountUsersPage() {
  return <AccountUsersView />;
}
