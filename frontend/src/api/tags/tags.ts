import { AxiosError } from "axios";
import { compact } from "lodash-es";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

import { formatQueryParams } from "src/utils/query-params";

import { ITagProps } from "src/types/tags";
import { IQueryParams } from "src/types/query-params";

import { Api } from "../service";
import { getCsrfToken } from "../utils/csrf";

const endpoint = "/tags" as const;

type ITag = {
  id: string;
  modified_at: string;
  created_at: string;
  name: string;
};

type ICreateTag = Pick<ITag, "name">;

type ICreateTagReturn = ICreateTag;

export const tagsQuery = (query?: IQueryParams) => {
  const url = endpoint;
  const urlParams = formatQueryParams(query);

  const queryFn = async () => {
    const { data } = await Api.get(`${url}?${urlParams}`);
    const { results, records_count, pages_count } = data;
    const modifiedResults = results.map(({ id, name, created_at }: ITag) => ({
      id,
      name,
      createdAt: created_at,
    }));
    return { results: modifiedResults, count: records_count, pagesCount: pages_count };
  };

  return { url, queryFn, queryKey: compact([url, urlParams]) };
};

export const useTags = (query?: IQueryParams, enabled: boolean = true) => {
  const { queryKey, queryFn } = tagsQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn, enabled });
  return { data: data?.results as ITagProps[], count: data?.count, ...rest };
};

export const useTagsPagesCount = (query?: IQueryParams) => {
  const { queryKey, queryFn } = tagsQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.pagesCount, ...rest };
};

export const useCreateTag = () => {
  const queryClient = useQueryClient();
  return useMutation<ICreateTagReturn, AxiosError, ICreateTag>(
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
