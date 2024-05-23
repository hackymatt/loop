import { createMetadata } from "src/utils/create-metadata";

import VerifyView from "src/sections/auth/verify-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Zweryfikuj");

export default function VerifyPage() {
  return <VerifyView />;
}
