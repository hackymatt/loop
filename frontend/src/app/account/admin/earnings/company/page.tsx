import packageInfo from "package.json";

import AccountEarningsCompanyView from "src/sections/view/account/admin/earnings-company/account-earnings-company-view";

// ----------------------------------------------------------------------

export const metadata = {
  title: `${packageInfo.name}: Konto - Zarobki firmy`,
};

export default function AccountEarningsCompanyPage() {
  return <AccountEarningsCompanyView />;
}
