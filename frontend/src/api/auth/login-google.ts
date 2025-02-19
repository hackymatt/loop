import { AxiosError } from "axios";
import { useMutation } from "@tanstack/react-query";

import { Api } from "../service";
import { getCsrfToken } from "../utils";

const endpoint = "/login-google" as const;

export type ILoginGoogle = {
  code: string;
};

export type ILoginGoogleReturn = {
  first_name?: string;
  last_name?: string;
  email: string;
  login?: string;
  user_type?: string;
};

export const useLoginGoogle = (onResult: () => void) =>
  useMutation<ILoginGoogleReturn, AxiosError, ILoginGoogle>(
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
