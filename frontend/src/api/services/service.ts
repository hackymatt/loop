import { AxiosError } from "axios";
import { compact } from "lodash-es";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

import { IServiceProp } from "src/types/service";

import { Api } from "../service";
import { GetQueryResponse } from "../types";
import { getData, getCsrfToken } from "../utils";

const endpoint = "/services" as const;

type IService = {
  id: string;
  title: string;
  description: string;
  price: number;
  active: boolean;
};

type IEditService = Omit<IService, "id">;
type IEditServiceReturn = IEditService;
export const serviceQuery = (id: string) => {
  const url = endpoint;
  const queryUrl = `${url}/${id}`;

  const queryFn = async (): Promise<GetQueryResponse<IServiceProp>> => {
    const { result } = await getData<IService>(queryUrl);
    return { results: result };
  };

  return { url, queryFn, queryKey: compact([endpoint, id]) };
};

export const useService = (id: string) => {
  const { queryKey, queryFn } = serviceQuery(id);
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.results as any as IServiceProp, ...rest };
};

export const useEditService = (id: string) => {
  const queryClient = useQueryClient();
  const url = `${endpoint}/${id}`;
  return useMutation<IEditServiceReturn, AxiosError, IEditService>(
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
