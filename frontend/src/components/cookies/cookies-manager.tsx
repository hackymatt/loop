"use client";

import { useCallback } from "react";

import { useBoolean } from "src/hooks/use-boolean";
import { useCookies } from "src/hooks/use-cookies";
import { useLocalStorage } from "src/hooks/use-local-storage";

import CookiesBanner from "./cookies-banner";

// ----------------------------------------------------------------------

export default function CookiesManager() {
  const { defaultCookies } = useCookies();
  const { state, update } = useLocalStorage("cookies", { ...defaultCookies, consent: false });

  const cookieFormOpen = useBoolean();

  const handleConfirm = useCallback(
    (selectedCookies: { [cookie: string]: boolean }) => {
      update("consent", true);
      Object.keys(selectedCookies).forEach((cookie) => update(cookie, selectedCookies[cookie]));
      cookieFormOpen.onFalse();
    },
    [cookieFormOpen, update],
  );

  if (!state.consent) {
    return <CookiesBanner open onConfirm={handleConfirm} />;
  }
}
