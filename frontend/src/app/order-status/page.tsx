import { createMetadata } from "src/utils/create-metadata";

import OrderStatusView from "src/sections/view/order-status-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Oczekiwanie na płatność");
export default function OrderStatusPage() {
  return <OrderStatusView />;
}
