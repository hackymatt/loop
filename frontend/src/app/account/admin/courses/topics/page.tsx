import { createMetadata } from "src/utils/create-metadata";

import AdminCoursesTopicsView from "src/sections/view/account/admin/topics/account-courses-topics-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Konto - Tematy");

export default function AccountCoursesTopicsPage() {
  return <AdminCoursesTopicsView />;
}
