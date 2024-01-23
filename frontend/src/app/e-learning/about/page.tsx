import packageInfo from "package.json";

import AboutView from "src/sections/_elearning/view/about-view";

// ----------------------------------------------------------------------

export const metadata = {
  title: `${packageInfo.name}: O nas`,
};

export default function AboutPage() {
  return <AboutView />;
}
