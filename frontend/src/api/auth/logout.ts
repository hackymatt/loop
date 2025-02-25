import { AxiosError } from "axios";
import { useMutation, useQueryClient } from "@tanstack/react-query";

import { Api } from "../service";
import { getCsrfToken } from "../utils";

const endpoint = "/logout" as const;

export type ILogout = {};

export type ILogoutReturn = ILogout;

export const useLogout = () => {
  const queryClient = useQueryClient();
  return useMutation<ILogoutReturn, AxiosError, ILogout>(
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
        queryClient.invalidateQueries({ queryKey: ["/personal-data"] });
        queryClient.invalidateQueries({ queryKey: ["/courses"] });
      },
    },
  );
};
