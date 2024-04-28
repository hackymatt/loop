import packageInfo from "package.json";

import OrderCompletedView from "src/sections/view/order-completed-view";

// ----------------------------------------------------------------------

export const metadata = {
  title: `${packageInfo.name}: Zakup ukończony`,
};

export default function OrderCompletedPage() {
  return <OrderCompletedView />;
}
