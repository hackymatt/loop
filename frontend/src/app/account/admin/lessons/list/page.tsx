import { createMetadata } from "src/utils/create-metadata";

import AdminLessonsView from "src/sections/view/account/admin/lesson/account-lessons-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Konto - Lekcje");

export default function AccountLessonsPage() {
  return <AdminLessonsView />;
}
