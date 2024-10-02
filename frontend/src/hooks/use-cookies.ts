import { useMemo } from "react";

import { cookies } from "src/consts/cookies";

export function useCookies() {
  const defaultCookies = useMemo(
    () =>
      cookies.reduce((acc: { [cookie: string]: boolean }, cookie) => {
        acc[cookie.type] = cookie.disabled;
        return acc;
      }, {}),
    [],
  );

  return { cookies, defaultCookies };
}
