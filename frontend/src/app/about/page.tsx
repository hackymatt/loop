import { createMetadata } from "src/utils/create-metadata";
import { ComingSoonViewUtil } from "src/utils/coming-soon-utils";

import AboutView from "src/sections/view/about-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("O nas");

export default function AboutPage() {
  return <ComingSoonViewUtil defaultView={<AboutView />} />;
}
