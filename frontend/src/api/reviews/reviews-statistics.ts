import { compact } from "lodash-es";
import { useQuery } from "@tanstack/react-query";

import { formatQueryParams } from "src/utils/query-params";

import { IReviewStatistic } from "src/types/review";
import { IQueryParams } from "src/types/query-params";

import { Api } from "../service";

const endpoint = "/reviews-stats" as const;

export const reviewsStatisticsQuery = (query?: IQueryParams) => {
  const url = endpoint;
  const urlParams = formatQueryParams(query);
  const queryUrl = urlParams ? `${url}?${urlParams}` : url;

  const queryFn = async () => {
    const { data } = await Api.get(queryUrl);
    const { results, records_count, pages_count } = data;
    return { results, count: records_count, pagesCount: pages_count };
  };

  return { url, queryFn, queryKey: compact([queryUrl]) };
};

export const useReviewsStatistics = (query?: IQueryParams) => {
  const { queryKey, queryFn } = reviewsStatisticsQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.results as IReviewStatistic[], ...rest };
};
