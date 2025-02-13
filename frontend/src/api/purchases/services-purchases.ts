import { AxiosError } from "axios";
import { compact } from "lodash-es";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

import { formatQueryParams } from "src/utils/query-params";

import { IGender } from "src/types/testimonial";
import { IQueryParams } from "src/types/query-params";
import { IPurchaseItemProp } from "src/types/purchase";

import { Api } from "../service";
import { getCsrfToken } from "../utils/csrf";

const endpoint = "/service-purchases" as const;

type IService = {
  id: string;
  title: string;
};

type IOther = {
  id: string;
  full_name: string;
  image: string | null;
  gender: IGender;
};

type IPurchase = {
  id: string;
  service: IService;
  other: IOther;
  created_at: string;
  price: number;
  payment: string;
};

type ICreatePurchase = Omit<IPurchase, "id" | "created_at" | "service" | "other" | "payment"> & {
  service: string;
  other: string;
  payment: string;
};

type ICreatePurchaseReturn = ICreatePurchase;

export const servicePurchasesQuery = (query?: IQueryParams) => {
  const url = endpoint;
  const urlParams = formatQueryParams(query);
  const queryUrl = urlParams ? `${url}?${urlParams}` : url;

  const queryFn = async () => {
    const { data } = await Api.get(queryUrl);
    const { results, records_count, pages_count } = data;
    const modifiedResults = results.map(
      ({ id, service, other, price, payment, created_at }: IPurchase) => {
        const { id: serviceId, title: serviceTitle } = service;
        return {
          id,
          lessonId: serviceId,
          lessonTitle: serviceTitle,
          lessonPrice: price,
          teacher: other,
          paymentId: payment,
          createdAt: created_at,
        };
      },
    );
    return { results: modifiedResults, count: records_count, pagesCount: pages_count };
  };

  return { url, queryFn, queryKey: compact([endpoint, urlParams]) };
};

export const useServicePurchases = (query?: IQueryParams, enabled: boolean = true) => {
  const { queryKey, queryFn } = servicePurchasesQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn, enabled });
  return { data: data?.results as IPurchaseItemProp[], count: data?.count, ...rest };
};

export const useServicePurchasesPageCount = (query?: IQueryParams) => {
  const { queryKey, queryFn } = servicePurchasesQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.pagesCount, ...rest };
};

export const useCreatePurchase = () => {
  const queryClient = useQueryClient();
  return useMutation<ICreatePurchaseReturn, AxiosError, ICreatePurchase>(
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
