import packageInfo from "package.json";

import LandingView from "src/sections/_elearning/view/landing-view";

// ----------------------------------------------------------------------

export const metadata = {
  title: `${packageInfo.name}: Strona głowna`,
};

export default function ElearningLandingPage() {
  return <LandingView />;
}
