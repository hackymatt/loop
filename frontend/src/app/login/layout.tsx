"use client";

import { LayoutUtil } from "src/utils/coming-soon-utils";

import AuthIllustrationLayout from "src/layouts/auth/illustration";

// ----------------------------------------------------------------------

type Props = {
  children: React.ReactNode;
};

export default function Layout({ children }: Props) {
  return (
    <LayoutUtil
      defaultLayout={<AuthIllustrationLayout>{children}</AuthIllustrationLayout>}
      children={children}
    />
  );
}
