import { AxiosError } from "axios";
import { useMutation } from "@tanstack/react-query";

import { Api } from "../service";

const endpoint = "/newsletter-unsubscribe" as const;

type INewsletter = {
  uuid: string;
};

export const useUnregisterNewsletter = () =>
  useMutation<INewsletter, AxiosError, INewsletter>(async ({ uuid, ...variables }) => {
    const result = await Api.put(`${endpoint}/${uuid}`, variables);
    return result.data as INewsletter;
  });
