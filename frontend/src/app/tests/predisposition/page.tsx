import { ViewUtil } from "src/utils/page-utils";
import { createMetadata } from "src/utils/create-metadata";

import PredispositionTestView from "src/sections/view/predisposition-test-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Test predyspozycji");
export default function PredispositionTestPage() {
  return <ViewUtil defaultView={<PredispositionTestView />} />;
}
