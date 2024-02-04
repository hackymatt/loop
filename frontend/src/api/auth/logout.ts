import { AxiosError } from "axios";
import { useMutation } from "@tanstack/react-query";

import { Api } from "../service";
import { getCsrfToken } from "../utils/csrf";

const endpoint = "/logout" as const;

export type ILogout = {};

export type ILogoutReturn = ILogout;

export const useLogout = () =>
  useMutation<ILogoutReturn, AxiosError, ILogout>(async (variables) => {
    const result = await Api.post(endpoint, variables, {
      headers: {
        "X-CSRFToken": getCsrfToken(),
      },
    });
    return result.data;
  });
