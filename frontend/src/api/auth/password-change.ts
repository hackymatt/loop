import { AxiosError } from "axios";
import { useMutation } from "@tanstack/react-query";

import { Api } from "../service";
import { getCsrfToken } from "../utils";

const endpoint = "/password-change" as const;

export type IPasswordChange = {
  old_password: string;
  password: string;
  password2: string;
};

export type IPasswordChangeReturn = IPasswordChange;

export const usePasswordChange = () =>
  useMutation<IPasswordChangeReturn, AxiosError, IPasswordChange>(async (variables) => {
    const result = await Api.post(endpoint, variables, {
      headers: {
        "X-CSRFToken": getCsrfToken(),
      },
    });
    return result.data;
  });
