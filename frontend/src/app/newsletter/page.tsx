import { paths } from "src/routes/paths";

import { createMetadata } from "src/utils/create-metadata";

import NewsletterSubscribeView from "src/sections/view/newsletter-subscribe-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata(
  "Zapisz się do newslettera loop",
  "Zapisz się do newslettera loop i bądź na bieżąco z najnowszymi kursami programowania, wydarzeniami i promocjami! Otrzymuj ekskluzywne informacje o nadchodzących kursach na żywo, zniżkach oraz materiałach edukacyjnych bezpośrednio na swoją skrzynkę. Nasz newsletter to doskonała okazja, aby rozwijać swoje umiejętności programistyczne i być na czołowej pozycji w branży IT. Dołącz do społeczności LOOP i nie przegap żadnej okazji do nauki!",
  [
    "newsletter loop",
    "kursy programowania",
    "kursy na żywo",
    "szkoła programowania",
    "nauka programowania",
    "promocje kursy programowania",
    "zapisz się do newslettera",
    "szkoła programowania online",
    "kursy z instruktorem",
    "programowanie z Google Meet",
    "nowe kursy programowania",
    "rozwój umiejętności IT",
    "zniżki na kursy programowania",
  ],
  paths.newsletter.subscribe,
);

export default function NewsletterSubscribePage({ params }: { params: { id: string } }) {
  return <NewsletterSubscribeView />;
}
