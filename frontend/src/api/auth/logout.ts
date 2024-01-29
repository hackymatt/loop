import { AxiosError } from "axios";
import { useMutation } from "@tanstack/react-query";

import { Api } from "../service";

const endpoint = "/logout" as const;

export type ILogout = {};

export type ILogoutReturn = ILogout;

export const useLogout = () =>
  useMutation<ILogoutReturn, AxiosError, ILogout>(async (variables) => {
    const result = await Api.post(endpoint, variables);
    return result.data;
  });
