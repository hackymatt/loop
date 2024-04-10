import { AxiosError } from "axios";
import { useMutation } from "@tanstack/react-query";

import { Api } from "../service";

const endpoint = "/newsletter-unsubscribe" as const;

type IEditNewsletter = { uuid: string };
type IEditNewsletterReturn = IEditNewsletter;
export const useUnregisterNewsletter = () =>
  useMutation<IEditNewsletterReturn, AxiosError, IEditNewsletter>(
    async ({ uuid, ...variables }) => {
      const result = await Api.put(`${endpoint}/${uuid}`, variables);
      return result.data;
    },
  );
