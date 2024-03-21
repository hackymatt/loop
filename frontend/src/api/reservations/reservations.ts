import { AxiosError } from "axios";
import { useMutation, useQueryClient } from "@tanstack/react-query";

import { Api } from "../service";
import { getCsrfToken } from "../utils/csrf";
import { purchaseQuery } from "../purchase/purchase";
import { lessonSchedulesQuery } from "../lesson-schedules/lesson-schedules";

const endpoint = "/reservation" as const;

type ICreateReservation = { lesson: string; schedule: string };
type ICreateReservationReturn = ICreateReservation;

export const useCreateReservation = () => {
  const queryClient = useQueryClient();
  return useMutation<ICreateReservationReturn, AxiosError, ICreateReservation>(
    async (variables) => {
      const result = await Api.post(endpoint, variables, {
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
