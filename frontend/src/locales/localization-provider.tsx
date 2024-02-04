"use client";

import { pl } from "date-fns/locale";

import { AdapterDateFns } from "@mui/x-date-pickers/AdapterDateFns";
import { LocalizationProvider as MuiLocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";

// ----------------------------------------------------------------------

type Props = {
  children: React.ReactNode;
};

export default function LocalizationProvider({ children }: Props) {
  return (
    <MuiLocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={pl}>
      {children}
    </MuiLocalizationProvider>
  );
}
