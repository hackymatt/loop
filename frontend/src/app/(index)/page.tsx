import packageInfo from "package.json";

import HomeView from "src/sections/view/home-view";

// ----------------------------------------------------------------------

export const metadata = {
  title: `${packageInfo.name}: Szkoła programowania`,
};

export default function HomePage() {
  return <HomeView />;
}
