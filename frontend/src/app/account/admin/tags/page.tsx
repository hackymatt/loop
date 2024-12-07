import { createMetadata } from "src/utils/create-metadata";

import AccountTagsView from "src/sections/view/account/admin/tags/account-tags-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Konto - Tagi");

export default function AccountTagsPage() {
  return <AccountTagsView />;
}
