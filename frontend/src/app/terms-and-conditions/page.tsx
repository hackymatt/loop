import packageInfo from "package.json";

import TermsAndConditionsView from "src/sections/_elearning/view/terms-and-conditions-view";

// ----------------------------------------------------------------------

export const metadata = {
  title: `${packageInfo.name}: Regulamin`,
};
export default function TermsAndConditionsPage() {
  return <TermsAndConditionsView />;
}
