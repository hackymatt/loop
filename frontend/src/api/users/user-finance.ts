import { AxiosError } from "axios";
import { compact } from "lodash-es";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

import { IUserFinanceProps } from "src/types/user";

import { Api } from "../service";
import { GetQueryResponse } from "../types";
import { getData, getCsrfToken } from "../utils";

const endpoint = "/users-finance" as const;

export type IUserFinance = {
  account: string | null;
  commission: number | null;
  rate: number | null;
};

type IEditUserFinance = IUserFinance;

type IEditUserFinanceReturn = IEditUserFinance;

export const userFinanceQuery = (id: string) => {
  const url = endpoint;
  const queryUrl = `${url}/${id}`;

  const queryFn = async (): Promise<GetQueryResponse<IUserFinanceProps>> => {
    const { data } = await getData<IUserFinance>(queryUrl);

    return { results: data };
  };

  return { url, queryFn, queryKey: compact([endpoint, id]) };
};

export const useUserFinance = (id: string) => {
  const { queryKey, queryFn } = userFinanceQuery(id);
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.results, ...rest };
};

export const useEditUserFinance = (id: string) => {
  const queryClient = useQueryClient();
  const url = `${endpoint}/${id}`;
  return useMutation<IEditUserFinanceReturn, AxiosError, IEditUserFinance>(
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
