"use client";

import { SnackbarProvider } from "notistack";

// ----------------------------------------------------------------------

type Props = {
  children: React.ReactNode;
};

export function ToastProvider({ children }: Props) {
  return (
    <SnackbarProvider maxSnack={3} autoHideDuration={3000}>
      {children}
    </SnackbarProvider>
  );
}
