import { useMutation } from "@tanstack/react-query";

import { Api } from "../service";

const endpoint = "/newsletter-subscribe" as const;

type INewsletter = {
  email: string;
};

export const useRegisterNewsletter = () =>
  useMutation<INewsletter, INewsletter, INewsletter>(async (variables) => {
    const result = await Api.post(endpoint, variables);
    return result.data as INewsletter;
  });
