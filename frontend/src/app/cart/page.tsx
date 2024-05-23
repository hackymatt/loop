import { createMetadata } from "src/utils/create-metadata";

import CartView from "src/sections/view/cart-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Koszyk");
export default function CartPage() {
  return <CartView />;
}
