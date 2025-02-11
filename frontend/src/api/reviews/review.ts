import { AxiosError } from "axios";
import { useMutation, useQueryClient } from "@tanstack/react-query";

import { IGender } from "src/types/testimonial";

import { Api } from "../service";
import { getCsrfToken } from "../utils/csrf";
import { purchaseQuery } from "../purchases/admin/lessons/purchases";

const endpoint = "/reviews" as const;

type IProfile = {
  full_name: string;
  gender: IGender | null;
  image: string | null;
};

type IReview = {
  id: string;
  lesson_title: string;
  student: IProfile;
  lecturer: IProfile;
  created_at: string;
  review?: string | null;
  rating: number;
};

type IEditReview = Pick<IReview, "rating" | "review"> & { lesson: string; lecturer: string };

type IEditReviewReturn = IEditReview;

type IDeleteReview = { id: string };

type IDeleteReviewReturn = {};

export const useEditReview = (id: string) => {
  const queryClient = useQueryClient();
  const url = `${endpoint}/${id}`;
  return useMutation<IEditReviewReturn, AxiosError, IEditReview>(
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
        queryClient.invalidateQueries({ queryKey: purchaseQuery().queryKey });
      },
    },
  );
};

export const useDeleteReview = () => {
  const queryClient = useQueryClient();
  return useMutation<IDeleteReviewReturn, AxiosError, IDeleteReview>(
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
        queryClient.invalidateQueries({ queryKey: purchaseQuery().queryKey });
      },
    },
  );
};
