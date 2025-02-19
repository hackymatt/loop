import { AxiosError } from "axios";
import { useMutation } from "@tanstack/react-query";

import { Api } from "../service";
import { getCsrfToken } from "../utils";

const endpoint = "/password-reset" as const;

export type IPasswordReset = {
  email: string;
};

export type IPasswordResetReturn = IPasswordReset & {
  password_reset?: string;
};

export const usePasswordReset = () =>
  useMutation<IPasswordResetReturn, AxiosError, IPasswordReset>(async (variables) => {
    const result = await Api.post(endpoint, variables, {
      headers: {
        "X-CSRFToken": getCsrfToken(),
      },
    });
    return result.data;
  });
