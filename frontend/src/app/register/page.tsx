import { ViewUtil } from "src/utils/page-utils";
import { createMetadata } from "src/utils/create-metadata";

import RegisterView from "src/sections/auth/register-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Rejestracja");
export default function RegisterPage() {
  return <ViewUtil defaultView={<RegisterView />} />;
}
