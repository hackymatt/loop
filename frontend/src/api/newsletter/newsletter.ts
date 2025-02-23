import { compact } from "lodash-es";
import { useQuery } from "@tanstack/react-query";

import { formatQueryParams } from "src/utils/query-params";

import { IQueryParams } from "src/types/query-params";
import { INewsletterProps } from "src/types/newsletter";

import { getListData } from "../utils";
import { ListQueryResponse } from "../types";

const endpoint = "/newsletter" as const;

type INewsletter = {
  uuid: string;
  email: string;
  active: boolean;
  created_at: string;
};

export const newsletterQuery = (query?: IQueryParams) => {
  const url = endpoint;
  const urlParams = formatQueryParams(query);
  const queryUrl = urlParams ? `${url}?${urlParams}` : url;

  const queryFn = async (): Promise<ListQueryResponse<INewsletterProps[]>> => {
    const { results, records_count, pages_count } = await getListData<INewsletter>(queryUrl);
    const modifiedResults = (results ?? []).map(({ created_at, ...rest }: INewsletter) => ({
      ...rest,
      createdAt: created_at,
    }));
    return { results: modifiedResults, count: records_count, pagesCount: pages_count };
  };

  return { url, queryFn, queryKey: compact([endpoint, urlParams]) };
};

export const useNewsletter = (query?: IQueryParams, enabled: boolean = true) => {
  const { queryKey, queryFn } = newsletterQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn, enabled });
  return { data: data?.results, count: data?.count, ...rest };
};

export const useNewsletterPagesCount = (query?: IQueryParams) => {
  const { queryKey, queryFn } = newsletterQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.pagesCount, ...rest };
};
