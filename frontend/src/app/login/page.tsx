import { createMetadata } from "src/utils/create-metadata";
import { ComingSoonViewUtil } from "src/utils/coming-soon-utils";

import LoginView from "src/sections/auth/login-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Logowanie");
export default function LoginPage() {
  return <ComingSoonViewUtil defaultView={<LoginView />} />;
}
