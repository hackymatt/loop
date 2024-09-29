import { ViewUtil } from "src/utils/page-utils";
import { createMetadata } from "src/utils/create-metadata";

import ContactView from "src/sections/view/contact-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata(
  "Kontakt",
  "Skontaktuj się z nami, aby dowiedzieć się więcej o naszych kursach programowania, nauczycielach i możliwościach zapisów. loop — Twoja szkoła programowania online.",
  [
    "kontakt",
    "skontaktuj się z nami",
    "informacje kontaktowe",
    "kontakt loop",
    "zapis na kurs",
    "kursy programowania kontakt",
    "konsultacje programistyczne",
    "zapytania o kursy",
    "wsparcie programistyczne",
    "kontakt szkoła programowania",
    "praca szkoła programowania",
    "kariera szkoła programowania",
  ],
);
export default function ContactPage() {
  return <ViewUtil defaultView={<ContactView />} />;
}
