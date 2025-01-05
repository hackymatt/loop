import { paths } from "src/routes/paths";

import { createMetadata } from "src/utils/create-metadata";

import AboutView from "src/sections/view/about-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata(
  "O nas",
  "Poznaj loop — szkołę programowania online. Nasi doświadczeni instruktorzy prowadzą kursy Python, JavaScript, C++ i innych technologii. Zdobądź certyfikat już dziś!",
  [
    "o nas",
    "szkoła programowania",
    "instruktorzy programowania",
    "nauczyciele programowania",
    "kursy online",
    "nauka programowania",
    "loop szkoła programowania",
    "opinie o kursach",
    "certyfikaty programowania",
    "mentorzy programowania",
  ],
  paths.about,
);

export default function AboutPage() {
  return <AboutView />;
}
