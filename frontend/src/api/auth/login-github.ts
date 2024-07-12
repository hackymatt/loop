import { AxiosError } from "axios";
import { useMutation } from "@tanstack/react-query";

import { Api } from "../service";
import { getCsrfToken } from "../utils/csrf";

const endpoint = "/login-github" as const;

export type ILoginGithub = {
  code: string;
};

export type ILoginGithubReturn = {
  first_name?: string;
  last_name?: string;
  email: string;
  login?: string;
  user_type?: string;
};

export const useLoginGithub = () =>
  useMutation<ILoginGithubReturn, AxiosError, ILoginGithub>(async (variables) => {
    const result = await Api.post(endpoint, variables, {
      headers: {
        "X-CSRFToken": getCsrfToken(),
      },
    });
    return result.data;
  });
