import { createMetadata } from "src/utils/create-metadata";

import HomeView from "src/sections/view/home-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata(
  "Zostań lepszym programistą już dziś!",
  "Naucz się programować w loop – oferujemy kursy Python, JavaScript, C++, oraz wiele innych. Rozwijaj swoją karierę IT z najlepszymi instruktorami, korzystając z nowoczesnych metod nauki i materiałów dostępnych 24/7.",
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
  return <HomeView />;
}
