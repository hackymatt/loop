import { createMetadata } from "src/utils/create-metadata";
import { ComingSoonViewUtil } from "src/utils/coming-soon-utils";

import SupportView from "src/sections/view/support-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Pomoc");
export default function SupportPage() {
  return <ComingSoonViewUtil defaultView={<SupportView />} />;
}
