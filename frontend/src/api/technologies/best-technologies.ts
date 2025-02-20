import { compact } from "lodash-es";
import { useQuery } from "@tanstack/react-query";

import { formatQueryParams } from "src/utils/query-params";

import { IQueryParams } from "src/types/query-params";
import { IBestTechnologyProps } from "src/types/technology";

import { getListData } from "../utils";
import { ListQueryResponse } from "../types";

const endpoint = "/best-technologies" as const;

type ITechnology = {
  id: string;
  courses_count: number;
  modified_at: string;
  created_at: string;
  name: string;
};

export const bestTechnologiesQuery = (query?: IQueryParams) => {
  const url = endpoint;
  const urlParams = formatQueryParams(query);
  const queryUrl = `${url}?${urlParams}`;

  const queryFn = async (): Promise<ListQueryResponse<IBestTechnologyProps[]>> => {
    const { results, records_count, pages_count } = await getListData<ITechnology>(queryUrl);
    const modifiedResults = results.map(({ id, name, courses_count, created_at }: ITechnology) => ({
      id,
      name,
      coursesCount: courses_count,
      createdAt: created_at,
    }));
    return { results: modifiedResults, count: records_count, pagesCount: pages_count };
  };

  return { url, queryFn, queryKey: compact([url, urlParams]) };
};

export const useBestTechnologies = (query?: IQueryParams) => {
  const { queryKey, queryFn } = bestTechnologiesQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.results, count: data?.count, ...rest };
};
