import packageInfo from "package.json";

import AccountReviewsView from "src/sections/view/account/teacher/reviews/account-reviews-view";

// ----------------------------------------------------------------------

export const metadata = {
  title: `${packageInfo.name}: Konto - Recenzje`,
};

export default function AccountReviewsPage() {
  return <AccountReviewsView />;
}
