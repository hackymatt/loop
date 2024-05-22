import { createMetadata } from "src/utils/create-metadata";

import AccountTeachingView from "src/sections/view/account/teacher/teaching/account-teaching-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Konto - Nauczanie");
export default function AccountTeachingPage() {
  return <AccountTeachingView />;
}
