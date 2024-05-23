import { createMetadata } from "src/utils/create-metadata";

import AccountLessonsView from "src/sections/view/account/student/lessons/account-lessons-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Konto - Lekcje");

export default function AccountLessonsPage() {
  return <AccountLessonsView />;
}
