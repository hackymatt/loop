import { AxiosError } from "axios";
import { compact } from "lodash-es";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

import { ITagProps } from "src/types/tags";

import { Api } from "../service";
import { getCsrfToken } from "../utils";

const endpoint = "/tags" as const;

type ITag = {
  id: string;
  created_at: string;
  name: string;
};

type IEditTag = Pick<ITag, "name">;

type IEditTagReturn = IEditTag;

type IDeleteTag = { id: string };

type IDeleteTagReturn = {};

export const tagQuery = (id: string) => {
  const url = endpoint;
  const queryUrl = `${url}/${id}`;

  const queryFn = async () => {
    const response = await Api.get<ITag>(queryUrl);
    const { data } = response;
    const { id: tagId, name, created_at } = data;

    const modifiedResults = {
      id: tagId,
      name,
      createdAt: created_at,
    };
    return { results: modifiedResults };
  };

  return { url, queryFn, queryKey: compact([endpoint, id]) };
};

export const useTag = (id: string) => {
  const { queryKey, queryFn } = tagQuery(id);
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.results as any as ITagProps, ...rest };
};

export const useEditTag = (id: string) => {
  const queryClient = useQueryClient();
  const url = `${endpoint}/${id}`;
  return useMutation<IEditTagReturn, AxiosError, IEditTag>(
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

export const useDeleteTag = () => {
  const queryClient = useQueryClient();
  return useMutation<IDeleteTagReturn, AxiosError, IDeleteTag>(
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
