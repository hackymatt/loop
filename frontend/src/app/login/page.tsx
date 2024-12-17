import { createMetadata } from "src/utils/create-metadata";

import LoginView from "src/sections/auth/login-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata(
  "Logowanie",
  "Zaloguj się na swoje konto w loop, aby uzyskać dostęp do kursów programowania online. Wprowadź swoje dane logowania i kontynuuj naukę programowania z certyfikatem.",
  [
    "logowanie",
    "logowanie do konta",
    "logowanie loop",
    "dostęp do konta",
    "kursy programowania logowanie",
    "zaloguj się",
    "konto programisty",
    "panel użytkownika",
    "loop logowanie",
    "dane logowania",
  ],
);
export default function LoginPage() {
  return <LoginView />;
}
