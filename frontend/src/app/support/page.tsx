import { createMetadata } from "src/utils/create-metadata";

import SupportView from "src/sections/view/support-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("FAQ");
export default function SupportPage() {
  return <SupportView />;
}
