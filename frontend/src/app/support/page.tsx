import { ViewUtil } from "src/utils/page-utils";
import { createMetadata } from "src/utils/create-metadata";

import SupportView from "src/sections/view/support-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata(
  "Pomoc",
  "Potrzebujesz wsparcia? Skontaktuj się z działem pomocy LOOP. Znajdź odpowiedzi na najczęściej zadawane pytania dotyczące kursów programowania, logowania i rejestracji.",
  [
    "pomoc",
    "wsparcie techniczne",
    "kontakt z pomocą",
    "loop pomoc",
    "najczęściej zadawane pytania",
    "FAQ",
    "problemy techniczne",
    "wsparcie użytkowników",
    "pomoc w rejestracji",
    "pomoc w logowaniu",
  ],
);
export default function SupportPage() {
  return <ViewUtil defaultView={<SupportView />} />;
}
