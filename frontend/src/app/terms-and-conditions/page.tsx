import { createMetadata } from "src/utils/create-metadata";
import { ViewUtil } from "src/utils/coming-soon-utils";

import TermsAndConditionsView from "src/sections/view/terms-and-conditions-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Regulamin");
export default function TermsAndConditionsPage() {
  return <ViewUtil defaultView={<TermsAndConditionsView />} />;
}
