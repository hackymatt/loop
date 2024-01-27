import packageInfo from "package.json";

import LoginView from "src/sections/auth/login-view";

// ----------------------------------------------------------------------

export const metadata = {
  title: `${packageInfo.name}: Logowanie`,
};

export default function LoginPage() {
  return <LoginView />;
}
