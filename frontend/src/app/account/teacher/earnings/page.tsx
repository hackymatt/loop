import packageInfo from "package.json";

import AccountReviewsView from "src/sections/_elearning/view/account/student/account-reviews-view";

// ----------------------------------------------------------------------

export const metadata = {
  title: `${packageInfo.name}: Konto - Recenzje`,
};

export default function AccountReviewsPage() {
  return <AccountReviewsView />;
}
