import { ViewUtil } from "src/utils/page-utils";
import { createMetadata } from "src/utils/create-metadata";

import PredispositionTestView from "src/sections/view/predisposition-test-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata(
  "Test predyspozycji",
  "Sprawdź swoje predyspozycje do programowania! Wykonaj darmowy test w loop i dowiedz się, czy kariera programisty jest dla Ciebie. Idealne narzędzie dla osób rozważających naukę programowania.",
  [
    "test predyspozycji",
    "test na programistę",
    "predyspozycje programistyczne",
    "czy nadaję się na programistę",
    "test loop",
    "kariera w IT",
    "test umiejętności programowania",
    "ocena predyspozycji",
    "test dla przyszłych programistów",
    "sprawdź predyspozycje programisty",
  ],
);
export default function PredispositionTestPage() {
  return <ViewUtil defaultView={<PredispositionTestView />} />;
}
