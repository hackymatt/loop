import packageInfo from "package.json";

import EcommerceCartView from "src/sections/_ecommerce/view/ecommerce-cart-view";

// ----------------------------------------------------------------------

export const metadata = {
  title: `${packageInfo.name}: Koszyk`,
};

export default function EcommerceCartPage() {
  return <EcommerceCartView />;
}
