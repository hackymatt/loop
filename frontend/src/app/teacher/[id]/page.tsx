import { ViewUtil } from "src/utils/page-utils";
import { createMetadata } from "src/utils/create-metadata";

import TeacherView from "src/sections/view/teacher-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Instruktor");
export default function TeacherPage({ params }: { params: { id: string } }) {
  return <ViewUtil defaultView={<TeacherView id={params.id} />} />;
}
