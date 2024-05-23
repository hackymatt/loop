import { createMetadata } from "src/utils/create-metadata";

import MaintenanceView from "src/sections/status/view/maintenance-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Trwają prace serwisowe");
export default function MaintenancePage() {
  return <MaintenanceView />;
}
