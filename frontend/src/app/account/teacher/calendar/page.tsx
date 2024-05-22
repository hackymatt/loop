import { createMetadata } from "src/utils/create-metadata";

import AccountCalendarView from "src/sections/view/account/teacher/calendar/account-calendar-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Konto - Terminarz");

export default function AccountCalendarPage() {
  return <AccountCalendarView />;
}
