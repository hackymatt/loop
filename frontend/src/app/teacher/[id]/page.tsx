import { ViewUtil } from "src/utils/page-utils";

import TeacherView from "src/sections/view/teacher-view";

// ----------------------------------------------------------------------

export default function TeacherPage({ params }: { params: { id: string } }) {
  return <ViewUtil defaultView={<TeacherView id={params.id} />} />;
}
