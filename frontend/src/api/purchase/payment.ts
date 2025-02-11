import { AxiosError } from "axios";
import { compact } from "lodash-es";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

import { IPaymentStatus } from "src/types/payment";
import { IPaymentItemProp, IPaymentMethodProp, IPaymentCurrencyProp } from "src/types/purchase";

import { Api } from "../service";
import { getCsrfToken } from "../utils/csrf";

const endpoint = "/payments" as const;

type IPayment = {
  id: string;
  session_id: string;
  amount: number;
  currency: IPaymentCurrencyProp;
  method: IPaymentMethodProp;
  status: IPaymentStatus;
  created_at: string;
};

type IEditPayment = Omit<IPayment, "id" | "session_id" | "created_at">;

type IEditPaymentReturn = IEditPayment;

export const paymentQuery = (id: string) => {
  const url = endpoint;
  const queryUrl = `${url}/${id}`;

  const queryFn = async () => {
    let modifiedResults;
    try {
      const response = await Api.get<IPayment>(queryUrl);
      const { data } = response;
      const { id: paymentId, session_id, amount, currency, method, status, created_at } = data;

      modifiedResults = {
        id: paymentId,
        sessionId: session_id,
        amount: amount / 100,
        currency,
        method,
        status,
        createdAt: created_at,
      };
    } catch (error) {
      if (error.response && (error.response.status === 400 || error.response.status === 404)) {
        modifiedResults = {};
      }
    }
    return { results: modifiedResults };
  };

  return { url, queryFn, queryKey: compact([endpoint, id]) };
};

export const usePayment = (id: string) => {
  const { queryKey, queryFn } = paymentQuery(id);
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.results as any as IPaymentItemProp, ...rest };
};

export const useEditPayment = (id: string) => {
  const queryClient = useQueryClient();
  const url = `${endpoint}/${id}`;
  return useMutation<IEditPaymentReturn, AxiosError, IEditPayment>(
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
