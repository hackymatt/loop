import packageInfo from "package.json";

import AccountScheduleView from "src/sections/_elearning/view/account/teacher/schedule/account-schedule-view";

// ----------------------------------------------------------------------

export const metadata = {
  title: `${packageInfo.name}: Konto - Terminarz`,
};

export default function AccountSchedulePage() {
  return <AccountScheduleView />;
}
