import { AxiosError } from "axios";
import { useMutation, useQueryClient } from "@tanstack/react-query";

import { Api } from "../service";
import { getCsrfToken } from "../utils/csrf";

const endpoint = "/technologies" as const;

type ITechnology = {
  id: number;
  modified_at: string;
  created_at: string;
  name: string;
};

type IEditTechnology = Pick<ITechnology, "name">;

type IEditTechnologyReturn = IEditTechnology;

type IDeleteTechnology = {};

type IDeleteTechnologyReturn = {};

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
        queryClient.invalidateQueries({ queryKey: [endpoint, id] });
      },
    },
  );
};

export const useDeleteTechnology = (id: string) => {
  const queryClient = useQueryClient();
  const url = `${endpoint}/${id}`;
  return useMutation<IDeleteTechnologyReturn, AxiosError, IDeleteTechnology>(
    async () => {
      const result = await Api.delete(url, {
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
