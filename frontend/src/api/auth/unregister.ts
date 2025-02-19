import { AxiosError } from "axios";
import { useMutation } from "@tanstack/react-query";

import { Api } from "../service";
import { getCsrfToken } from "../utils";

const endpoint = "/unregister" as const;

export type IUnregisterReturn = {};

export const useUnregister = () =>
  useMutation<IUnregisterReturn, AxiosError>(async () => {
    const result = await Api.delete(endpoint, {
      headers: {
        "X-CSRFToken": getCsrfToken(),
      },
    });
    return result.data;
  });
