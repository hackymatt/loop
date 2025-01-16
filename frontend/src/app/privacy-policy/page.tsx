import { paths } from "src/routes/paths";

import { createMetadata } from "src/utils/create-metadata";

import PrivacyPolicyView from "src/sections/view/privacy-policy-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata(
  "Polityka prywatności",
  "Dowiedz się, jak loop chroni Twoje dane osobowe. Przeczytaj naszą politykę prywatności, aby poznać szczegóły dotyczące przetwarzania i zabezpieczania Twoich informacji.",
  [
    "polityka prywatności",
    "ochrona danych osobowych",
    "przetwarzanie danych",
    "loop polityka prywatności",
    "bezpieczeństwo danych",
    "RODO",
    "prywatność użytkowników",
    "gromadzenie danych",
    "udostępnianie danych",
    "zabezpieczenie informacji",
  ],
  paths.privacyPolicy,
);
export default function PrivacyPolicyPage() {
  return <PrivacyPolicyView />;
}
