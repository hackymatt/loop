import { AxiosError } from "axios";
import { useMutation } from "@tanstack/react-query";

import { Api } from "../service";

const endpoint = "/register" as const;

type IRegister = {
  first_name: string;
  last_name: string;
  email: string;
  password: string;
  password2: string;
};

type IRegisterReturn = Omit<IRegister, "password" | "password2">;

export const useRegister = () =>
  useMutation<IRegisterReturn, AxiosError, IRegister>(async (variables) => {
    const result = await Api.post(endpoint, variables);
    return result.data;
  });
