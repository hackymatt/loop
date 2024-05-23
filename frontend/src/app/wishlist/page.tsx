import { createMetadata } from "src/utils/create-metadata";

import WishlistView from "src/sections/view/wishlist-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Ulubione");

export default function WishlistPage() {
  return <WishlistView />;
}
