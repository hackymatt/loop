import { createMetadata } from "src/utils/create-metadata";

import NotFoundView from "src/sections/error/not-found-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("404 Strona nie istnieje!");
export default function NotFoundPage() {
  return <NotFoundView />;
}
