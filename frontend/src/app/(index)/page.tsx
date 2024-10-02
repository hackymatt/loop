import { ViewUtil } from "src/utils/page-utils";
import { createMetadata } from "src/utils/create-metadata";

import HomeView from "src/sections/view/home-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata(
  "Zostań lepszym programistą już dziś!",
  "Naucz się programować w loop. Kursy Python, JavaScript, C++ i więcej. Zdobądź certyfikat i rozwijaj swoją karierę IT z najlepszymi instruktorami.",
  [
    "programowanie dla początkujących",
    "kursy programowania online",
    "nauka programowania",
    "szkoła programowania online",
    "certyfikat programowania",
    "kursy Python",
    "kursy JavaScript",
    "kursy TypeScript",
    "kursy C++",
    "kursy Git",
    "kursy programistyczne",
    "loop szkoła programowania",
  ],
);

export default function HomePage() {
  return <ViewUtil defaultView={<HomeView />} />;
}
