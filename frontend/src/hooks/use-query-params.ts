import { useMemo } from "react";
import { useRouter, usePathname, useSearchParams } from "next/navigation";

export const useQueryParams = () => {
  const searchParams = useSearchParams();
  const params = useMemo(() => new URLSearchParams(searchParams), [searchParams]);

  const pathname = usePathname();
  const { replace } = useRouter();

  const setQueryParam = (name: string, value?: string | number) => {
    params.set(name, value ? value.toString() : "");
    replace(`${pathname}?${params.toString()}`);
  };

  const getQueryParam = (name: string) => params.get(name);

  return { getQueryParam, setQueryParam };
};
