import { createMetadata } from "src/utils/create-metadata";

import ComingSoonView from "src/sections/status/view/coming-soon-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Już wkrótce!");
export default function ComingSoonPage() {
  return <ComingSoonView />;
}
