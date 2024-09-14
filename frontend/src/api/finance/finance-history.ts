import { compact } from "lodash-es";
import { useQuery } from "@tanstack/react-query";

import { formatQueryParams } from "src/utils/query-params";

import { IGender } from "src/types/testimonial";
import { IQueryParams } from "src/types/query-params";
import { IFinanceHistoryProp } from "src/types/finance";

import { Api } from "../service";

const endpoint = "/finance-history" as const;

type ILecturer = {
  id: string;
  full_name: string;
  image: string | null;
  gender: IGender;
};

type IFinanceHistory = {
  id: string;
  lecturer: ILecturer;
  account: string | null;
  rate: number | null;
  commission: number | null;
  created_at: string;
};

export const financeHistoryQuery = (query?: IQueryParams) => {
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
    const modifiedResults = results.map(
      ({ id, lecturer, account, rate, commission, created_at }: IFinanceHistory) => {
        const { id: lecturerId, full_name, gender, image } = lecturer;
        return {
          id,
          teacher: { id: lecturerId, name: full_name, avatarUrl: image, gender },
          account,
          rate,
          commission,
          createdAt: created_at,
        };
      },
    );
    return { results: modifiedResults, count: records_count, pagesCount: pages_count };
  };

  return { url, queryFn, queryKey: compact([endpoint, urlParams]) };
};
export const useFinanceHistory = (query?: IQueryParams, enabled: boolean = true) => {
  const { queryKey, queryFn } = financeHistoryQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn, enabled });
  return { data: data?.results as IFinanceHistoryProp[], count: data?.count, ...rest };
};

export const useFinanceHistoryPagesCount = (query?: IQueryParams) => {
  const { queryKey, queryFn } = financeHistoryQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.pagesCount, ...rest };
};
