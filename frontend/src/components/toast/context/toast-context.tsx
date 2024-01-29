"use client";

import { useSnackbar } from "notistack";

// ----------------------------------------------------------------------

export const useToastContext = () => {
  const snackbar = useSnackbar();

  return snackbar;
};
