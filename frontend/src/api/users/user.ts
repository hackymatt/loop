import { AxiosError } from "axios";
import { compact } from "lodash-es";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

import { IUserDetailsProps } from "src/types/user";

import { Api } from "../service";
import { getCsrfToken } from "../utils/csrf";

const endpoint = "/users" as const;

type IEditUser = IUserDetailsProps;

type IEditUserReturn = IEditUser;

export const userQuery = (id: string) => {
  const url = endpoint;
  const queryUrl = `${url}/${id}`;

  const queryFn = async () => {
    let modifiedResults;
    try {
      const response = await Api.get<IUserDetailsProps>(queryUrl);
      const { data } = response;
      modifiedResults = data;
    } catch (error) {
      if (error.response && (error.response.status === 400 || error.response.status === 404)) {
        modifiedResults = {};
      }
    }
    return { results: modifiedResults };
  };

  return { url, queryFn, queryKey: compact([endpoint, id]) };
};

export const useUser = (id: string) => {
  const { queryKey, queryFn } = userQuery(id);
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.results as any as IUserDetailsProps, ...rest };
};

export const useEditUser = (id: string) => {
  const queryClient = useQueryClient();
  const url = `${endpoint}/${id}`;
  return useMutation<IEditUserReturn, AxiosError, IEditUser>(
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
