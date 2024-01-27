import packageInfo from "package.json";

import VerifyView from "src/sections/auth/verify-view";

// ----------------------------------------------------------------------

export const metadata = {
  title: `${packageInfo.name}: Zweryfikuj`,
};

export default function VerifyPage() {
  return <VerifyView />;
}
