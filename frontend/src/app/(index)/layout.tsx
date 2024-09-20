"use client";

import { LayoutUtil } from "src/utils/page-utils";

import MainLayout from "src/layouts/main";

// ----------------------------------------------------------------------

type Props = {
  children: React.ReactNode;
};

export default function Layout({ children }: Props) {
  return (
    <LayoutUtil
      defaultLayout={<MainLayout disabledSpacing>{children}</MainLayout>}
      children={children}
    />
  );
}
