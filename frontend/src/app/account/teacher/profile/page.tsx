import { createMetadata } from "src/utils/create-metadata";

import AccountProfileView from "src/sections/view/account/teacher/profile/account-profile-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Konto - Profil instruktora");
export default function AccountProfilePage() {
  return <AccountProfileView />;
}
