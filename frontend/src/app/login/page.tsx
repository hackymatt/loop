import { createMetadata } from "src/utils/create-metadata";

import LoginView from "src/sections/auth/login-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Logowanie");
export default function LoginPage() {
  return <LoginView />;
}
