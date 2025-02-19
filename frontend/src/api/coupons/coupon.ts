import { AxiosError } from "axios";
import { compact } from "lodash-es";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

import { ICouponProps } from "src/types/coupon";

import { Api } from "../service";
import { getCsrfToken } from "../utils";

const endpoint = "/coupons" as const;

type IEditCoupon = Omit<ICouponProps, "id" | "users"> & { users: string[] };

type IEditCouponReturn = IEditCoupon;

type IDeleteCoupon = { id: string };

type IDeleteCouponReturn = {};

export const couponQuery = (id: string) => {
  const url = endpoint;
  const queryUrl = `${url}/${id}`;

  const queryFn = async () => {
    let modifiedResults;
    try {
      const response = await Api.get<ICouponProps>(queryUrl);
      const { data } = response;
      modifiedResults = data;
    } catch (error) {
      if (error.response && (error.response.status === 400 || error.response.status === 404)) {
        modifiedResults = {};
      }
    }
    return { results: modifiedResults };
  };

  return { url, queryFn, queryKey: compact([endpoint, id]) };
};

export const useCoupon = (id: string) => {
  const { queryKey, queryFn } = couponQuery(id);
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.results as any as ICouponProps, ...rest };
};

export const useEditCoupon = (id: string) => {
  const queryClient = useQueryClient();
  const url = `${endpoint}/${id}`;
  return useMutation<IEditCouponReturn, AxiosError, IEditCoupon>(
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

export const useDeleteCoupon = () => {
  const queryClient = useQueryClient();
  return useMutation<IDeleteCouponReturn, AxiosError, IDeleteCoupon>(
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
