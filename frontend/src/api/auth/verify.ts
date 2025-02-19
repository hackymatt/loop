import { AxiosError } from "axios";
import { useMutation } from "@tanstack/react-query";

import { Api } from "../service";
import { getCsrfToken } from "../utils";

const endpoint = "/verify" as const;

export type IVerify = {
  email: string;
  code: string;
};

export type IVerifyReturn = Pick<IVerify, "email"> & { code?: string };

export const useVerify = () =>
  useMutation<IVerifyReturn, AxiosError, IVerify>(async (variables) => {
    const result = await Api.post(endpoint, variables, {
      headers: {
        "X-CSRFToken": getCsrfToken(),
      },
    });
    return result.data;
  });
