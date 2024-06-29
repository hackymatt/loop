"use client";

import { ComingSoonLayoutUtil } from "src/utils/coming-soon-utils";

import MainLayout from "src/layouts/main";

// ----------------------------------------------------------------------

type Props = {
  children: React.ReactNode;
};

export default function Layout({ children }: Props) {
  return (
    <ComingSoonLayoutUtil
      defaultLayout={<MainLayout disabledSpacing>{children}</MainLayout>}
      children={children}
    />
  );
}
