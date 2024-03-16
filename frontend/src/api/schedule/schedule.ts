import { AxiosError } from "axios";
import { useMutation, useQueryClient } from "@tanstack/react-query";

import { Api } from "../service";
import { getCsrfToken } from "../utils/csrf";

const endpoint = "/schedules" as const;

type IDeleteSchedule = {};

type IDeleteScheduleReturn = {};

export const useDeleteSchedule = (id: string) => {
  const queryClient = useQueryClient();
  const url = `${endpoint}/${id}`;
  return useMutation<IDeleteScheduleReturn, AxiosError, IDeleteSchedule>(
    async () => {
      const result = await Api.delete(url, {
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
