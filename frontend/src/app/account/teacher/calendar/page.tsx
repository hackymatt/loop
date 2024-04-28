import packageInfo from "package.json";

import AccountCalendarView from "src/sections/view/account/teacher/calendar/account-calendar-view";

// ----------------------------------------------------------------------

export const metadata = {
  title: `${packageInfo.name}: Konto - Terminarz`,
};

export default function AccountCalendarPage() {
  return <AccountCalendarView />;
}
