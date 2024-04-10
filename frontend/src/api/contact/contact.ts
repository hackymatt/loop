import { AxiosError } from "axios";
import { useMutation } from "@tanstack/react-query";

import { Api } from "../service";

const endpoint = "/contact" as const;

type ICreateContact = {
  full_name: string;
  email: string;
  subject: string;
  message: string;
};
type ICreateContactrReturn = ICreateContact;

export const useContact = () =>
  useMutation<ICreateContactrReturn, AxiosError, ICreateContact>(async (variables) => {
    const result = await Api.post(endpoint, variables);
    return result.data;
  });
