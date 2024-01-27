import { useMemo } from "react";
import { useRouter, usePathname, useSearchParams } from "next/navigation";

import { IQueryParamValue } from "src/types/queryParams";

export function useQueryParams() {
  const searchParams = useSearchParams();
  const params = useMemo(() => new URLSearchParams(searchParams), [searchParams]);

  const pathname = usePathname();
  const { replace } = useRouter();

  const setQueryParam = (name: string, value?: IQueryParamValue) => {
    params.set(name, value ? value.toString() : "");
    replace(`${pathname}?${params.toString()}`);
  };

  const removeQueryParam = (name: string) => {
    params.delete(name);
    replace(`${pathname}?${params.toString()}`);
  };

  const getQueryParam = (name: string) => params.get(name);

  const getQueryParams = () => Object.fromEntries(params);

  return { getQueryParam, setQueryParam, removeQueryParam, getQueryParams };
}
