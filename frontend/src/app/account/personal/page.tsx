import packageInfo from "package.json";

import AccountPersonalView from "src/sections/_elearning/view/account-personal-view";
// ----------------------------------------------------------------------

export const metadata = {
  title: `${packageInfo.name}: Konto - Dane osobowe`,
};

export default function AccountPersonalPage() {
  return <AccountPersonalView />;
}
