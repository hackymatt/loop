import { AxiosError } from "axios";
import { compact } from "lodash-es";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

import { IGender } from "src/types/testimonial";
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

type IEditPurchase = Omit<IPurchase, "id" | "created_at" | "service" | "other" | "payment"> & {
  service: string;
  other: string;
  payment: string;
};

type IEditPurchaseReturn = IEditPurchase;

type IDeletePurchase = { id: string };

type IDeletePurchaseReturn = {};

export const servicePurchaseQuery = (id: string) => {
  const url = endpoint;
  const queryUrl = `${url}/${id}`;

  const queryFn = async () => {
    const response = await Api.get<IPurchase>(queryUrl);
    const { data } = response;
    const { id: purchaseId, other, service, price, payment, created_at } = data;
    const { id: serviceId, title: serviceTitle } = service;
    const modifiedResults = {
      id: purchaseId,
      lessonId: serviceId,
      lessonTitle: serviceTitle,
      lessonPrice: price,
      teacher: other,
      paymentId: payment,
      createdAt: created_at,
    };
    return { results: modifiedResults };
  };

  return { url, queryFn, queryKey: compact([endpoint, id]) };
};

export const useServicePurchase = (id: string) => {
  const { queryKey, queryFn } = servicePurchaseQuery(id);
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.results as any as IPurchaseItemProp, ...rest };
};

export const useEditServicePurchase = (id: string) => {
  const queryClient = useQueryClient();
  const url = `${endpoint}/${id}`;
  return useMutation<IEditPurchaseReturn, AxiosError, IEditPurchase>(
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

export const useDeleteServicePurchase = () => {
  const queryClient = useQueryClient();
  return useMutation<IDeletePurchaseReturn, AxiosError, IDeletePurchase>(
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
