import { AxiosError } from "axios";
import { useMutation } from "@tanstack/react-query";

import { Api } from "../service";

const endpoint = "/verify-code" as const;

export type IVerifyCode = {
  email: string;
};

export type IVerifyCodeReturn = IVerifyCode & {
  code?: string;
};

export const useVerifyCode = () =>
  useMutation<IVerifyCodeReturn, AxiosError, IVerifyCode>(async (variables) => {
    const result = await Api.post(endpoint, variables);
    return result.data;
  });
