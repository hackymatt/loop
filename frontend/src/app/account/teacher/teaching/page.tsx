import packageInfo from "package.json";

import AccountTeachingView from "src/sections/_elearning/view/account/teacher/teaching/account-teaching-view";

// ----------------------------------------------------------------------

export const metadata = {
  title: `${packageInfo.name}: Konto - Nauczanie`,
};

export default function AccountTeachingPage() {
  return <AccountTeachingView />;
}
