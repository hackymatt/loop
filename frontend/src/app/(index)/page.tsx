import { differenceInMinutes } from "date-fns";

import { createMetadata } from "src/utils/create-metadata";

import { ENV } from "src/config-global";

import HomeView from "src/sections/view/home-view";
import ComingSoonView from "src/sections/status/view/coming-soon-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Zostań lepszym programistą już dziś!");

export default function HomePage() {
  const startDate = new Date("10/01/2024 00:00");
  const diff = differenceInMinutes(startDate, new Date());
  const showComingSoon = ENV === "PROD" && diff > 0;
  return showComingSoon ? <ComingSoonView startDate={startDate} /> : <HomeView />;
}
