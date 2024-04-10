import { AxiosError } from "axios";
import { useMutation } from "@tanstack/react-query";

import { Api } from "../service";

const endpoint = "/newsletter-subscribe" as const;

type ICreateNewsletter = { email: string };
type ICreateNewsletterReturn = ICreateNewsletter;
export const useRegisterNewsletter = () =>
  useMutation<ICreateNewsletterReturn, AxiosError, ICreateNewsletter>(async (variables) => {
    const result = await Api.post(endpoint, variables);
    return result.data;
  });
