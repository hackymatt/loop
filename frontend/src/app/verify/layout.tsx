"use client";

import AuthBackgroundLayout from "src/layouts/auth/background";

import { useUserContext } from "src/components/user";

// ----------------------------------------------------------------------

type Props = {
  children: React.ReactNode;
};

export default function Layout({ children }: Props) {
  const { email } = useUserContext();
  return email ? <AuthBackgroundLayout>{children}</AuthBackgroundLayout> : <>{children}</>;
}
