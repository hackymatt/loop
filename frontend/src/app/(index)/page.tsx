import { createMetadata } from "src/utils/create-metadata";

import HomeView from "src/sections/view/home-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Zostań lepszym programistą już dziś!");

export default function HomePage() {
  return <HomeView />;
}
