import { compact } from "lodash-es";
import { useQuery } from "@tanstack/react-query";

import { IStatistics } from "src/types/statistics";

import { Api } from "../service";

const statsEndpoint = "/stats" as const;

export const statisticsQuery = () => {
  const url = statsEndpoint;

  const queryFn = async () => {
    const { data } = await Api.get(url);
    return { results: data };
  };

  return { url, queryFn, queryKey: compact([url]) };
};

export const useStatistics = () => {
  const { queryKey, queryFn } = statisticsQuery();
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.results as IStatistics, ...rest };
};
