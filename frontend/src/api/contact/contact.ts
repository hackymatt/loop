import { useMutation } from "@tanstack/react-query";

import { Api } from "../service";

const endpoint = "/contact" as const;

type IContact = {
  full_name: string;
  email: string;
  subject: string;
  message: string;
};

export const useContact = () =>
  useMutation<IContact, IContact, IContact>(async (variables) => {
    const result = await Api.post(endpoint, variables);
    return result.data as IContact;
  });
