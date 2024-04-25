import { AxiosError } from "axios";
import { useMutation } from "@tanstack/react-query";

import { Api } from "../service";
import { getCsrfToken } from "../utils/csrf";

const endpoint = "/login-facebook" as const;

export type ILoginFacebook = {
  code: string;
};

export type ILoginFacebookReturn = {
  first_name?: string;
  last_name?: string;
  email: string;
  login?: string;
};

export const useLoginFacebook = () =>
  useMutation<ILoginFacebookReturn, AxiosError, ILoginFacebook>(async (variables) => {
    const result = await Api.post(endpoint, variables, {
      headers: {
        "X-CSRFToken": getCsrfToken(),
      },
    });
    return result.data;
  });
