import { createMetadata } from "src/utils/create-metadata";
import { ViewUtil } from "src/utils/coming-soon-utils";

import LoginView from "src/sections/auth/login-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Logowanie");
export default function LoginPage() {
  return <ViewUtil defaultView={<LoginView />} />;
}
