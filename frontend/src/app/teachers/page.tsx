import { createMetadata } from "src/utils/create-metadata";

import TeachersView from "src/sections/view/teachers-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Instruktorzy");
export default function CoursesPage() {
  return <TeachersView />;
}
