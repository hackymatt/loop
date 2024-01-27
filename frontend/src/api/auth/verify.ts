import { AxiosError } from "axios";
import { useMutation } from "@tanstack/react-query";

import { Api } from "../service";

const endpoint = "/verify" as const;

type IVerify = {
  email: string;
  code: string;
};

export const useVerify = () =>
  useMutation<IVerify, AxiosError, IVerify>(async (variables) => {
    const result = await Api.post(endpoint, variables);
    return result.data;
  });
