"use client";

import { useUser } from "src/hooks/use-user";

import AuthBackgroundLayout from "src/layouts/auth/background";

// ----------------------------------------------------------------------

type Props = {
  children: React.ReactNode;
};

export default function Layout({ children }: Props) {
  const { email } = useUser();
  return email ? <AuthBackgroundLayout>{children}</AuthBackgroundLayout> : <>{children}</>;
}
