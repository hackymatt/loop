import { createMetadata } from "src/utils/create-metadata";
import { ViewUtil } from "src/utils/page-utils";

import AboutView from "src/sections/view/about-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("O nas");

export default function AboutPage() {
  return <ViewUtil defaultView={<AboutView />} />;
}
