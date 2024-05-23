import { createMetadata } from "src/utils/create-metadata";

import AccountCoursesView from "src/sections/view/account/admin/course/account-courses-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Konto - Kursy");
export default function AccountLessonsPage() {
  return <AccountCoursesView />;
}
