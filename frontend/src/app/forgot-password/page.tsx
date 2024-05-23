import { createMetadata } from "src/utils/create-metadata";

import ForgotPasswordView from "src/sections/auth/forgot-password-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Resetowanie hasła");
export default function ForgotPasswordPage() {
  return <ForgotPasswordView />;
}
