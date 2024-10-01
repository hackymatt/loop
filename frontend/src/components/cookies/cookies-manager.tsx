"use client";

import { useMemo, useCallback } from "react";

import { useBoolean } from "src/hooks/use-boolean";
import { useLocalStorage } from "src/hooks/use-local-storage";

import { ENV } from "src/config-global";
import { cookies } from "src/consts/cookies";

import CookiesBanner from "./cookies-banner";

// ----------------------------------------------------------------------

export default function CookiesManager() {
  const defaultCookies = useMemo(
    () =>
      cookies.reduce((acc: { [cookie: string]: boolean }, cookie) => {
        acc[cookie.type] = cookie.disabled;
        return acc;
      }, {}),
    [],
  );

  const { state, update } = useLocalStorage("cookies", { ...defaultCookies, consent: false });

  const cookieFormOpen = useBoolean();

  const handleConfirm = useCallback(
    (selectedCookies: { [cookie: string]: boolean }) => {
      update("consent", true);
      Object.keys(selectedCookies).forEach((cookie) => update(cookie, selectedCookies[cookie]));
      window.gtag("consent", "update", {
        analytics_storage: selectedCookies.analytics && ENV === "PROD" ? "granted" : "denied",
      });
      cookieFormOpen.onFalse();
    },
    [cookieFormOpen, update],
  );

  if (!state.consent) {
    return <CookiesBanner open onConfirm={handleConfirm} />;
  }
}
