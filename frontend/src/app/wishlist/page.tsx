import packageInfo from "package.json";

import WishlistView from "src/sections/view/wishlist-view";

// ----------------------------------------------------------------------

export const metadata = {
  title: `${packageInfo.name}: Ulubione`,
};

export default function WishlistPage() {
  return <WishlistView />;
}
