import { createMetadata } from "src/utils/create-metadata";
import { ViewUtil } from "src/utils/page-utils";

import PrivacyPolicyView from "src/sections/view/privacy-policy-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Polityka prywatności");
export default function PrivacyPolicyPage() {
  return <ViewUtil defaultView={<PrivacyPolicyView />} />;
}
