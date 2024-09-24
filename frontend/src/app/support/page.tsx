import { ViewUtil } from "src/utils/page-utils";
import { createMetadata } from "src/utils/create-metadata";

import SupportView from "src/sections/view/support-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Pomoc");
export default function SupportPage() {
  return <ViewUtil defaultView={<SupportView />} />;
}
