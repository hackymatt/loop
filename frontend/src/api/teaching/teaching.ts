import { AxiosError } from "axios";
import { useMutation, useQueryClient } from "@tanstack/react-query";

import { Api } from "../service";
import { getCsrfToken } from "../utils";

const endpoint = "/teaching" as const;

type IDeleteTechnology = { id: string };

type IDeleteTechnologyReturn = {};

export const useDeleteTeaching = () => {
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
