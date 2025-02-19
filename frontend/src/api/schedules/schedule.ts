import { AxiosError } from "axios";
import { useMutation, useQueryClient } from "@tanstack/react-query";

import { Api } from "../service";
import { getCsrfToken } from "../utils";

const endpoint = "/schedules" as const;

type IDeleteSchedule = { id: string };

type IDeleteScheduleReturn = {};

export const useDeleteSchedule = () => {
  const queryClient = useQueryClient();
  return useMutation<IDeleteScheduleReturn, AxiosError, IDeleteSchedule>(
    async ({ id }) => {
      const result = await Api.delete(`${endpoint}/${id}`, {
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
