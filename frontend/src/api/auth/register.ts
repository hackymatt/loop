import { AxiosError } from "axios";
import { useMutation } from "@tanstack/react-query";

import { Api } from "../service";
import { getCsrfToken } from "../utils";

const endpoint = "/register" as const;

export type IRegister = {
  first_name: string;
  last_name: string;
  email: string;
  password: string;
  password2: string;
  newsletter: boolean;
};

export type IRegisterReturn = Omit<IRegister, "password" | "password2">;

export const useRegister = () =>
  useMutation<IRegisterReturn, AxiosError, IRegister>(async (variables) => {
    const result = await Api.post(endpoint, variables, {
      headers: {
        "X-CSRFToken": getCsrfToken(),
      },
    });
    return result.data;
  });
