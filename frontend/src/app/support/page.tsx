import packageInfo from "package.json";

import SupportView from "src/sections/_elearning/view/support-view";

// ----------------------------------------------------------------------

export const metadata = {
  title: `${packageInfo.name}: FAQ`,
};

export default function SupportPage() {
  return <SupportView />;
}
