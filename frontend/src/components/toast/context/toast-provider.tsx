"use client";

import { SnackbarProvider } from "notistack";

// ----------------------------------------------------------------------

type Props = {
  children: React.ReactNode;
};

export function ToastProvider({ children }: Props) {
  return <SnackbarProvider maxSnack={3}>{children}</SnackbarProvider>;
}
