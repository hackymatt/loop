import packageInfo from "package.json";

import ForgotPasswordView from "src/sections/auth/forgot-password-view";

// ----------------------------------------------------------------------

export const metadata = {
  title: `${packageInfo.name}: Resetowanie hasła`,
};

export default function ForgotPasswordPage() {
  return <ForgotPasswordView />;
}
