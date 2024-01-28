"use client";

import MainLayout from "src/layouts/main";
import AccountLayout from "src/layouts/account";

// ----------------------------------------------------------------------

type Props = {
  children: React.ReactNode;
};

export default function Template({ children }: Props) {
  return (
    <MainLayout>
      <AccountLayout>{children}</AccountLayout>
    </MainLayout>
  );
}
