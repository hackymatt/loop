import packageInfo from "package.json";

import HomeView from "src/sections/_elearning/view/home-view";

// ----------------------------------------------------------------------

export const metadata = {
  title: `${packageInfo.name}: Strona głowna`,
};

export default function LandingPage() {
  return <HomeView />;
}
