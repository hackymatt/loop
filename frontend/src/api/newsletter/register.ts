import { AxiosError } from "axios";
import { useMutation } from "@tanstack/react-query";

import { Api } from "../service";

const endpoint = "/newsletter-subscribe" as const;

type INewsletter = {
  email: string;
};

export const useRegisterNewsletter = () =>
  useMutation<INewsletter, AxiosError, INewsletter>(async (variables) => {
    const result = await Api.post(endpoint, variables);
    return result.data as INewsletter;
  });
