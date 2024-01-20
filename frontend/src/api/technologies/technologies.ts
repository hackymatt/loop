import { compact } from "lodash-es";
import { useQuery } from "@tanstack/react-query";

import { formatQueryParams } from "src/utils/query-params";

import { IQueryParams } from "src/types/queryParams";
import { ICourseByCategoryProps } from "src/types/course";

import { Api } from "../service";

const endpoint = "/technologies" as const;

type ITechnology = {
  id: number;
  courses_count: number;
  modified_at: string;
  created_at: string;
  name: string;
};

export const technologiesQuery = (query?: IQueryParams) => {
  const url = endpoint;
  const urlParams = formatQueryParams(query);

  const queryFn = async () => {
    const { data } = await Api.get(`${url}?${urlParams}`);
    const { results, records_count } = data;
    const modifiedResults = results.map(({ id, name, courses_count }: ITechnology) => ({
      id,
      name,
      totalStudents: courses_count,
    }));
    return { results: modifiedResults, count: records_count };
  };

  return { url, queryFn, queryKey: compact([url, urlParams]) };
};

export const useTechnologies = (query?: IQueryParams) => {
  const { queryKey, queryFn } = technologiesQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.results as ICourseByCategoryProps[], ...rest };
};
