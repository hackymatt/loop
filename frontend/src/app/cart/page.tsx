import packageInfo from "package.json";

import CartView from "src/sections/view/cart-view";

// ----------------------------------------------------------------------

export const metadata = {
  title: `${packageInfo.name}: Koszyk`,
};

export default function CartPage() {
  return <CartView />;
}
