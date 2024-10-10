import { createMetadata } from "src/utils/create-metadata";

import AdminPostsView from "src/sections/view/account/admin/post/account-posts-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Konto - Blog");

export default function AccountPostsPage() {
  return <AdminPostsView />;
}
