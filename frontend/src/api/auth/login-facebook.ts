import { AxiosError } from "axios";
import { useMutation } from "@tanstack/react-query";

import { Api } from "../service";
import { getCsrfToken } from "../utils";

const endpoint = "/login-facebook" as const;

export type ILoginFacebook = {
  code: string;
};

export type ILoginFacebookReturn = {
  first_name?: string;
  last_name?: string;
  email: string;
  login?: string;
  user_type?: string;
};

export const useLoginFacebook = (onResult: () => void) =>
  useMutation<ILoginFacebookReturn, AxiosError, ILoginFacebook>(
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
