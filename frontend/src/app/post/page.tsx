import { ViewUtil } from "src/utils/page-utils";

import { PostView } from "src/sections/view/post-view";

// ----------------------------------------------------------------------

export default function PostPage() {
  return <ViewUtil defaultView={<PostView />} />;
}
