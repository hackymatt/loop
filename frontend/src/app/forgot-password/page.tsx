import { paths } from "src/routes/paths";

import { createMetadata } from "src/utils/create-metadata";

import ForgotPasswordView from "src/sections/auth/forgot-password-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata(
  "Resetowanie hasła",
  "Zapomniałeś hasła? Zresetuj je szybko i łatwo na stronie loop. Wprowadź swój adres e-mail, aby odzyskać dostęp do swojego konta i kontynuować naukę programowania.",
  [
    "resetowanie hasła",
    "odzyskiwanie hasła",
    "zapomniałem hasła",
    "zmiana hasła",
    "przywrócenie dostępu",
    "reset hasła online",
    "nowe hasło",
    "odzyskanie konta",
    "loop reset hasła",
    "problemy z hasłem",
  ],
  paths.forgotPassword,
);
export default function ForgotPasswordPage() {
  return <ForgotPasswordView />;
}
