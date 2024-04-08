import packageInfo from "package.json";

import CartView from "src/sections/_elearning/view/cart-view";

// ----------------------------------------------------------------------

export const metadata = {
  title: `${packageInfo.name}: Koszyk`,
};

export default function CartPage() {
  return <CartView />;
}
