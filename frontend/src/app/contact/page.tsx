import packageInfo from "package.json";

import ContactView from "src/sections/view/contact-view";

// ----------------------------------------------------------------------

export const metadata = {
  title: `${packageInfo.name}: Kontakt`,
};

export default function ContactPage() {
  return <ContactView />;
}
