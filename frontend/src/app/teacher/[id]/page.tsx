import { createMetadata } from "src/utils/create-metadata";
import { ComingSoonViewUtil } from "src/utils/coming-soon-utils";

import TeacherView from "src/sections/view/teacher-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Instruktor");
export default function TeacherPage({ params }: { params: { id: string } }) {
  return <ComingSoonViewUtil defaultView={<TeacherView id={params.id} />} />;
}
