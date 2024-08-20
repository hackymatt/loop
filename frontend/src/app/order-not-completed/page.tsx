import { createMetadata } from "src/utils/create-metadata";

import OrderNotCompletedView from "src/sections/view/order-not-completed-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Zakup nieukończony");
export default function OrderNotCompletedPage() {
  return <OrderNotCompletedView />;
}
