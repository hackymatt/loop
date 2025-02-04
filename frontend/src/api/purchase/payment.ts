import { compact } from "lodash-es";
import { useQuery } from "@tanstack/react-query";

import { formatQueryParams } from "src/utils/query-params";

import { IPaymentStatus } from "src/types/payment";
import { IQueryParams } from "src/types/query-params";
import { IPaymentItemProp } from "src/types/purchase";

import { Api } from "../service";

const endpoint = "/payments" as const;

type IPayment = {
  session_id: string;
  amount: number;
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
    const modifiedResults = results.map(({ session_id, amount, status, created_at }: IPayment) => ({
      id: session_id,
      amount: amount / 100,
      status,
      createdAt: created_at,
    }));
    return { results: modifiedResults, count: records_count, pagesCount: pages_count };
  };

  return { url, queryFn, queryKey: compact([endpoint, urlParams]) };
};

export const usePayments = (query?: IQueryParams, enabled: boolean = true) => {
  const { queryKey, queryFn } = paymentQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn, enabled });
  return { data: data?.results as IPaymentItemProp[], count: data?.count, ...rest };
};

export const usePaymentsPageCount = (query?: IQueryParams) => {
  const { queryKey, queryFn } = paymentQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.pagesCount, ...rest };
};
