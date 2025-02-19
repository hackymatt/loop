import { AxiosError } from "axios";
import { useMutation, useQueryClient } from "@tanstack/react-query";

import { Api } from "../service";
import { getCsrfToken } from "../utils";

const endpoint = "/wishlist" as const;

type IDeleteWishlist = { id: string };

type IDeleteWishlistReturn = {};

export const useDeleteWishlist = () => {
  const queryClient = useQueryClient();
  return useMutation<IDeleteWishlistReturn, AxiosError, IDeleteWishlist>(
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
