import packageInfo from "package.json";

import PrivacyPolicyView from "src/sections/view/privacy-policy-view";

// ----------------------------------------------------------------------

export const metadata = {
  title: `${packageInfo.name}: Polityka prywatności`,
};

export default function PrivacyPolicyPage() {
  return <PrivacyPolicyView />;
}
