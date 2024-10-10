import { createMetadata } from "src/utils/create-metadata";

import AccountPostCategoriesView from "src/sections/view/account/admin/post-categories/account-post-categories-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Konto - Kategorie");

export default function AccountCategoriesPage() {
  return <AccountPostCategoriesView />;
}
