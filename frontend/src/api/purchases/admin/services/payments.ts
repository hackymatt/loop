import { AxiosError } from "axios";
import { compact } from "lodash-es";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

import { formatQueryParams } from "src/utils/query-params";

import { IQueryParams } from "src/types/query-params";
import {
  IPaymentProp,
  IPaymentStatus,
  IPaymentMethodProp,
  IPaymentCurrencyProp,
} from "src/types/payment";

import { Api } from "../../../service";
import { getCsrfToken } from "../../../utils/csrf";

const endpoint = "/service-payments" as const;

type IPayment = {
  id: string;
  session_id: string;
  amount: number;
  currency: IPaymentCurrencyProp;
  method: IPaymentMethodProp;
  status: IPaymentStatus;
  created_at: string;
};

type ICreatePayment = Omit<IPayment, "id" | "session_id" | "created_at">;

type ICreatePaymentReturn = ICreatePayment;

export const paymentQuery = (query?: IQueryParams) => {
  const url = endpoint;
  const urlParams = formatQueryParams(query);
  const queryUrl = urlParams ? `${url}?${urlParams}` : url;

  const queryFn = async () => {
    const { data } = await Api.get(queryUrl);
    const { results, records_count, pages_count } = data;
    const modifiedResults = results.map(
      ({ id, session_id, amount, currency, method, status, created_at }: IPayment) => ({
        id,
        sessionId: session_id,
        amount: amount / 100,
        currency,
        method,
        status,
        createdAt: created_at,
      }),
    );
    return { results: modifiedResults, count: records_count, pagesCount: pages_count };
  };

  return { url, queryFn, queryKey: compact([endpoint, urlParams]) };
};

export const usePayments = (query?: IQueryParams, enabled: boolean = true) => {
  const { queryKey, queryFn } = paymentQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn, enabled });
  return { data: data?.results as IPaymentProp[], count: data?.count, ...rest };
};

export const usePaymentsPageCount = (query?: IQueryParams) => {
  const { queryKey, queryFn } = paymentQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.pagesCount, ...rest };
};

export const useCreatePayment = () => {
  const queryClient = useQueryClient();
  return useMutation<ICreatePaymentReturn, AxiosError, ICreatePayment>(
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
        queryClient.invalidateQueries({ queryKey: [endpoint] });
      },
    },
  );
};
