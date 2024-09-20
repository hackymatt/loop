import { createMetadata } from "src/utils/create-metadata";
import { ViewUtil } from "src/utils/page-utils";

import ContactView from "src/sections/view/contact-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Kontakt");
export default function ContactPage() {
  return <ViewUtil defaultView={<ContactView />} />;
}
