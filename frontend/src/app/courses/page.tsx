import { ViewUtil } from "src/utils/page-utils";
import { createMetadata } from "src/utils/create-metadata";

import CoursesView from "src/sections/view/courses-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata(
  "Kursy programowania online - sprawdź ofertę",
  "Odkryj ofertę kursów programowania w loop. Nauka Python, JavaScript, C++ oraz innych od podstaw z certyfikatem. Zajęcia prowadzone online przez doświadczonych instruktorów.",
  [
    "oferta kursów programowania",
    "kursy Python",
    "kursy JavaScript",
    "kursy C++",
    "programowanie dla początkujących",
    "kursy programistyczne",
    "certyfikat programowania",
    "nauka kodowania",
    "nauka programowania",
    "lekcje programowania online",
    "loop kursy programowania",
  ],
);

export default function CoursesPage() {
  return <ViewUtil defaultView={<CoursesView />} />;
}
