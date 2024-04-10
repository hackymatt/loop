import { AxiosError } from "axios";
import { useMutation, useQueryClient } from "@tanstack/react-query";

import { Api } from "../service";
import { getCsrfToken } from "../utils/csrf";

const endpoint = "/cart" as const;

type IDeleteCart = { id: string };

type IDeleteCartReturn = {};

export const useDeleteCart = () => {
  const queryClient = useQueryClient();
  return useMutation<IDeleteCartReturn, AxiosError, IDeleteCart>(
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
