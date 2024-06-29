"use client";

import { ComingSoonLayoutUtil } from "src/utils/coming-soon-utils";

import AuthIllustrationLayout from "src/layouts/auth/illustration";

// ----------------------------------------------------------------------

type Props = {
  children: React.ReactNode;
};

export default function Layout({ children }: Props) {
  return (
    <ComingSoonLayoutUtil
      defaultLayout={<AuthIllustrationLayout>{children}</AuthIllustrationLayout>}
      children={children}
    />
  );
}
