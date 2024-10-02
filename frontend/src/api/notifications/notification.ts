import { AxiosError } from "axios";
import { useMutation, useQueryClient } from "@tanstack/react-query";

import { Api } from "../service";
import { getCsrfToken } from "../utils/csrf";

const endpoint = "/notifications" as const;

type IEditNotification = { id: string; status: string };

type IEditNotificationReturn = IEditNotification;

export const useEditNotification = (id: string) => {
  const queryClient = useQueryClient();
  const url = `${endpoint}/${id}`;
  return useMutation<IEditNotificationReturn, AxiosError, IEditNotification>(
    async (variables) => {
      const result = await Api.put(url, variables, {
        headers: {
          "X-CSRFToken": getCsrfToken(),
        },
      });
      return result.data;
    },
    {
      onSuccess: () => {
        queryClient.invalidateQueries({ queryKey: [endpoint] });
      },
    },
  );
};
