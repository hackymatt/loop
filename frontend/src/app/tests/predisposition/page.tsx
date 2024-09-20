import { createMetadata } from "src/utils/create-metadata";
import { ViewUtil } from "src/utils/coming-soon-utils";

import PredispositionTestView from "src/sections/view/predisposition-test-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Test predyspozycji");
export default function PredispositionTestPage() {
  return <ViewUtil defaultView={<PredispositionTestView />} />;
}
