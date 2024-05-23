import { createMetadata } from "src/utils/create-metadata";

import AboutView from "src/sections/view/about-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("O nas");

export default function AboutPage() {
  return <AboutView />;
}
