import { AxiosError } from "axios";
import { compact } from "lodash-es";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

import { Api } from "../service";
import { getCsrfToken } from "../utils";

const endpoint = "/finance-details" as const;

type IFinanceDetail = {
  account?: string | null;
  rate?: number | null;
  commission?: number | null;
};

type IEditFinanceDetail = Pick<IFinanceDetail, "account">;

type IEditFinanceDetailReturn = IEditFinanceDetail;

export const userFinanceDetailsQuery = () => {
  const url = endpoint;

  const queryFn = async () => {
    const response = await Api.get<IFinanceDetail>(url, {
      headers: {
        "X-CSRFToken": getCsrfToken(),
      },
    });
    const { data } = response;

    return { results: data };
  };

  return { url, queryFn, queryKey: compact([endpoint]) };
};

export const useUserFinanceDetail = () => {
  const { queryKey, queryFn } = userFinanceDetailsQuery();
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.results, ...rest };
};

export const useEditUserFinanceDetail = () => {
  const queryClient = useQueryClient();
  const url = endpoint;
  return useMutation<IEditFinanceDetailReturn, AxiosError, IEditFinanceDetail>(
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
