import { compact } from "lodash-es";
import { useQuery } from "@tanstack/react-query";

import { formatQueryParams } from "src/utils/query-params";

import { IQueryParams } from "src/types/query-params";
import {
  IPaymentProp,
  IPaymentStatus,
  IPaymentMethodProp,
  IPaymentCurrencyProp,
} from "src/types/payment";

import { Api } from "../service";

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
