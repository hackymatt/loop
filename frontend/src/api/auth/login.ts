import { AxiosError } from "axios";
import { useMutation } from "@tanstack/react-query";

import { Api } from "../service";

const endpoint = "/login" as const;

type ILogin = {
  email: string;
  password: string;
};

export const useLogin = () =>
  useMutation<ILogin, AxiosError, ILogin>(async (variables) => {
    const result = await Api.post(endpoint, variables);
    return result.data;
  });
