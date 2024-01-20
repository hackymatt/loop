import packageInfo from "package.json";

import ElearningContactView from "src/sections/_elearning/view/elearning-contact-view";

// ----------------------------------------------------------------------

export const metadata = {
  title: `${packageInfo.name}: Kontakt`,
};

export default function ElearningContactPage() {
  return <ElearningContactView />;
}
