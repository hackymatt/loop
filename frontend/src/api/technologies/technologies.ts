import { AxiosError } from "axios";
import { compact } from "lodash-es";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

import { formatQueryParams } from "src/utils/query-params";

import { IQueryParams } from "src/types/query-params";
import { ICourseByTechnologyProps } from "src/types/course";

import { Api } from "../service";
import { getCsrfToken } from "../utils";

const endpoint = "/technologies" as const;

type ITechnology = {
  id: string;
  modified_at: string;
  created_at: string;
  name: string;
};

type ICreateTechnology = Pick<ITechnology, "name">;

type ICreateTechnologyReturn = ICreateTechnology;

export const technologiesQuery = (query?: IQueryParams) => {
  const url = endpoint;
  const urlParams = formatQueryParams(query);

  const queryFn = async () => {
    const { data } = await Api.get(`${url}?${urlParams}`);
    const { results, records_count, pages_count } = data;
    const modifiedResults = results.map(({ id, name, created_at }: ITechnology) => ({
      id,
      name,
      createdAt: created_at,
    }));
    return { results: modifiedResults, count: records_count, pagesCount: pages_count };
  };

  return { url, queryFn, queryKey: compact([url, urlParams]) };
};

export const useTechnologies = (query?: IQueryParams, enabled: boolean = true) => {
  const { queryKey, queryFn } = technologiesQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn, enabled });
  return { data: data?.results as ICourseByTechnologyProps[], count: data?.count, ...rest };
};

export const useTechnologiesPagesCount = (query?: IQueryParams) => {
  const { queryKey, queryFn } = technologiesQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.pagesCount, ...rest };
};

export const useCreateTechnology = () => {
  const queryClient = useQueryClient();
  return useMutation<ICreateTechnologyReturn, AxiosError, ICreateTechnology>(
    async (variables) => {
      const result = await Api.post(endpoint, variables, {
        headers: {
          "X-CSRFToken": getCsrfToken(),
        },
      });
      return result.data;
    },
    {
      onSuccess: () => {
        queryClient.invalidateQueries({ queryKey: [endpoint] });
      },
    },
  );
};
