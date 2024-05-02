"use client";

import AuthIllustrationLayout from "src/layouts/auth/illustration";

import { useUserContext } from "src/components/user";

// ----------------------------------------------------------------------

type Props = {
  children: React.ReactNode;
};

export default function Layout({ children }: Props) {
  const { email } = useUserContext();
  return email ? <AuthIllustrationLayout>{children}</AuthIllustrationLayout> : <>{children}</>;
}
