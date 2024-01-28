import { AxiosError } from "axios";
import { useMutation } from "@tanstack/react-query";

import { Api } from "../service";

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
};

export const useLogin = () =>
  useMutation<ILoginReturn, AxiosError, ILogin>(async (variables) => {
    const result = await Api.post(endpoint, variables);
    return result.data;
  });
