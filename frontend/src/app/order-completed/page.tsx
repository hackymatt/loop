import { createMetadata } from "src/utils/create-metadata";

import OrderCompletedView from "src/sections/view/order-completed-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Zakup ukończony");
export default function OrderCompletedPage() {
  return <OrderCompletedView />;
}
