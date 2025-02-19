import { AxiosError } from "axios";
import { useMutation } from "@tanstack/react-query";

import { Api } from "../service";
import { getCsrfToken } from "../utils";

const endpoint = "/login" as const;

export type ILogin = {
  email: string;
  password: string;
};

export type ILoginReturn = {
  first_name?: string;
  last_name?: string;
  email: string;
  login?: string;
  user_type?: string;
};

export const useLogin = (onResult: () => void) =>
  useMutation<ILoginReturn, AxiosError, ILogin>(
    async (variables) => {
      const result = await Api.post(endpoint, variables, {
        headers: {
          "X-CSRFToken": getCsrfToken(),
        },
      });
      return result.data;
    },
    {
      onSuccess: onResult,
      onError: onResult,
    },
  );
