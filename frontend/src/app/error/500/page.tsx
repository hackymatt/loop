import { createMetadata } from "src/utils/create-metadata";

import View500 from "src/sections/error/500-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("500 Błąd serwera");
export default function Page500() {
  return <View500 />;
}
