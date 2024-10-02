import { ViewUtil } from "src/utils/page-utils";
import { createMetadata } from "src/utils/create-metadata";

import RegisterView from "src/sections/auth/register-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata(
  "Rejestracja",
  "Zarejestruj się w loop i uzyskaj dostęp do kursów programowania online. Stwórz konto, aby rozpocząć naukę z certyfikatem pod okiem profesjonalnych instruktorów.",
  [
    "rejestracja",
    "załóż konto",
    "rejestracja loop",
    "stworzenie konta",
    "nowe konto",
    "rejestracja użytkownika",
    "konto programisty",
    "dostęp do kursów",
    "rejestracja na kursy",
    "loop rejestracja",
  ],
);
export default function RegisterPage() {
  return <ViewUtil defaultView={<RegisterView />} />;
}
