import { createMetadata } from "src/utils/create-metadata";
import { ComingSoonViewUtil } from "src/utils/coming-soon-utils";

import RegisterView from "src/sections/auth/register-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Rejestracja");
export default function RegisterPage() {
  return <ComingSoonViewUtil defaultView={<RegisterView />} />;
}
