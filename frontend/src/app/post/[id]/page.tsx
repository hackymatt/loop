import { ViewUtil } from "src/utils/page-utils";

import { PostView } from "src/sections/view/post-view";

// ----------------------------------------------------------------------

export default function PostPage({ params }: { params: { id: string } }) {
  return <ViewUtil defaultView={<PostView id={params.id} />} />;
}
