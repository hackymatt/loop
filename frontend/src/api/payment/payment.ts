import { compact } from "lodash-es";
import { useQuery } from "@tanstack/react-query";

import { formatQueryParams } from "src/utils/query-params";

import { IQueryParams } from "src/types/query-params";
import { IPaymentProp, IPaymentStatus } from "src/types/payment";

import { Api } from "../service";

const endpoint = "/payment-status" as const;

type IPayment = {
  session_id: string;
  order_id: number;
  amount: number;
  status: IPaymentStatus;
};

export const paymentQuery = (query?: IQueryParams) => {
  const url = endpoint;
  const urlParams = formatQueryParams(query);
  const queryUrl = urlParams ? `${url}?${urlParams}` : url;

  const queryFn = async () => {
    let modifiedResults;
    try {
      const response = await Api.get<IPayment>(queryUrl);
      const { data } = response;
      const { session_id, order_id, amount, status } = data;

      modifiedResults = {
        sessionId: session_id,
        orderId: order_id,
        amount,
        status,
      };
    } catch (error) {
      if (error.response && (error.response.status === 400 || error.response.status === 404)) {
        modifiedResults = {};
      }
    }
    return { results: modifiedResults };
  };

  return { url, queryFn, queryKey: compact([endpoint, urlParams]) };
};

export const usePaymentStatus = (
  query?: IQueryParams,
  enabled: boolean = true,
  refetchInterval: number = 0,
) => {
  const { queryKey, queryFn } = paymentQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn, enabled, refetchInterval });
  return { data: data?.results as any as IPaymentProp, ...rest };
};
