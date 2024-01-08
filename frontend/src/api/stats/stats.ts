import { compact } from "lodash-es";
import { useQuery } from "@tanstack/react-query";

import { IStats } from "src/interfaces/stats";

import { Api } from "../service";

const statsEndpoint = "/stats" as const;
export const statsQuery = () => {
  const url = statsEndpoint;

  const queryFn = async () => {
    const { data } = await Api.get(url);
    const { results, count } = data;
    return { results, count };
  };

  return { url, queryFn, queryKey: compact([url]) };
};

export const useStats = () => {
  const { queryKey, queryFn } = statsQuery();
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.results as IStats, ...rest };
};
