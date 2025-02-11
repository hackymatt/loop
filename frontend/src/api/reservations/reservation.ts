import { AxiosError } from "axios";
import { useMutation, useQueryClient } from "@tanstack/react-query";

import { Api } from "../service";
import { getCsrfToken } from "../utils/csrf";
import { purchaseQuery } from "../purchases/admin/lessons/purchases";
import { lessonSchedulesQuery } from "../lesson-schedules/lesson-schedules";

const endpoint = "/reservation" as const;

type IDeleteReservation = { id: string };

type IDeleteReservationReturn = {};

export const useDeleteReservation = () => {
  const queryClient = useQueryClient();
  return useMutation<IDeleteReservationReturn, AxiosError, IDeleteReservation>(
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
        queryClient.invalidateQueries({ queryKey: purchaseQuery().queryKey });
        queryClient.invalidateQueries({ queryKey: lessonSchedulesQuery().queryKey });
      },
    },
  );
};
