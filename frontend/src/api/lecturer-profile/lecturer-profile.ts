import { AxiosError } from "axios";
import { compact } from "lodash-es";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

import { Api } from "../service";
import { getCsrfToken } from "../utils/csrf";

const endpoint = "/lecturer-details" as const;

type ILecturerDetail = {
  title: string;
  linkedin_url: string;
  description: string;
};

type IEditLecturerDetail = ILecturerDetail;

type IEditLecturerDetailReturn = IEditLecturerDetail;

export const userLecturerDetailsQuery = () => {
  const url = endpoint;

  const queryFn = async () => {
    const response = await Api.get<ILecturerDetail>(url, {
      headers: {
        "X-CSRFToken": getCsrfToken(),
      },
    });
    const { data } = response;

    return { results: data };
  };

  return { url, queryFn, queryKey: compact([endpoint]) };
};

export const useUserLecturerDetail = () => {
  const { queryKey, queryFn } = userLecturerDetailsQuery();
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.results, ...rest };
};

export const useEditUserLecturerDetail = () => {
  const queryClient = useQueryClient();
  const url = endpoint;
  return useMutation<IEditLecturerDetailReturn, AxiosError, IEditLecturerDetail>(
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
