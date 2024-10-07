import { ViewUtil } from "src/utils/page-utils";
import { createMetadata } from "src/utils/create-metadata";

import { PostsView } from "src/sections/view/posts-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata(
  "Blog",
  "Blog to źródło wiedzy dla każdego, kto pragnie zgłębić świat programowania. Publikujemy artykuły, porady i tutoriale dotyczące najnowszych technologii, najlepszych praktyk w programowaniu oraz rozwoju umiejętności w IT. Dołącz do naszej społeczności i ucz się z nami!",
  [
    "nauka programowania",
    "blog programistyczny",
    "porady dla programistów",
    "kursy online programowanie",
    "szkoła programowania online",
    "jak nauczyć się programować",
    "kodowanie dla początkujących",
    "najlepsze technologie IT",
    "rozwój umiejętności programistycznych",
    "tutoriale programistyczne",
  ],
);

export default function PostsPage() {
  return <ViewUtil defaultView={<PostsView />} />;
}
