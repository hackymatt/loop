import { createMetadata } from "src/utils/create-metadata";

import AccountCoursesCandidatesView from "src/sections/view/account/admin/candidates/account-courses-candidates-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Konto - Kandydaci");

export default function AccountCoursesCandidatesPage() {
  return <AccountCoursesCandidatesView />;
}
