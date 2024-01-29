import { useMutation } from "@tanstack/react-query";

import { Api } from "../service";

const endpoint = "/newsletter-subscribe" as const;

export const useRegisterNewsletter = () =>
  useMutation({
    mutationFn: (newsletter: { email: string }) =>
      Api.post(endpoint, newsletter).then((response) => response.data),
  });
