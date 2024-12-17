import { createMetadata } from "src/utils/create-metadata";

import TermsAndConditionsView from "src/sections/view/terms-and-conditions-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata(
  "Regulamin",
  "Zapoznaj się z regulaminem korzystania z platformy loop. Sprawdź zasady dotyczące uczestnictwa w kursach, płatności, rejestracji i ochrony danych osobowych.",
  [
    "regulamin",
    "zasady korzystania",
    "regulamin loop",
    "warunki uczestnictwa",
    "płatności za kursy",
    "zasady rejestracji",
    "regulamin platformy",
    "warunki użytkowania",
    "ochrona danych",
    "loop regulamin",
  ],
);
export default function TermsAndConditionsPage() {
  return <TermsAndConditionsView />;
}
