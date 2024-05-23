import { createMetadata } from "src/utils/create-metadata";

import AccountReviewsView from "src/sections/view/account/teacher/reviews/account-reviews-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Konto - Recenzje");
export default function AccountReviewsPage() {
  return <AccountReviewsView />;
}
