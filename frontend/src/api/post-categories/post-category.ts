import { AxiosError } from "axios";
import { compact } from "lodash-es";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

import { ICourseByTechnologyProps } from "src/types/course";

import { Api } from "../service";
import { getCsrfToken } from "../utils/csrf";

const endpoint = "/post-categories" as const;

type ICategory = {
  id: string;
  modified_at: string;
  created_at: string;
  name: string;
};

type IEditCategory = Pick<ICategory, "name">;

type IEditCategoryReturn = IEditCategory;

type IDeleteCategory = { id: string };

type IDeleteCategoryReturn = {};

export const postCategoryQuery = (id: string) => {
  const url = endpoint;
  const queryUrl = `${url}/${id}`;

  const queryFn = async () => {
    const response = await Api.get<ICategory>(queryUrl);
    const { data } = response;
    const { id: categoryId, name, created_at } = data;

    const modifiedResults = {
      id: categoryId,
      name,
      createdAt: created_at,
    };
    return { results: modifiedResults };
  };

  return { url, queryFn, queryKey: compact([endpoint, id]) };
};

export const usePostCategory = (id: string) => {
  const { queryKey, queryFn } = postCategoryQuery(id);
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.results as any as ICourseByTechnologyProps, ...rest };
};

export const useEditPostCategory = (id: string) => {
  const queryClient = useQueryClient();
  const url = `${endpoint}/${id}`;
  return useMutation<IEditCategoryReturn, AxiosError, IEditCategory>(
    async (variables) => {
      const result = await Api.put(url, variables, {
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

export const useDeletePostCategory = () => {
  const queryClient = useQueryClient();
  return useMutation<IDeleteCategoryReturn, AxiosError, IDeleteCategory>(
    async ({ id }) => {
      const result = await Api.delete(`${endpoint}/${id}`, {
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
