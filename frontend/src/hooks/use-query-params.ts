import { useMemo, useCallback } from "react";
import { useRouter, usePathname, useSearchParams } from "next/navigation";

import { IQueryParamValue } from "src/types/query-params";

export function useQueryParams() {
  const searchParams = useSearchParams();
  const params = useMemo(() => new URLSearchParams(searchParams), [searchParams]);

  const pathname = usePathname();
  const { replace } = useRouter();

  const setQueryParam = useCallback(
    (name: string, value?: IQueryParamValue) => {
      params.set(name, value ? value.toString() : "");
      replace(`${pathname}?${params.toString()}`);
    },
    [params, pathname, replace],
  );

  const removeQueryParam = useCallback(
    (name: string) => {
      params.delete(name);
      replace(`${pathname}?${params.toString()}`);
    },
    [params, pathname, replace],
  );

  const getQueryParam = useCallback((name: string) => params.get(name), [params]);

  const getQueryParams = useCallback(() => Object.fromEntries(params), [params]);

  return { getQueryParam, setQueryParam, removeQueryParam, getQueryParams };
}
