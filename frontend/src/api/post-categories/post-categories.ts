import { AxiosError } from "axios";
import { compact } from "lodash-es";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

import { formatQueryParams } from "src/utils/query-params";

import { IPostCategoryProps } from "src/types/blog";
import { IQueryParams } from "src/types/query-params";

import { Api } from "../service";
import { getCsrfToken } from "../utils/csrf";

const endpoint = "/post-categories" as const;

type ICategory = {
  id: string;
  modified_at: string;
  created_at: string;
  name: string;
};

type ICreateCategory = Pick<ICategory, "name">;

type ICreateCategoryReturn = ICreateCategory;

export const postCategoriesQuery = (query?: IQueryParams) => {
  const url = endpoint;
  const urlParams = formatQueryParams(query);

  const queryFn = async () => {
    const { data } = await Api.get(`${url}?${urlParams}`);
    const { results, records_count, pages_count } = data;
    const modifiedResults = results.map(({ id, name, created_at }: ICategory) => ({
      id,
      name,
      createdAt: created_at,
    }));
    return { results: modifiedResults, count: records_count, pagesCount: pages_count };
  };

  return { url, queryFn, queryKey: compact([url, urlParams]) };
};

export const usePostCategories = (query?: IQueryParams, enabled: boolean = true) => {
  const { queryKey, queryFn } = postCategoriesQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn, enabled });
  return { data: data?.results as IPostCategoryProps[], count: data?.count, ...rest };
};

export const usePostCategoriesPagesCount = (query?: IQueryParams) => {
  const { queryKey, queryFn } = postCategoriesQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.pagesCount, ...rest };
};

export const useCreateCategory = () => {
  const queryClient = useQueryClient();
  return useMutation<ICreateCategoryReturn, AxiosError, ICreateCategory>(
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
