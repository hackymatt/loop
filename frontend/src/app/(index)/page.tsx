import { createMetadata } from "src/utils/create-metadata";
import { ViewUtil } from "src/utils/coming-soon-utils";

import HomeView from "src/sections/view/home-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Zostań lepszym programistą już dziś!");

export default function HomePage() {
  return <ViewUtil defaultView={<HomeView />} />;
}
