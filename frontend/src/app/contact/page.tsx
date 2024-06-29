import { createMetadata } from "src/utils/create-metadata";
import { ComingSoonViewUtil } from "src/utils/coming-soon-utils";

import ContactView from "src/sections/view/contact-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Kontakt");
export default function ContactPage() {
  return <ComingSoonViewUtil defaultView={<ContactView />} />;
}
