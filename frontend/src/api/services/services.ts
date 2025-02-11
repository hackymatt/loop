import { AxiosError } from "axios";
import { compact } from "lodash-es";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

import { formatQueryParams } from "src/utils/query-params";

import { IServiceProp } from "src/types/service";
import { IQueryParams } from "src/types/query-params";

import { Api } from "../service";
import { getCsrfToken } from "../utils/csrf";

const endpoint = "/services" as const;

type IService = {
  id: string;
  title: string;
  description: string;
  price: number;
  active: boolean;
};

type ICreateService = Omit<IService, "id">;

type ICreateServiceReturn = ICreateService;
export const servicesQuery = (query?: IQueryParams) => {
  const url = endpoint;
  const urlParams = formatQueryParams(query);
  const queryUrl = urlParams ? `${url}?${urlParams}` : url;

  const queryFn = async () => {
    let data;
    try {
      const response = await Api.get(queryUrl);
      ({ data } = response);
    } catch (error) {
      if (error.response && (error.response.status === 400 || error.response.status === 404)) {
        data = { results: [], records_count: 0, pages_count: 0 };
      }
    }
    const { results, records_count, pages_count } = data;
    return { results, count: records_count, pagesCount: pages_count };
  };

  return { url, queryFn, queryKey: compact([endpoint, urlParams]) };
};

export const useServices = (query?: IQueryParams, enabled: boolean = true) => {
  const { queryKey, queryFn } = servicesQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn, enabled });
  return { data: data?.results as IServiceProp[], count: data?.count, ...rest };
};

export const useServicesPagesCount = (query?: IQueryParams) => {
  const { queryKey, queryFn } = servicesQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.pagesCount, ...rest };
};

export const useCreateService = () => {
  const queryClient = useQueryClient();
  return useMutation<ICreateServiceReturn, AxiosError, ICreateService>(
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
