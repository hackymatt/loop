import packageInfo from "package.json";

import RegisterView from "src/sections/auth/register-view";

// ----------------------------------------------------------------------

export const metadata = {
  title: `${packageInfo.name}: Rejestracja`,
};

export default function RegisterPage() {
  return <RegisterView />;
}
