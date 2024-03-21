import { AxiosError } from "axios";
import { useMutation, useQueryClient } from "@tanstack/react-query";

import { Api } from "../service";
import { getCsrfToken } from "../utils/csrf";
import { purchaseQuery } from "../purchase/purchase";
import { lessonSchedulesQuery } from "../lesson-schedules/lesson-schedules";

const endpoint = "/reservation" as const;

type IDeleteReservation = {};

type IDeleteReservationReturn = {};

export const useDeleteReservation = (id: string) => {
  const queryClient = useQueryClient();
  const url = `${endpoint}/${id}`;
  return useMutation<IDeleteReservationReturn, AxiosError, IDeleteReservation>(
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
        queryClient.invalidateQueries({ queryKey: purchaseQuery().queryKey });
        queryClient.invalidateQueries({ queryKey: lessonSchedulesQuery().queryKey });
      },
    },
  );
};
