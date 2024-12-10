import { AxiosError } from "axios";
import { compact } from "lodash-es";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

import { ICourseByTechnologyProps } from "src/types/course";

import { Api } from "../service";
import { getCsrfToken } from "../utils/csrf";

const endpoint = "/technologies" as const;

type ITechnology = {
  id: string;
  modified_at: string;
  created_at: string;
  name: string;
  description: string;
};

type IEditTechnology = Pick<ITechnology, "name" | "description">;

type IEditTechnologyReturn = IEditTechnology;

type IDeleteTechnology = { id: string };

type IDeleteTechnologyReturn = {};

export const technologyQuery = (id: string) => {
  const url = endpoint;
  const queryUrl = `${url}/${id}`;

  const queryFn = async () => {
    const response = await Api.get<ITechnology>(queryUrl);
    const { data } = response;
    const { id: technologyId, name, description, created_at } = data;

    const modifiedResults = {
      id: technologyId,
      name,
      description,
      createdAt: created_at,
    };
    return { results: modifiedResults };
  };

  return { url, queryFn, queryKey: compact([endpoint, id]) };
};

export const useTechnology = (id: string) => {
  const { queryKey, queryFn } = technologyQuery(id);
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.results as any as ICourseByTechnologyProps, ...rest };
};

export const useEditTechnology = (id: string) => {
  const queryClient = useQueryClient();
  const url = `${endpoint}/${id}`;
  return useMutation<IEditTechnologyReturn, AxiosError, IEditTechnology>(
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

export const useDeleteTechnology = () => {
  const queryClient = useQueryClient();
  return useMutation<IDeleteTechnologyReturn, AxiosError, IDeleteTechnology>(
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
