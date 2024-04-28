import { compact } from "lodash-es";
import { useQuery } from "@tanstack/react-query";

import { formatQueryParams } from "src/utils/query-params";

import { ICouponUsageProps } from "src/types/coupon";
import { IQueryParams } from "src/types/query-params";

import { Api } from "../service";

const endpoint = "/coupon-usage" as const;

export const couponUsageQuery = (query?: IQueryParams) => {
  const url = endpoint;
  const urlParams = formatQueryParams(query);
  const queryUrl = urlParams ? `${url}?${urlParams}` : url;

  const queryFn = async () => {
    let data;
    try {
      const response = await Api.get(queryUrl);
      ({ data } = response);
    } catch (error) {
      if (error.response && (error.response.status === 400 || error.response.status === 404)) {
        data = { results: [], records_count: 0, pages_count: 0 };
      }
    }
    const { results, records_count, pages_count } = data;
    return { results, count: records_count, pagesCount: pages_count };
  };

  return { url, queryFn, queryKey: compact([endpoint, urlParams]) };
};
export const useCouponUsage = (query?: IQueryParams) => {
  const { queryKey, queryFn } = couponUsageQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.results as ICouponUsageProps[], count: data?.count, ...rest };
};

export const useCouponUsagePagesCount = (query?: IQueryParams) => {
  const { queryKey, queryFn } = couponUsageQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.pagesCount, ...rest };
};
