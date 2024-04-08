import { AxiosError } from "axios";
import { useMutation, useQueryClient } from "@tanstack/react-query";

import { Api } from "../service";
import { getCsrfToken } from "../utils/csrf";

const endpoint = "/wishlist" as const;

type IDeleteWishlist = {};

type IDeleteWishlistReturn = {};

export const useDeleteWishlist = (id: string) => {
  const queryClient = useQueryClient();
  const url = `${endpoint}/${id}`;
  return useMutation<IDeleteWishlistReturn, AxiosError, IDeleteWishlist>(
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
